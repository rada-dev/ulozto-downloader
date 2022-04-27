import urwid as uw
try:
    import detail_item
except ImportError:
    from . import detail_item


class UldDetailView(uw.WidgetWrap):

    def __init__(self, n_parts, print_part_info_queue):

        self.n_parts = n_parts
        self.walker = uw.SimpleFocusListWalker([])
        self.lb = uw.ListBox(self.walker)
        self.print_part_info_queue = print_part_info_queue
        super(UldDetailView, self).__init__(self.lb)
        self.create_items()

    def create_items(self):
        items = [
            detail_item.SimpleItem("Filename:", "filename", "item0", "item_selected"),
        ]
        self.walker.extend(items)

    def write_line(self, i, line):
        self.lines[i] = line
        self.text.set_text("\n".join(self.lines))
