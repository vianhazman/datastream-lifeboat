import importlib
def __getclass__(type, class_name):
    """
    Method to get the desired transformation and client plugin
    :param type: transformers/clients
    :param class_name: the target plugin file and class
    :return: the plugin instance
    """
    module = importlib.import_module("{}.{}".format(type, class_name))
    instance = getattr(module, class_name)
    return instance
