#!/usr/bin/python
# import os
import argparse
import configparser
import os
import sys
from .memo import Memo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="edit the config file", action='store_true')
    parser.add_argument('-l', '--list', help="list all memos", action='store_true')
    parser.add_argument('-s', '--show', help="show memos, default behavior", action='store_true')
    parser.add_argument('-a', '--add', help="add new memo", action='store_true')
    args = parser.parse_args()

    config_path = os.path.join(sys.prefix, 'memo', 'data', 'memo.conf')
    config = configparser.ConfigParser()
    config.read(config_path)

    if args.config:
        os.system('vim %s' % (config_path))
    else:
        memo = Memo(config)
        if args.list:
            memo.list()
        elif args.add:
            memo.add()
        else:
            memo.show()

if __name__ == '__main__':
    main()

