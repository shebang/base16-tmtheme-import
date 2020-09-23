#!/usr/bin/env python3
import sys
import os
import plistlib

def get_style(data, wanted_scope):
    for color_setting in data['settings']:
        scopes_raw = color_setting.get('scope')
        if scopes_raw:
            scopes = map(str.strip, scopes_raw.split(','))
            if wanted_scope in scopes:
                retval = color_setting.get('settings')
                if 'base16.reversed' in scopes:
                    retval['reversed'] = True
                else:
                    retval['reversed'] = False
                return color_setting.get('settings')
    return None

def create_yaml(data, out_filename):
    theme_name, _ = os.path.splitext(os.path.basename(out_filename))
    theme_name = theme_name.replace('-', ' ')
    f = open(out_filename, "w")
    f.write('scheme: ' + '\'' + theme_name + '\'\n')
    f.write('author: \'shebang\'\n\n')
    for color_id in range(20):
        color_name = 'base%02X'%(color_id)
        color_style = get_style(data, 'base16.'+color_name)
        if color_style:
            print('using %s=%s'%(color_name, color_style))
            color_key = 'foreground' if not color_style['reversed'] else 'background'
            f.write(color_name + ': ' + '\'' + color_style[color_key].strip('#') + '\'\n')
    f.close()


def process_file(file):
    out_filename, _ = os.path.splitext(file)
    out_filename = out_filename + '.yaml'
    with open(file, 'rb') as fp:
        data = plistlib.load(fp)
        create_yaml(data, out_filename)

def main(argv):
    process_file(argv[0])

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1:])
