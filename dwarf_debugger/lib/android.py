import os
import subprocess
from dwarf_debugger.lib import utils, external_tools


class AndroidPackage(object):
    def __init__(self):
        self.path = ''
        self.package = ''


class AndroidDecompileUtil(object):
    @staticmethod
    def decompile(adb, apk_path):
        if not os.path.exists('.decompile'):
            os.mkdir('.decompile')
        adb.su_cmd('cp ' + apk_path + ' /sdcard/dwarf-decompile.apk')
        adb.pull('/sdcard/dwarf-decompile.apk', '.decompile/base.apk')
        adb.su_cmd('rm /sdcard/dwarf-decompile.apk')

        utils.do_shell_command('java -version')

        try:
            if os.name == 'nt':
                utils.do_shell_command(
                    'jadx-gui.bat .decompile/base.apk &')
            else:
                utils.do_shell_command(
                    'jadx-gui.sh .decompile/base.apk &')
        except:
            pass
