#!/usr/bin/python
import sys
import os
import npyscreen
import curses
import time


class ListButton(npyscreen.ButtonPress):
    """
    override the __init__ and update functions to change apperance.
    override the whenPressed function to control behavior.
    """

    def __init__(self, screen, name='Button', memo_path=None, cursor_color=None, *args, **keywords):
        super(ListButton, self).__init__(screen, name=name, cursor_color=None, *args, **keywords)
        self.cursor_color = "CURSOR_INVERSE"
        self.color = "CURSOR_COLOR"
        self.date_color = "LABEL"
        self.cursor_date = "CURSOR_INVERSE"
        self.memo_path = memo_path

    def update(self, clear=True):
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False

        if self.editing:
            button_state = curses.A_STANDOUT
        else:
            button_state = curses.A_NORMAL

        button_name = self.name
        if isinstance(button_name, bytes):
            button_name = button_name.decode(self.encoding, 'replace')
        button_name = button_name.center(self.label_width)

        if self.do_colors():
            if self.cursor_color:
                if self.editing:
                    button_attributes = self.parent.theme_manager.findPair(self, self.cursor_color)
                else:
                    button_attributes  = self.parent.theme_manager.findPair(self, self.color)
            else:
                button_attributes = self.parent.theme_manager.findPair(self, self.color) | button_state
        else:
            button_attributes = button_state

        if self.do_colors():
            if self.editing:
                date_attributes = self.parent.theme_manager.findPair(self, self.cursor_date)
            else:
                date_attributes  = self.parent.theme_manager.findPair(self, self.date_color)
        else:
            button_attributes = button_state

        date = button_name.split('\t')[0] + '\t'
        file_name = button_name.split('\t')[1]

        self.add_line(self.rely, self.relx+1,
            date,
            self.make_attributes_list(date, date_attributes),
            len(date)
            )
        self.add_line(self.rely, self.relx+1+len(date),
            file_name,
            self.make_attributes_list(file_name, button_attributes),
            len(file_name)
            )

    def whenPressed(self):
        f = self.name.split('\t')[1]
        m_path = os.path.join(self.memo_path, f)
        os.system("vim %s" % m_path)
        sys.exit(0)


class ListForm(npyscreen.FormMultiPage):
    """
    List form page
    """

    def create(self):
        self.file_list = self.parentApp.file_list
        self.memo_path = self.parentApp.memo_path

        for f, d in self.file_list:
            display = str(d) + '\t' + f
            self.add_widget_intelligent(ListButton, name=display, memo_path=self.memo_path, value=display)

        self.add_handlers({
            "q": self.exit_editing,
            "Q": self.exit_editing
        })

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class ListUI(npyscreen.NPSAppManaged):
    """
    UI for memo list
    """
    def __init__(self, config):
        super(ListUI, self).__init__()
        self.memo_path = config.get('memo', 'memo_path')
        memo_files = os.listdir(self.memo_path)
        file_list = []
        for memo_file in memo_files:
            mdate = os.path.getmtime(os.path.join(self.memo_path, memo_file))
            t = time.localtime(mdate)
            file_list.append((memo_file, "%02d-%02d-%02d %02d:%02d:%02d" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)))
        file_list.sort(key=lambda x: x[1], reverse=True)

        self.file_list = file_list

    def onStart(self):
        self.addForm("MAIN", ListForm, name="Memo List")
