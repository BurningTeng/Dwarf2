class CpuRegister():
    __slots__ = ['name', 'description', 'value']

    def __init__(self, name, value, description=None):
        self.name = name
        self.value = value
        self.description = 'Register'
        if description:
            self.description = description
