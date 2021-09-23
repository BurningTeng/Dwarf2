import json
import os

from PyQt5.QtCore import QObject, pyqtSignal


VIEW_BACKTRACE = 'view_backtrace'
VIEW_CONTEXT = 'view_context'
VIEW_BREAKPOINTS = 'view_breakpoints'
VIEW_WATCHERS = 'view_watchpoints'


class Prefs(QObject):
    """ Preferences

        json settings '.dwarf'

        signals:
            settingChanged(key, value)
            prefsChanged()
    """

    prefsChanged = pyqtSignal(name='prefsChanged')

    def __init__(self):
        super().__init__()

        from pathlib import Path
        home_path = str(Path.home()) + os.sep + '.dwarf' + os.sep

        self._prefs = {}
        self._prefs_file = home_path + 'preferences.json'

        if os.path.exists(self._prefs_file):
            with open(self._prefs_file, 'r') as f:
                try:
                    self._prefs = json.load(f)
                except:
                    pass

    def get(self, key, default=None):
        """ Get Setting

            key - setting name
            default
        """
        if key in self._prefs:
            return self._prefs[key]
        return default

    def put(self, key, value):
        """ Set Setting

            key - setting name
            value

            emits
                settingChanged(key, value)
                prefsChanged()
        """
        self._prefs[key] = value
        with open(self._prefs_file, 'w') as f:
            f.write(json.dumps(self._prefs))

        self.prefsChanged.emit()
