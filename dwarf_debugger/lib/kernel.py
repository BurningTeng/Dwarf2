class FTrace(object):
    STATE_NOT_TRACING = 0
    STATE_TRACING = 1
    STATE_PAUSED = 2

    def __init__(self, dwarf):
        self.dwarf = dwarf
        self.state = FTrace.STATE_NOT_TRACING

    def get_current_events(self):
        return self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.events()', True])

    def get_current_filters(self):
        return self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.filters()', True])

    def get_options(self):
        return self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.options(true)', True])

    def set_current_events(self, events):
        return self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setEvents(\'%s\')' % events, True])

    def set_current_filters(self, filters):
        return self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setFilters(\'%s\')' % filters, True])

    def set_option(self, option, enabled):
        en = 'true'
        if not enabled:
            en = 'false'
        return self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setOption(\'%s\', %s)' % (option, en), True])

    def start(self):
        if self.state == FTrace.STATE_NOT_TRACING:
            self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setCurrentTracer(\'nop\')', True])
            self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setCurrentTracer(\'function\')', True])
            self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.traceOwnPid()', True])
            self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setTracing(true)', True])
        elif self.state == FTrace.STATE_PAUSED:
            self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setTracing(true)', True])

        self.state = FTrace.STATE_TRACING

    def stop(self):
        if self.state == FTrace.STATE_TRACING or self.state == FTrace.STATE_PAUSED:
            self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setTracing(false)', True])

        self.state = FTrace.STATE_NOT_TRACING

    def pause(self):
        if self.state == FTrace.STATE_TRACING:
            self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.setTracing(false)', True])

        self.state = FTrace.STATE_PAUSED

    def read_trace(self):
        return self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.readTrace()', True])

    def read_trace_async(self):
        self.dwarf.dwarf_api('evaluate', ['kernel.ftrace.readTraceAsync()', True])


class Kernel(object):
    def __init__(self, dwarf):
        self.dwarf = dwarf
        self.ftrace = FTrace(dwarf)

    def is_available(self):
        ret = self.dwarf.dwarf_api('evaluate', ['kernel.available()', True])
        if ret is not None:
            return ret.startswith('a')
        return False

    def lookup_symbol(self, symbol):
        return self.dwarf.dwarf_api('evaluate', ['kernel.lookupSymbol(\'%s\')' % symbol, True])

    def get_ftrace(self):
        return self.ftrace
