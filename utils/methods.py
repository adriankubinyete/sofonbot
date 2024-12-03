def methods(thing):
    # iterate over thing and show all methods:
    for method in dir(thing):
        if callable(getattr(thing, method)):
            print(method)