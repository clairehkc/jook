#!c:\Users\Claire\Documents\dev\jukebox\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'gunicorn==18.0','console_scripts','gunicorn'
__requires__ = 'gunicorn==18.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('gunicorn==18.0', 'console_scripts', 'gunicorn')()
    )
