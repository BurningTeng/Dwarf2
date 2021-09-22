BREAKPOINT_NATIVE = 0
BREAKPOINT_JAVA = 1
BREAKPOINT_INITIALIZATION = 2
BREAKPOINT_OBJC = 3


class Breakpoint(object):
    def __init__(self, breakpoint_type):
        self.breakpoint_type = breakpoint_type
        self.target = None
        self.condition = ''
        self.debug_symbol = None

    def set_condition(self, condition):
        self.condition = condition

    def set_debug_symbol(self, symbol):
        self.debug_symbol = symbol

    def set_target(self, target):
        self.target = target

    def get_condition(self):
        return self.condition

    def get_target(self):
        return self.target

    def to_json(self):
        return {
            'target': self.target,
            'condition': self.condition,
            'debug_symbol': self.debug_symbol
        }
