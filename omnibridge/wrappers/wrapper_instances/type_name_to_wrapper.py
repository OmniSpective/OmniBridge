def register_wrapper(cls):
    type_names[cls.get_class_type_field()] = cls
    return cls


type_names = {}
