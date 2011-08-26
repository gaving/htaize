#! /usr/bin/env python

"""
Usage: htaize.py [options]

Launch a URI in a HTA

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PATH, --path=PATH  path to launch
  -t TITLE, --title=TITLE
                        title of hta
  -q QUERY, --query=QUERY
                        parse hta:// protocol

  Icon Options:
    -i ICON, --icon=ICON
                        icon URI of hta
    -I BUNDLE_ICON, --bundle-icon=BUNDLE_ICON
                        bundle icon.ico to the hta

  Output Options:
    -o OUTPUT, --output=OUTPUT
                        output directory
    -L, --launch        open the HTA
"""

import sys, tempfile, shutil, os
from string import Template
from optparse import OptionParser, OptionGroup

options = {}
DEFAULTS = {
    'title': 'HTA',
    'icon': 'migpwd.exe',
    'bundle_icon': None
}

def main():

    parser = OptionParser(usage="%prog [options]", version="0.2", description="Launch a URI in a HTA")

    parser.add_option('-p', '--path', dest='path', help='path to launch', action="store")
    parser.add_option('-t', '--title', dest='title', help='title of hta', action="store")
    parser.add_option('-q', '--query', dest='query', help='parse hta:// protocol', action="store")

    group = OptionGroup(parser, "Icon Options")
    group.add_option('-i', '--icon', dest='icon', help='icon URI of hta', action="store")
    group.add_option('-I', '--bundle-icon', dest='bundle_icon', help='bundle icon.ico to the hta', action="store")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Output Options")
    group.add_option('-o', '--output', dest='output', help='output directory', action="store")
    group.add_option('-L', '--launch', dest='launch', help='open the HTA', action="store_true")
    parser.add_option_group(group)

    parser.set_defaults(**DEFAULTS)
    (option_obj, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    options['path'] = option_obj.path
    options['title'] = option_obj.title
    options['icon'] = option_obj.icon
    options['query'] = option_obj.query
    options['launch'] = option_obj.launch
    options['output'] = option_obj.output
    options['bundle_icon'] = option_obj.bundle_icon

    params = {}

    if options['path']:
        path = options['path']

        params = {
            'name' : options['title'],
            'icon' : options['icon'],
            'url' : options['path']
        }

    elif options['query']:
        import urlparse, cgi

        path = options['query'].replace('hta', 'http')
        qs = cgi.parse_qs(urlparse.urlsplit(path).query)
        options['launch'] = True # Implied Launch of query strings

        try:
            title = qs['title'][0]
        except KeyError:
            title = DEFAULTS['title']

        try:
            icon = qs['icon'][0]
        except KeyError:
            icon = DEFAULTS['icon']

        params = {
            'name' : title,
            'icon' : icon,
            'url' : path
        }

    if not params:
        print "no parameters to write"
        return

    try:

        if options['output']:
            temp = os.open(options['output'], os.O_CREAT | os.O_WRONLY)
            path = options['output']
        else:
            temp, path = tempfile.mkstemp(suffix='.hta')

        if not options['bundle_icon']:
            html = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
    <head>
        <hta:application id="smartmain" sysMenu="yes" applicationName="${name}"
        scroll="no" windowstate="maximize" maximizeButton="yes"
        singleInstance="no" caption="yes" border="thick" borderStyle="raised"
        icon="${icon}"
        navigable="yes">
        <title>${name}</title>
    </head>
    <frameset>
        <frame scrolling="yes" application="yes" trusted="yes" src="${url}"></frame>
    </frameset>
</html>
            """
        else:
            html = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
    <head>
        <title>${name}</title>
        <script type="text/javascript">
            document.write('<hta:application id="smartmain" sysMenu="yes" applicationName="${name}" scroll="no" windowstate="maximize" maximizeButton="yes" singleInstance="no" caption="yes" border="thick" borderStyle="raised" icon="'+document.URL+'" navigable="yes">');
        </script>
    </head>
    <frameset>
        <frame scrolling="yes" application="yes" trusted="yes" src="${url}"></frame>
    </frameset>
</html>
        """

        template = Template(html).substitute(params);

        if options['bundle_icon']:
            # Prepend the icon binary to the HTA file
            icon = open(options['bundle_icon'], 'rb').read()
            os.write(temp, icon + template)
        else:
            os.write(temp, template)

    finally:
        os.close(temp)

    print "Saved to %s" % path
    if options['launch']:
        # os.system(path + '&')
        import subprocess
        subprocess.Popen([ 'mshta.exe', path ])

if __name__=="__main__":
    main()
