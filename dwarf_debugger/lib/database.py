class Database:
    """ DwarfDatabase
    """

    def __init__(self):
        super().__init__()
        self.modules_info = {}

    def get_module_info(self, address):
        address = self.sanify_address(address)
        if address:
            try:
                address = int(address, 16)
            except ValueError:
                return None

            for module_info in self.modules_info:
                _module = self.modules_info[module_info]
                if _module:
                    if _module.base <= address <= _module.base + _module.size:
                        return _module

        return None

    def put_module_info(self, address, module_info):
        address = self.sanify_address(address)
        self.modules_info[address] = module_info
        return module_info

    @staticmethod
    def sanify_address(address):
        hex_adr = address
        if isinstance(hex_adr, int):
            hex_adr = hex(hex_adr)
        return hex_adr.lower()
