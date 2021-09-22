from dwarf_debugger.lib.types.register import Register


class Context(object):
    def __init__(self, context):

        if 'pc' in context:
            self.is_native_context = True

            for register in context:
                if len(register) > 0 and register != 'toJSON':
                    self.__dict__[register] = Register(register, context[register])
        else:
            self.is_native_context = False
