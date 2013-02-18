"""
Call this like ``python create-venv-script.py``; it will refresh the bootscrap.py script
"""
import os

here = os.path.dirname(os.path.abspath(__file__))
#base_dir = os.path.dirname(here)
script_name = os.path.join(here, 'bootstrap.py')

#TODO download virtualenv.py here

import virtualenv

EXTRA_TEXT = """
import shutil

def extend_parser(parser):
    pass

def adjust_options(options, args):
    pass

def after_install(options, home_dir):
    base_dir = os.path.dirname(home_dir)

    # make etc directory
    etc = join(home_dir, 'etc')
    if not os.path.exists(etc):
        os.makedirs(etc)

    subprocess.call(['sudo', 'apt-get', 'install', 'libevent-dev'])
    subprocess.call([join(home_dir, 'bin', 'pip'), 'install', '-r', 'requirements.txt'])
"""

def main():
    text = virtualenv.create_bootstrap_script(EXTRA_TEXT, python_version='2.7')
    print 'Updating %s' % script_name
    f = open(script_name, 'w')
    f.write(text)
    f.close()

if __name__ == '__main__':
    main()
