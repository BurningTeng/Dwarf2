import sys
from dwarf_debugger.trace import main

if __name__ == '__main__':
    if sys.version_info.major < 3:
        exit('Python3 required!')

    main()
