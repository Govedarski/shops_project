def execute_access_validators(*validators):
    def decorated_function(func):
        def wrapper(self, *args, **kwargs):
            for validator in validators:
                validator.validate(self, *args, **kwargs)
            return func(self, *args, **kwargs)

        return wrapper

    return decorated_function
