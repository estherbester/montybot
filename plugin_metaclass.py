# meta class for singletons


# thanks http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class PluginMetaClass(type):
    """ This is for making each plugin a singleton.
     We need to make sure both the plugin and the logger are singletons. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(PluginMetaClass, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
