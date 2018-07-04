
def strong_parameters(params, keys=[]):
    arguments = {}
    for key in keys:
        if key in params:
            arguments[key] = params[key]

    return arguments
