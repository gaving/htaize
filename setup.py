from distutils.core import setup
import py2exe

setup(windows = [{"script":"htl.py"}],
    name = "Launch HTA",
    zipfile = None,
    options = {
        "py2exe": {
            "compressed" : 1,
            "dll_excludes": ["w9xpopen.exe"],
            "bundle_files": 3
        }
    },
)
