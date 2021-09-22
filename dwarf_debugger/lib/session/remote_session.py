import frida

from dwarf_debugger.lib.session.session import Session


class RemoteSession(Session):

    def __init__(self, app_window):
        super(RemoteSession, self).__init__(app_window)

    @property
    def session_type(self):
        """ return session name to show in menus etc
        """
        return 'remote'

    @property
    def device_manager_type(self):
        return 'remote'

    @property
    def frida_device(self):
        return frida.get_remote_device()
