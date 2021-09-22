import sys
from dwarf_debugger.dwarf import run_dwarf

if __name__ == '__main__':
    if sys.version_info.major < 3:
        exit('Python3 required!')

    run_dwarf()
