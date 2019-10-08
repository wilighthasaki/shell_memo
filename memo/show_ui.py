#!/usr/bin/python
import sys
import os
import npyscreen
import curses
import time


class MemoPager(npyscreen.Pager):
    def __init__(self, screen, when_pressed_function=None, *args, **keywords):
        super(MemoPager, self).__init__(screen, *args, **keywords)
        self.highlight = False
        self.title_highlight = False
        self.title_color = "NO_EDIT"
        self.autowrap = True

    def setValuesWrap(self, lines):
        if self.autowrap and (lines == self._values_cache_for_wrapping):
            return False
        try:
            lines = lines.split('\n')
        except AttributeError:
            pass
        self.values = self._wrap_message_lines(lines, max(1, self.width))
        self._values_cache_for_wrapping = self.values

    def _wrap_message_lines(self, message_lines, line_length):
        """
        override this function to change wrap to cut up
        """
        lines = []
        if len(message_lines) < self.parent.row_height:
            for _ in range(self.parent.row_height - len(message_lines)):
                message_lines.append("")
        for line in message_lines:
            # calculate line length
            size = 0
            line_length_cur = line_length
            # Because of Chinese occur 2 space in a line, so we calculate
            # true line width below
            for ch in line:
                if len(ch.encode('utf8')) > 1:
                    size += 2
                    line_length_cur -= 1
                else:
                    size += 1
                if size >= line_length - 4:
                    break
            line += ' '.join(['' for _ in range(line_length - size - 2)])
            lines.append(line[: line_length_cur - 3])

        return lines

    def update(self, clear=True):
        """
        override this function to change memo preview apperance
        """
        #we look this up a lot. Let's have it here.
        if self.autowrap:
            self.setValuesWrap(list(self.values))

        if self.center:
            self.centerValues()

        display_length = len(self._my_widgets)
        values_len = len(self.values)

        if self.start_display_at > values_len - display_length:
            self.start_display_at = values_len - display_length
        if self.start_display_at < 0: self.start_display_at = 0

        indexer = 0 + self.start_display_at
        # do the first line
        line = self._my_widgets[0]
        self._print_first_line(line, indexer)
        indexer += 1

        for line in self._my_widgets[1:-1]:
            self._print_line(line, indexer)
            indexer += 1

        # Now do the final line
        line = self._my_widgets[-1]

        if values_len > indexer+1:
            line.value = "- more -"
            line.highlight = False
            # line.highlight = False
            # line.show_bold = False

        for w in self._my_widgets:
            # call update to avoid needless refreshes
            w.update(clear=True)
        # There is a bug somewhere that affects the first line.  This cures it.
        # Without this line, the first line inherits the color of the form when not editing. Not clear why.
        self._my_widgets[0].update()

    def _print_line(self, line, value_indexer):
        super(MemoPager, self)._print_line(line, value_indexer)
        if self.highlight:
            line.highlight = True
        else:
            line.highlight = False

    def _print_first_line(self, line, value_indexer):
        self._set_line_values(line, value_indexer)
        self._set_line_highlighting(line, value_indexer)
        line.color = self.title_color
        line.show_bold = True
        if self.highlight:
            line.highlight = True
        else:
            line.highlight = False


class MemoGrid(npyscreen.SimpleGrid):
    _contained_widgets = MemoPager

    def set_up_handlers(self):
        """
        add handlers to control
        """
        super(MemoGrid, self).set_up_handlers()
        self.handlers.update({
            ord("q"): self.parent.exit_editing,
            "Q": self.parent.exit_editing,
            "^Q": self.parent.exit_editing,
            curses.ascii.CR: self.open_memo,
            curses.ascii.NL: self.open_memo
        })

    def open_memo(self, input):
        """
        open the memo file with vim
        """
        file_name = self.values[self.edit_cell[0]][self.edit_cell[1]][0]
        file_path = os.path.join(self.parent.memo_path, file_name)
        os.system("vim %s" % file_path)
        sys.exit(0)

    def _cell_widget_show_value(self, cell, value):
        """
        override this function to change TextField.value to Pager.values.
        """
        cell.values = value

    def display_value(self, vl):
        """
        override this function to change string to list.
        """
        return vl


class ShowForm(npyscreen.FormMultiPage):
    """
    Show form page
    """

    def create(self):
        self.file_list = self.parentApp.file_list
        self.memo_path = self.parentApp.memo_path
        self.row_height = self.parentApp.row_height
        self.column_number = self.parentApp.column_number

        # add code to load all memos
        memo_values = []
        for memo_file, memo_date in self.file_list:
            memo_value = [memo_file]
            with open(os.path.join(self.memo_path, memo_file), 'r') as memo_input:
                line_num = 0
                for line in memo_input:
                    line_num += 1
                    memo_value.append(line.rstrip())
                    if line_num > self.row_height:
                        break
            memo_values.append(memo_value)

        # add memo messages to Grid object
        gd = self.add(MemoGrid, row_height=self.row_height)
        gd.default_column_number = self.column_number
        gd.values = []
        new_value_row = []
        for memo_value in memo_values:
            new_value_row.append(memo_value)
            if len(new_value_row) == self.column_number:
                gd.values.append(new_value_row)
                new_value_row = []
        gd.values.append(new_value_row)

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class ShowUI(npyscreen.NPSAppManaged):
    """
    UI for memo list
    """
    def __init__(self, config):
        super(ShowUI, self).__init__()
        self.memo_path = config.get('memo', 'memo_path', fallback=os.path.join(sys.prefix, 'memo', 'data', 'local'))
        self.row_height = int(config.get('memo', 'row_height'))
        self.column_number = int(config.get('memo', 'column_number'))

        # load memo file
        memo_files = os.listdir(self.memo_path)
        file_list = []
        for memo_file in memo_files:
            mdate = os.path.getmtime(os.path.join(self.memo_path, memo_file))
            t = time.localtime(mdate)
            file_list.append((memo_file, "%02d-%02d-%02d %02d:%02d:%02d" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)))
        file_list.sort(key=lambda x: x[1], reverse=True)

        self.file_list = file_list

    def onStart(self):
        self.addForm("MAIN", ShowForm, name="Memo Preview")
