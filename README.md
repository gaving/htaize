# htaize

## issues

    C:\gavin\workspace\projects\htaize>python htaize.py -p localhost
    /c/DOCUME~1/5052661/LOCALS~1/Temp/tmprQDnvu.hta
    /c/DOCUME~1/5052661/LOCALS~1/Temp/tmprQDnvu.hta: line 1: syntax error near unexpected token `newline'
    /c/DOCUME~1/5052661/LOCALS~1/Temp/tmprQDnvu.hta: line 1: `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'

    Path issues executing from windows:-

    SET PATH="C:\Python26"
    PATH=
    echo %PATH%

## installation

    python setup.py py2exe --help
    python setup.py py2exe --help

    Note the bundle options in setup.py

# notes

    http://stackoverflow.com/questions/175994/can-i-embed-an-icon-to-a-hta-file
    copy /b icon.ico+source.hta iconapp.hta

    import subprocess
    subprocess.Popen([ 'mshta.exe', path ], stdin=open(os.devnull), stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT) 
