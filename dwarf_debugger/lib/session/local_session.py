import frida

from dwarf_debugger.lib.session.session import Session


class LocalSession(Session):

    def __init__(self, app_window):
        super(LocalSession, self).__init__(app_window)

    @property
    def session_type(self):
        """ return session name to show in menus etc
        """
        return 'local'

    @property
    def device_manager_type(self):
        return 'local'

    @property
    def frida_device(self):
        return frida.get_local_device()
