import sys
import io
import asyncio
import inspect
import traceback
import logging
from functools import partialmethod

import re
import makefun

from .client import Route, Channel

class State:
    def __init__(self, attributes=None, methods=None, repr=None, doc=None, pipeline=None):
        self.attributes = attributes or []
        self.methods = methods or {}
        self.pipeline = pipeline or []
        self.repr = repr or ''
        self.doc = doc

    def to_dict(self):
        return {
            'attributes': self.attributes,
            'methods': self.methods,
            'pipeline': self.pipeline,
            'repr': self.repr,
            'doc': self.doc
        }
    
    def clone(self):
        return State(**self.to_dict())
    
    @staticmethod
    def from_object(target):
        logger = logging.getLogger(__name__)
        
        attributes, methods, repr_ = [], {}, ''
        
        for attribute_name in dir(target):
            if attribute_name[0] != '_'  or attribute_name in ['__call__', '__getitem__', '__setitem__', '__add__', '__mul__']:
                try:
                    if isinstance(target, type):
                        target_attribute = target.__getattribute__(target, attribute_name)
                    else:
                        target_attribute = target.__getattribute__(attribute_name)

                    if '__call__' in dir(target_attribute):
                        if attribute_name == '__call__':
                            target_attribute = target
                        signature = None
                        try:
                            signature = str(inspect.signature(target_attribute))
                            
                            if '_tk_inject_first_arg' in dir(target_attribute) \
                            and target_attribute._tk_inject_first_arg:
                                signature = re.sub(r'[a-zA-Z0-9=\_\s]+(?=[\)\,])', '', signature, 1)\
                                                .replace('(,','(',1).replace('( ','(',1)
                        except:
                            logger.debug('Cound not obtain signature from %s.%s', 
                                        target, attribute_name)

                        methods[attribute_name] = (signature, target_attribute.__doc__)
                    else:
                        attributes.append(attribute_name)

                except Exception as e:
                    logger.error('Could not obtain handle for %s.%s: %s', target, 
                                 attribute_name, e)

        if isinstance(target, type):
            repr_ =  str(type(target))
            methods['__call__'] = (str(inspect.signature(target)), target.__init__.__doc__)
            doc = target.__doc__
        else:
            doc = None
            repr_ = target.__repr__()

        return State(attributes, methods, repr_, doc)

class Listener:
    def __init__(self, channel, expose_tb=True, max_depth=None, mask=None):
        self.channel = channel
        self.coro_callback = None
        self.expose_tb = expose_tb
        self.max_depth = max_depth
        self.mask = mask
        self.current_tasks = set()
    
    def set_callback(self, coro_callback):
        self.coro_callback = coro_callback
        self.listen_task = asyncio.get_event_loop().create_task(self.listen())
        return self

    async def listen(self):
        while True:
            try:
                await self.channel.listen()
                while True:
                    message = await self.channel.recv()

                    self.current_tasks.add(asyncio.get_event_loop().create_task(
                        self.coro_callback(self, self.channel, *message)))

                    await asyncio.gather(*(x for x in self.current_tasks if x.done()))
                    self.current_tasks = set(x for x in self.current_tasks if not x.done())
            except:
                logging.getLogger(__name__).error('', exc_info=True)

class Telekinesis():
    def __init__(self, target, session, parent=None):
        self._logger = logging.getLogger(__name__)
        self._target = target
        self._session = session
        self._parent = parent
        self._listeners = {}
        if isinstance(target, Route):
            self._state = State()
        else:
            self._update_state(State.from_object(target))
       
    def __getattribute__(self, attr):
        if (attr[0] == '_'): #and (attr != '__call__'):
            return super().__getattribute__(attr)
        
        state = self._state.clone()
        state.pipeline.append(('get', attr))

        return Telekinesis._from_state(self._target, self._session, state, self)

    def _get_root_state(self):
        if self._parent:
            return self._parent._get_root_state()
        return self._state

    def _update_root_state(self, state):
        if self._parent:
            return self._parent._update_root_state(state)
        return self._update_state(state)

    def _update_state(self, state):
        for d in dir(self):
            if d[0] != '_':
                self.__delattr__(d)

        for method_name in state.methods:
            if method_name[0] != '_':
                self.__setattr__(method_name, None)

        for attribute_name in state.attributes:
            if attribute_name[0] != '_':
                self.__setattr__(attribute_name, None)

        self._state = state

        return self

    def _add_listener(self, channel, expose_tb=True, max_depth=None, mask=None):
        route = channel.route

        channel.telekinesis = self
        
        self._listeners[route] = Listener(channel, expose_tb, max_depth, mask).set_callback(self._handle)
        
        return route

    async def _handle(self, listener, channel, reply, payload):
        try:
            pipeline = self._decode(payload.get('pipeline'), reply.session)
            self._logger.info('%s called %s', reply.session[:4], len(pipeline))
            ret = await self._execute(reply, listener, pipeline)
            
            await channel.send(reply, {
                'return': self._encode(ret, reply.session, listener),
                'repr': self._state.repr})
        except:
            self._logger.error(payload, exc_info=True)

            self._state.pipeline.clear()
            await channel.send(reply, {
                'error': traceback.format_exc() if listener.expose_tb else ''})
    
    def _delegate(self, recepient_id, listener=None):
        if isinstance(self._target, Route):
            route = self._target.clone()

        else:
            if isinstance(listener, Listener):
                route = self._add_listener(Channel(self._session), listener.expose_tb, 
                                        listener.max_depth, listener.mask)
            else:
                route = self._add_listener(Channel(self._session))
                listener = self._listeners[route]
        
        token_header = self._session.extend_route(route, recepient_id, listener.max_depth)
        listener.channel.header_buffer.append(token_header)
        
        return route

    def _call(self, *args, **kwargs):
        state = self._state.clone()
        state.pipeline.append(('call', (args, kwargs)))

        return Telekinesis._from_state(self._target, self._session, state, self)

    async def _execute(self, route=None, listener=None, pipeline=None):
        if not pipeline:
            pipeline = []

        pipeline = self._state.pipeline + pipeline
        self._state.pipeline.clear()
        
        if isinstance(self._target, Route):
            out = {}
            async with Channel(self._session) as new_channel:
                await new_channel.send(
                    self._target,
                    {'pipeline': self._encode(pipeline, self._target.session, Listener(new_channel))})

                _, out = await new_channel.recv()
            
            if 'error' in out:
                raise Exception(out['error'])

            if 'return' in out:
                output = self._decode(out['return'], self._target.session)
                state = self._get_root_state()
                state.repr = out['repr']
                return output

            raise Exception('Telekinesis communication error: received unrecognized message schema')
        
        async def exc(x):
            if isinstance(x, Telekinesis) and x._state.pipeline:
                return (await x._execute(route))
            return x

        target = self._target
        for action, arg in pipeline:
            if action == 'get':
                self._logger.info('%s %s %s', action, arg, target)
                if arg[0] == '_' and arg not in ['__getitem__', '__setitem__', '__add__', '__mul__']:
                    raise Exception('Unauthorized!')
                target = target.__getattribute__(arg)
            if action == 'call':
                self._logger.info('%s %s', action, target)
                ar, kw = arg
                args, kwargs = [await exc(x) for x in ar], {x: await exc(kw[x]) for x in kw}
                
                if '_tk_inject_first_arg' in dir(target) \
                and target._tk_inject_first_arg:
                    target = target(route, *args, **kwargs)
                else:
                    target = target(*args, **kwargs)
                if asyncio.iscoroutine(target):
                    target = await target
        
        self._update_state(State.from_object(self._target))
        return target

    def __await__(self):
        return self._execute().__await__()

    def __repr__(self):
        return '\033[92m\u2248\033[0m ' + str(self._state.repr)

    def _encode(self, arg, receiver_id=None, listener=None):
        if type(arg) in (int, float, str, bytes, bool, type(None)):
            return (type(arg).__name__, arg)
        if type(arg) in (range, slice):
            return (type(arg).__name__, (arg.start, arg.stop, arg.step))
        if type(arg) in (list, tuple, set):
            return (type(arg).__name__, [self._encode(v, receiver_id, listener) for v in arg])
        if isinstance(arg, dict):
            return ('dict', {x: self._encode(arg[x], receiver_id, listener) for x in arg})
        if isinstance(arg, Telekinesis):
            obj = arg
        else:
            obj = Telekinesis(arg, self._session)
            
        route = obj._delegate(receiver_id, listener)
        return ('obj', (route.to_dict(), obj._state.to_dict()))

    def _decode(self, tup, caller_id=None):
        typ, obj = tup
        if typ in ('int', 'float', 'str', 'bytes', 'bool', 'NoneType'):
            return obj
        if typ in ('range', 'slice'):
            return {'range': range, 'slice': slice}[typ](*obj)
        if typ in ('list', 'tuple', 'set'):
            return {'list':list, 'tuple':tuple, 'set':set}[typ]([self._decode(v, caller_id) 
                                                                 for v in obj])
        if typ == 'dict':
            return {x: self._decode(obj[x], caller_id) for x in obj}
        
        route = Route(**obj[0])
        state = State(**obj[1])
        if route.session == self._session.session_key.public_serial() and route.channel in self._session.channels:
            channel = self._session.channels.get(route.channel)
            if channel.validate_token_chain(caller_id, route.tokens):
                return Telekinesis._from_state(channel.telekinesis._target, self._session, state, channel.telekinesis)
            else:
                raise Exception('Unauthorized!')

        return Telekinesis._from_state(route, self._session, State(**obj[1]))

    @staticmethod
    def _from_state(target, session, state, parent=None):
        def callable_subclass(signature, method_name, docstring):
            class Telekinesis_(Telekinesis):
                @makefun.with_signature(signature,
                                        func_name=method_name,
                                        doc=docstring if method_name == '__call__' else None,
                                        module_name='telekinesis.telekinesis')
                def __call__(self, *args, **kwargs):
                    return self._call(*args, **kwargs)
            
            return Telekinesis_

        method_name = state.pipeline[-1][1] if state.pipeline and state.pipeline[-1][0] == 'get' \
                                            else '__call__'

        reset = 'call' in [x[0] for x in state.pipeline[:-1]]
        if method_name in state.methods or reset:
            signature, docstring = (not reset and state.methods.get(method_name)) or (None, None)
            signature = signature or '(*args, **kwargs)'
            # if not isinstance(target, type):
            signature = signature.replace('(', '(self, ')

            stderr = sys.stderr
            sys.stderr = io.StringIO()

            try:
                if session.compile_signatures and check_signature(signature):
                    Telekinesis_ = callable_subclass(signature, method_name, docstring)
                else:
                    Telekinesis_ = callable_subclass('(self, *args, **kwargs)', method_name, docstring)
            except:
                Telekinesis_ = callable_subclass('(self, *args, **kwargs)', method_name, docstring)

            sys.stderr = stderr

        else:
            Telekinesis_ = Telekinesis
            docstring = None
        
        if method_name == '__call__':
            def dundermethod(self, method, key):
                state = self._state.clone()
                state.pipeline.append(('get', method))
                state.pipeline.append(('call', ((key,), {})))
                return Telekinesis._from_state(self._target, self._session, state, self)

            def setitem(self, key, value):
                state = self._state
                state.pipeline.append(('get', '__setitem__'))
                state.pipeline.append(('call', ((key, value), {})))
                return Telekinesis._from_state(self._target, self._session, state, self)

            if '__getitem__' in state.methods:
                Telekinesis_.__getitem__ = partialmethod(dundermethod, '__getitem__')
            if '__add__' in state.methods:
                Telekinesis_.__add__ = partialmethod(dundermethod, '__getitem__')
            if '__mul__' in state.methods:
                Telekinesis_.__mul__ = partialmethod(dundermethod, '__getitem__')
            if '__setitem__' in state.methods:
                Telekinesis_.__setitem__ = setitem

        out = Telekinesis_(target, session, parent)._update_state(state)
        out.__doc__ = state.doc if method_name == '__call__' else docstring

        return out

def check_signature(signature):
    return not ('\n' in signature or \
                (signature != re.sub(r'(?:[^A-Za-z0-9_])lambda(?=[\)\s\:])', '', signature)))

def inject_first_arg(func):
    func._tk_inject_first_arg = True
    return func
