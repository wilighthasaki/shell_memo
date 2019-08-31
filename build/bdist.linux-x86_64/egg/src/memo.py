#!/usr/bin/python
import os
from .util import get_size
import time
from .list_ui import ListUI
from .show_ui import ShowUI


class Memo(object):
    def __init__(self, config):
        self.memo_path = config.get('memo', 'memo_path')

    def add(self):
        title = input("Please enter a title:")
        title = title.replace(' ', '_').replace('\t', '_')
        file_path = os.path.join(self.memo_path, title)
        os.mknod(file_path)
        os.system("vim %s" % file_path)

    def list(self):
        lui = ListUI(self.memo_path)
        lui.run()

    def show(self):
        sui = ShowUI(self.memo_path)
        sui.run()
