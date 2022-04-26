import urwid as uw
try:
    import list_item
except ImportError:
    from . import list_item


class UldListView(uw.WidgetWrap):

    def __init__(self):
        uw.register_signal(self.__class__, ['show_details'])
        self.walker = uw.SimpleFocusListWalker([])
        self.lb = uw.ListBox(self.walker)
        super(UldListView, self).__init__(self.lb)

    def modified(self):
        focus_w, _ = self.walker.get_focus()
        uw.emit_signal(self, 'show_details', focus_w.data)

    def create_total_list_item(self):
        return list_item.ListItem(0, {"name": "Total"}, "footer", "country_selected")

    def AddLink(self, link):
        i = len(self.walker)
        attr = f"country{i % 2}"
        data = {"name": link, "pop": "325,084,756", "gdp": "$ 19.485 trillion"}
        w = list_item.ListItem(i, data, attr, "country_selected")
        self.walker.append(w)

    def set_data(self, countries):
        countries_widgets = []
        for i, c in enumerate(countries):
            attr = f"country{i % 2}"
            countries_widgets.append(list_item.ListItem(i, c, attr, "country_selected"))

        uw.disconnect_signal(self.walker, 'modified', self.modified)

        while len(self.walker) > 0:
            self.walker.pop()
        self.walker.extend(countries_widgets)
        uw.connect_signal(self.walker, "modified", self.modified)
        self.walker.set_focus(0)
