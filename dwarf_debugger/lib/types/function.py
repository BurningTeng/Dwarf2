class Function:
    def __init__(self, symbol, exported=False):
        self.name = symbol['name']
        self.address = symbol['address']

        self.exported = exported
