import sys
import os
import inspect
import importlib.util

from dwarf_debugger.lib.utils import home_path


class PluginManager:
    def __init__(self, app):
        self._app = app
        self._plugins_path = os.path.join(home_path(), 'plugins')
        sys.path.append(self._plugins_path)

        self._plugins = {}

    @property
    def plugins(self):
        return self._plugins

    def reload_plugins(self):
        for _, directories, _ in os.walk(self._plugins_path):
            for directory in [x for x in directories if x != '__pycache__']:
                plugin_dir = os.path.join(self._plugins_path, directory)
                if self._app is None:
                    plugin_file = os.path.join(plugin_dir, 'injector_plugin.py')
                else:
                    plugin_file = os.path.join(plugin_dir, 'plugin.py')

                if plugin_file and os.path.exists(plugin_file):
                    spec = importlib.util.spec_from_file_location('', location=plugin_file)

                    if not spec:
                        continue

                    try:
                        _plugin = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(_plugin)
                    except Exception as e:  # pylint: disable=broad-except, invalid-name
                        print('failed to load plugin %s: %s' % (plugin_file, str(e)))
                        return

                    _classes = inspect.getmembers(_plugin, predicate=inspect.isclass)
                    for _, _class in _classes:
                        if inspect.isclass(_class) and not inspect.isabstract(_class):

                            if _class.__name__ != 'Plugin':
                                continue

                            _has_required_funcs = False
                            _funcs = inspect.getmembers(_class, predicate=inspect.isfunction)

                            for function_name, _ in _funcs:
                                if function_name == '__get_plugin_info__':
                                    _has_required_funcs = True
                                    break

                            if _has_required_funcs:
                                try:
                                    if self._app is not None:
                                        _instance = _class(self._app)
                                    else:
                                        _instance = _class()
                                    plugin_info = _instance.__get_plugin_info__()
                                    if 'name' not in plugin_info:
                                        print(
                                            'failed to load plugin "%s": '
                                            'missing name in __get_plugin_info__' % plugin_file)
                                        continue
                                    _instance.name = plugin_info['name']
                                    self._plugins[_instance.name] = _instance
                                    break
                                except Exception as e:  # pylint: disable=broad-except, invalid-name
                                    print('failed to load plugin %s: %s' % (plugin_file, str(e)))
                            else:
                                print('failed to load plugin "%s": missing __get_plugin_info__ method' % plugin_file)
