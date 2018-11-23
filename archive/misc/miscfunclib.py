import re

#valid_identifier = re.compile(r'^[_a-zA-Z]\w*$')
valid_identifier = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def identify_number(strg):
    if type(strg).__name__ in ("float", "int"):
        return type(strg).__name__
    try:
        float(strg)
        strg_type = "float"
        if strg[0] in ("+", "-"):
            strg = strg[1:]
        if strg.isdigit():
            strg_type = "int"
        return strg_type
    except ValueError:
        return "str"


def args_into_func(func, **args): 
    '''Assign a dictionary of keyword arguments to a function
    Ref: http://stackoverflow.com/questions/817087/call-a-function-with-argument-list-in-python
    '''
    return func(**args)


def tryto_curry_node_with_args(rootNode, func, **kwargs):
    apply_args = []
    apply_kwargs = {}
    #func_args = inspect.getargspec(func).args
    for ii, func_arg in enumerate(inspect.getargspec(func).args):
        if func_arg in kwargs:
            if ii==len(apply_args):
                apply_args.append(kwargs[func_arg])
            else:
                apply_kwargs[func_arg]=kwargs[func_arg]
    """for ii, (kwarg, value) in enumerate(kwargs.items()):
        if kwarg not in func_args:
            continue
        if ii == func_args.index(kwarg):
            apply_args.append(value)
        else:
            apply_kwargs[kwarg]=value"""
    print("func_args=", inspect.getargspec(func).args)
    print("apply_args=", apply_args)
    print("apply_kwargs=", apply_kwargs)
    if apply_args or apply_kwargs:
        # WARNING: functools.partial does not 'curry' **apply_kwargs below,
        # to be safe use keywords args only with func_to_patch
        # http://stackoverflow.com/questions/24755463/functools-partial-wants-to-use-a-positional-argument-as-a-keyword-argument
        #func_to_patch = functools.partial(func, **apply_kwargs)
        func_to_patch = functools.partial(func, *apply_args, **apply_kwargs)
    else:
        func_to_patch = func
    # WARNING: assuming no super-class nodes in tree!
    setattr(rootNode.__class__, func.__name__, func_to_patch)


