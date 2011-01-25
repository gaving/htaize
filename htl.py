#! /usr/bin/env python

"""
Usage: htl.py [options]

Launch a HTA URL

Options:
  --version               show program's version number and exit
  -h, --help              show this help message and exit
  -p PATH, --path=PATH    path to launch
  -t TITLE, --title=TITLE title of hta
  -i ICON, --icon=ICON    icon of hta
  -q QUERY, --query=QUERY querystring
"""

import sys, tempfile, shutil, os

from string import Template
from optparse import OptionParser

options = {}
DEFAULTS = {
    'title': 'HTA',
    'icon': 'green.ico'
}

def main():

    parser = OptionParser(usage="%prog [options]", version="0.1", description="launch a hta process")
    parser.add_option('-p', '--path', dest='path', help='path to launch', action="store")
    parser.add_option('-t', '--title', dest='title', help='title of hta', action="store")
    parser.add_option('-i', '--icon', dest='icon', help='icon of hta', action="store")
    parser.add_option('-q', '--query', dest='query', help='query string', action="store")
    parser.set_defaults(**DEFAULTS)
    (option_obj, args) = parser.parse_args()

    options['path'] = option_obj.path
    options['title'] = option_obj.title
    options['icon'] = option_obj.icon
    options['query'] = option_obj.query

    if options['path']:
        path = options['path']

        params = {
            'name' : options['title'],
            'graphic' : options['icon'],
            'url' : options['path']
        }

    elif options['query']:
        import urlparse, cgi

        path = options['query'].replace('hta', 'http')
        qs = cgi.parse_qs(urlparse.urlsplit(path).query)

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
            'graphic' : icon,
            'url' : path
        }

    try:
        temp, path = tempfile.mkstemp(suffix='.hta')

        template = Template("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
    <head>
        <hta:application id='smartmain' sysMenu='yes' applicationName='${name}'
        scroll='no' windowstate='maximize' maximizeButton='yes'
        singleInstance='no' caption='yes' border='thick' borderStyle='raised'
        icon="http://tpscope/gg5052661/icons/${graphic}"
        navigable='yes'>
        <title>${name}</title>
    </head>
    <frameset>
        <frame scrolling='yes' application='yes' trusted='yes' src='${url}'></frame>
    </frameset>
</html>
    """)

        os.write(temp, template.substitute(params))

    finally:
        os.close(temp)

    os.system(path)

if __name__=="__main__":
    main()
