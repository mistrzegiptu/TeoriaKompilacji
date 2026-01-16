# visit.py
import inspect

def on(param_name):
    def f(fn):
        dispatcher = Dispatcher(param_name, fn)
        return dispatcher
    return f

def when(param_type):
    def f(fn):
        frame = inspect.currentframe().f_back
        dispatcher = frame.f_locals.get(fn.__name__)
        if not isinstance(dispatcher, Dispatcher):
            dispatcher = dispatcher.dispatcher
        dispatcher.add_target(param_type, fn)
        def ff(*args, **kwargs):
            return dispatcher(*args, **kwargs)
        ff.dispatcher = dispatcher
        return ff
    return f

class Dispatcher(object):
    def __init__(self, param_name, fn):
        parent = inspect.currentframe().f_back
        self.param_index = inspect.getfullargspec(fn).args.index(param_name)
        self.param_name = param_name
        self.targets = {}

    def __call__(self, *args, **kw):
        typ = args[self.param_index].__class__
        d = self.targets.get(typ)
        if d is not None:
            return d(*args, **kw)
        arg = args[self.param_index]
        param = list(inspect.getfullargspec(self.targets[typ]).args)
        
        for t in self.targets:
            if issubclass(typ, t):
                return self.targets[t](*args, **kw)
        return None

    def add_target(self, typ, target):
        self.targets[typ] = target