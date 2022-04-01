#!/usr/bin/env python

import os, sys, getpass

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def help():
    eprint('''Generate nginx and systemd files for OHCA API
Usage: ./generate.py <nginx/systemd/help> [<user> <group>]
   nginx    Generate nginx config to be installed in
            nginx/sites-enabled
   systemd  Generate systemd service file to be installed
            in systemd/system
   help     Show this help text

The script must be run from the OHCA API root directory.
''')
    sys.exit(2)

def nginx():
    server = ' '.join(list(map(str.strip, os.getenv('ALLOWED_HOSTS', '*').split(','))))
    if server == '*':
        server = '_'
    with sys.stdout as f:
        f.write('# OHCA API Server config\n')
        f.write('server {\n')
        f.write('        listen 80;\n')
        f.write('        server_name ' + server + ';\n')
        f.write('\n')
        f.write('        location / {\n')
        f.write('                include proxy_params;\n')
        f.write('                proxy_pass http://unix:' + str(os.getcwd()) + '/ohca.sock;\n')
        f.write('        }\n')
        f.write('\n')
        f.write('        location /static/ {\n')
        f.write('                root ' + str(os.getcwd()) + '/ohca;\n')
        f.write('        }\n')
        f.write('}\n')

def systemd(user):
    with sys.stdout as f:
        f.write('[Unit]\n')
        f.write('Description=OHCA Django API Server\n')
        f.write('After=network.target\n')
        f.write('\n')
        f.write('[Service]\n')
        f.write('User=' + getpass.getuser() + '\n')
        f.write('Group=' + getpass.getuser() + '\n')
        f.write('WorkingDirectory=' + str(os.getcwd()) + '\n')
        f.write('Environment="PATH=' + str(os.getcwd()) + '/.venv/bin"\n')
        f.write('EnvironmentFile=' + str(os.getcwd()) + '/.env\n')
        f.write('ExecStart=' + str(os.getcwd()) + '/.venv/bin/gunicorn --workers 3 --bind unix:ohca.sock -m 007 ohca.wsgi\n')
        f.write('\n')
        f.write('[Install]\n')
        f.write('WantedBy=multi-user.target\n')

def main(argv):
    try:
        if len(argv) > 3 or len(argv) == 0:
            help()
        if not(os.path.exists('manage.py') and os.path.isfile('manage.py')):
            eprint('Please run this script from the root directory of the OHCA API!')
            sys.exit(3)
        if str(argv[0]).casefold() == "nginx".casefold() and len(argv) == 1:
            nginx()
        elif str(argv[0]).casefold() == "systemd".casefold():
            if len(argv) == 1:
                systemd(getpass.getuser(), getpass.getuser())
            elif len(argv) == 2:
                systemd(argv[1], argv[1])
            elif len(argv) == 3:
                systemd(argv[1], argv[2])
        else:
            help()
    except:
        help()

if __name__ == '__main__':
    main(sys.argv[1:])