import urwid as uw
try:
    import detail_item
except ImportError:
    from . import detail_item


class UldDetailView(uw.WidgetWrap):

    def __init__(self, n_parts, print_part_info_queue):
        uw.register_signal(self.__class__, ['update'])
        self.n_parts = n_parts
        self.items = {}
        self.walker = uw.SimpleFocusListWalker([])
        self.lb = uw.ListBox(self.walker)
        self.print_part_info_queue = print_part_info_queue
        super(UldDetailView, self).__init__(self.lb)

    def create_items(self):
        items = [
            detail_item.SimpleItem("Filename:", "filename", "item0", "item_selected"),
            detail_item.SimpleItem("Url:", "url", "item1", "item_selected"),
            detail_item.SimpleItem("Download Type:", "captcha protected", "item0", "item_selected"),
            detail_item.SimpleItem("File Parts:", f"{self.n_parts}x{100} MB", "item1", "item_selected"),
        ]
        i_start = len(self.items)
        for i in range(self.n_parts):
            items.append(detail_item.PartItem(i, f"item{(i_start+i)%2}", "item_selected"))
        self.walker.extend(items)

    def update(self, item_caption, item_column, value):
        for it in self.walker:
            if item_caption == it.caption.rstrip(":").lower():
                it.set_value(item_column, value)

    def added_item(self, i, data):
        if len(self.walker) == 0:
            self.create_items()
            self.show_details(data)

    def show_details(self, data):
        self.update("filename", "text", data.filename)
        self.update("url", "text", data.url)
