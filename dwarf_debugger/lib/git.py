import hashlib
import json
import os
import time

import requests

from dwarf_debugger.lib import utils


class Git(object):
    CACHE_PATH = '.git_cache'
    DWARF_CACHE = CACHE_PATH + '/dwarf'
    DWARF_COMMITS_CACHE = CACHE_PATH + '/dwarf_commits'
    DWARF_SCRIPTS_CACHE = CACHE_PATH + '/dwarf_scripts'
    FRIDA_CACHE = CACHE_PATH + '/frida'

    def __init__(self):
        if not os.path.exists(Git.CACHE_PATH):
            os.mkdir(Git.CACHE_PATH)

    def _open_cache(self, path, url, _json=True):
        data = None
        now = time.time()
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                last_update = data['updated']
                data = data['data']
                if now - last_update < 60 * 15:
                    return data
        if utils.is_connected():
            try:
                r = requests.get(url)
            except:
                return data
            if r is None or r.status_code != 200:
                return data
            if _json:
                try:
                    data = r.json()
                except:
                    return None
            else:
                data = r.text
            with open(path, 'w') as f:
                f.write(json.dumps({
                    'updated': now,
                    'data': data
                }))
        return data

    def get_frida_version(self):
        return self._open_cache(
            Git.FRIDA_CACHE, 'https://api.github.com/repos/frida/frida/releases/latest')

    def get_script(self, url):
        return self._open_cache(
            Git.CACHE_PATH + '/' + hashlib.md5(url.encode('utf8')).hexdigest(), url, _json=False)

    def get_script_info(self, url):
        return self._open_cache(
            Git.CACHE_PATH + '/' + hashlib.md5(url.encode('utf8')).hexdigest(), url)
