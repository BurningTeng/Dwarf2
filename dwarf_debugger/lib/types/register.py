class Register(object):
    def __init__(self, register_name, register_data):
        self.name = register_name
        self.value = int(register_data['value'], 16)
        self.is_pointer = register_data['isValidPointer']

        self.telescope_type = -1
        self.telescope_value = None

        self.symbol_name = None
        self.symbol_module_name = None

        self.instruction_size = 0
        self.instruction_groups = []
        self.thumb = False

        if self.is_pointer:
            self.telescope_type = register_data['telescope'][0]
            self.telescope_value = register_data['telescope'][1]
            if self.telescope_type > 0:
                self.telescope_value = int(self.telescope_value, 16)

        if 'symbol' in register_data:
            self.symbol_name = register_data['symbol']['name']
            self.symbol_module_name = register_data['symbol']['moduleName']

        if 'instruction' in register_data:
            self.instruction_size = register_data['instruction']['size']
            self.instruction_groups = register_data['instruction']['groups']
            self.thumb = register_data['instruction']['thumb']
