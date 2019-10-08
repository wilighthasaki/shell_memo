#!/usr/bin/python
import os
import sys
import time
from .list_ui import ListUI
from .show_ui import ShowUI


class Memo(object):
    def __init__(self, config):
        self.config = config
        self.memo_path = config.get('memo', 'memo_path', fallback=os.path.join(sys.prefix, 'memo', 'data', 'local'))

    def add(self):
        title = input("Please enter a title:")
        title = title.replace(' ', '_').replace('\t', '_')
        file_path = os.path.join(self.memo_path, title)
        os.mknod(file_path)
        os.system("vim %s" % file_path)

    def list(self):
        lui = ListUI(self.config)
        lui.run()

    def show(self):
        sui = ShowUI(self.config)
        sui.run()
