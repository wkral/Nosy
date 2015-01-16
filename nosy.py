# By Jeff Winkler, http://jeffwinkler.net
# Enhanced by William Kral

import fnmatch
import json
import os
import stat
import subprocess
import sys
import time

'''
Nosy
====

Nosy will watch your project's source folder and execute a command of your
choosing whenever a watched source file changes.


Config file precedence:
-----------------------

    `pwd`/.nosy
    ~/.nosy

JSON Config example:
--------------------

    { "exec": "nosetests",
      "watch": ["*.py", "*.html", "*.js"] }
'''


def load_config_file(config_path):
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except:
        sys.stderr.write("Error parsing json config files.\n")
        sys.exit(1)

    return {}


def load_config():
    ''' Load the configuration data based on the current working directory or
        the home folders default configurations '''

    config = {'exec': 'nosetests', 'watch': ['*.py']}

    config.update(load_config_file(os.path.expanduser("~/.nosy")))
    config.update(load_config_file('.nosy'))

    return config


def check_sum(config):
    ''' Stat all files matching the patterns in config['watch'] '''
    val = 0
    for root, dirs, files in os.walk(os.getcwd()):
        for extension in config['watch']:
            for f in fnmatch.filter(files, extension):
                stats = os.stat(os.path.join(root, f))
                val += stats[stat.ST_SIZE] + stats[stat.ST_MTIME]
    return val


def main():
    ''' Continuously run check_sum on path expressions in the config
        If there is a change in any of those files execute the test runner'''
    config = load_config()

    args = ' '.join(sys.argv[1:])
    command = '{0} {1}'.format(config['exec'], args)

    last_sum = 0
    try:
        while (True):
            new_sum = check_sum(config)
            if new_sum != last_sum:
                last_sum = new_sum
                subprocess.call(command, shell=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nGoodbye')

if __name__ == '__main__':
    main()
