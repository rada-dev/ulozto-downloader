import urwid as uw
try:
    import list_item
except ImportError:
    from . import list_item


class UldListView(uw.WidgetWrap):

    def __init__(self):
        uw.register_signal(self.__class__, ['show_details', 'added_item'])
        self.walker = uw.SimpleFocusListWalker([])
        self.lb = uw.ListBox(self.walker)
        uw.connect_signal(self.walker, "modified", self.modified)
        super(UldListView, self).__init__(self.lb)

    def modified(self):
        item, _ = self.walker.get_focus()
        uw.emit_signal(self, 'show_details', item.data)

    def create_total_list_item(self):
        return list_item.ListItem(0, {"name": "Total"}, "footer", "item_selected")

    def AddItem(self, data):
        i = len(self.walker)
        w = list_item.ListItem(i, data, f"item{i % 2}", "item_selected")
        self.walker.append(w)
        uw.emit_signal(self, "added_item", i, data)

    def set_data(self, countries):
        countries_widgets = []
        for i, c in enumerate(countries):
            attr = f"item{i % 2}"
            countries_widgets.append(list_item.ListItem(i, c, attr, "item_selected"))

        uw.disconnect_signal(self.walker, 'modified', self.modified)

        while len(self.walker) > 0:
            self.walker.pop()
        self.walker.extend(countries_widgets)
        uw.connect_signal(self.walker, "modified", self.modified)
        self.walker.set_focus(0)
