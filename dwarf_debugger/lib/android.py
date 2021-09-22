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
        dex2jar = 'd2j-dex2jar.sh'
        if os.name == 'nt':
            dex2jar = 'd2j-dex2jar.bat'
        try:
            utils.do_shell_command(dex2jar).index('version')
        except:
            utils.show_message_box('failed to find %s' % dex2jar)
            return
        utils.do_shell_command(
            dex2jar + ' .decompile/base.apk -o .decompile/base.jar -f')
        if not external_tools.tool_exist('luyten.jar'):
            if os.name == 'nt':
                external_tools.get_tool(
                    'https://github.com/deathmarine/Luyten/releases/download/v0.5.4_Rebuilt_with_Latest_depenencies/luyten-0.5.4.exe',
                    'luyten.exe')
            else:
                external_tools.get_tool(
                    'https://github.com/deathmarine/Luyten/releases/download/v0.5.4_Rebuilt_with_Latest_depenencies/luyten-0.5.4.jar',
                    'luyten.jar')
        java_version = utils.do_shell_command('java -version')

        try:
            if os.name == 'nt':
                utils.do_shell_command(
                    'tools/luyten.exe .decompile/base.jar &')
            else:
                utils.do_shell_command(
                    'java -jar tools/luyten.jar .decompile/base.jar &')
        except:
            pass

