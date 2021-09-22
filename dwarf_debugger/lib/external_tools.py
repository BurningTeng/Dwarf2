import os

import urllib.request


def tool_exist(tool):
    if not os.path.exists('tools'):
        os.mkdir('tools')
        return False
    return os.path.exists('tools/%s' % tool)


def get_tool(url, path):
    if not os.path.exists('tools'):
        os.mkdir('tools')

    urllib.request.urlretrieve(url, 'tools/%s' % path)
