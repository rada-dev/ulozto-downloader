import urwid as uw


class UldDetailView(uw.WidgetWrap):

    def __init__(self, n_lines, print_part_info_queue):
        self.text = uw.Text("")
        self.lines = [""]*n_lines
        self.print_part_info_queue = print_part_info_queue
        super(UldDetailView, self).__init__(self.text)

    def write_line(self, i, line):
        self.lines[i] = line
        self.text.set_text("\n".join(self.lines))
