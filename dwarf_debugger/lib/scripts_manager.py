from PyQt5.QtCore import QObject, pyqtSignal
from dwarf_debugger.lib.git import Git


class ScriptsManager(QObject):
    """ ScriptManager

        signals:
            scriptsUpdated()
    """

    scriptsUpdated = pyqtSignal(name='scriptsUpdated')

    def __init__(self):
        super(ScriptsManager, self).__init__()
        self._git = Git()
        self.scripts = {}

        self.update_scripts()

    def _check_version(self, required_dwarf):
        from dwarf_debugger.version import DWARF_VERSION
        required_dwarf = required_dwarf.split('.')
        dwarf_version = DWARF_VERSION.split('.')
        print(required_dwarf)
        if int(dwarf_version[0]) < int(required_dwarf[0]):
            return False
        elif (int(dwarf_version[0]) <= int(required_dwarf[0])) and (
                int(dwarf_version[1]) < int(required_dwarf[1])):
            return False
        elif (int(dwarf_version[1]) <= int(required_dwarf[1])) and (
                int(dwarf_version[2]) < int(required_dwarf[2])):
            return False

        return True

    def update_scripts(self):
        scripts = self._git.get_dwarf_scripts()

        if scripts is None:
            return

        scripts = scripts.replace(' ', '').replace('\t', '').split('\n')
        submodule_path = '[submodule"'
        url_path = 'url='
        module_name = ''

        for line in scripts:
            if line.startswith(submodule_path):
                module_name = line.replace(submodule_path, "")
                module_name = module_name[:-2]
            elif line.startswith(url_path):
                url = line.replace(url_path, "")
                if url.endswith('.git'):
                    url = url[:-4]
                url = url.replace('https://github.com',
                                  'https://raw.githubusercontent.com')

                info_url = url + '/master/dwarf.json'
                script_url = url + '/master/script.js'
                info = self._git.get_script_info(info_url)
                if info is None:
                    continue
                if 'dwarf' in info:
                    if not self._check_version(info['dwarf']):
                        continue
                self.scripts[module_name] = {
                    'info': info,
                    'script': script_url
                }

        self.scriptsUpdated.emit()

    def get_script(self, script_name):
        return self.scripts[script_name]

    def get_scripts(self):
        return self.scripts
