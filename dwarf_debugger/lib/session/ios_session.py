import frida
from PyQt5.QtWidgets import QMenu, QAction

from dwarf_debugger.lib.session.session import Session
from dwarf_debugger.lib import utils


class IosSession(Session):

    @staticmethod
    def _is_frida_running():
        # untested
        utils.do_shell_command('ssh -p2222 mobile@127.0.0.1 ps -A | grep \'frida\'')

    def __init__(self, app_window):
        super(IosSession, self).__init__(app_window)

    @property
    def session_type(self):
        """ return session name to show in menus etc
        """
        return 'ios'

    @property
    def device_manager_type(self):
        return 'ios'

    @property
    def frida_device(self):
        return frida.get_usb_device()

    def _setup_menu(self):
        """ Build Menus
        """
        super()._setup_menu()

        obcj_menu = QMenu('&ObjC')
        obcj_menu.addAction('Inspector', self._on_objc_modules)
        self._menu.append(obcj_menu)

    def _on_proc_selected(self, data):
        super()._on_proc_selected(data)

    def _on_spawn_selected(self, data):
        device, package_name, break_at_start = data
        if device:
            self.dwarf.device = device
        if package_name:
            try:
                self.dwarf.spawn(package_name, break_at_start=break_at_start)
            except Exception as e:
                utils.show_message_box('Failed spawning {0}'.format(package_name), str(e))
                self.stop()
                return

            self._on_objc_modules()

    def _on_objc_modules(self):
        self._app_window.show_main_tab('objc-inspector')
        self.dwarf.dwarf_api('enumerateObjCModules')

