import urwid as uw
try:
    import detail_view, list_view, popups
except ImportError:
    from . import detail_view, list_view, popups


class UldFrame(uw.Frame):
    palette = [
        ("bg", "default", "default"),
        ("country0", "white", "default"),
        ("country1", "default", "default"),
        ("country_selected", "white", "dark blue"),
        ("footer", "black", "dark cyan"),
        ("title", "default,bold", "default"),
        ('popup', 'white', 'dark blue'),
        ('popup_footer', 'black', 'dark green'),
        ('banner', 'black', 'light gray'),
        ('selectable', 'white', 'black'),
        ('focus', 'black', 'light gray')
    ]

    def __init__(self):
        self.loop = None
        self.summary_view = detail_view.UldDetailView()
        self.list_view = list_view.UldListView()
        self.detail_view = detail_view.UldDetailView()
        col_rows = uw.raw_display.Screen().get_cols_rows()
        h = col_rows[0] - 2
        f1 = uw.Filler(self.list_view, valign='top', height=h)
        f2 = uw.Filler(self.detail_view, valign='top')
        self.box_summary = uw.LineBox(self.summary_view, title="Summary", title_attr="title")
        self.box_list = uw.LineBox(f1, title="List of Files", title_attr="title")
        self.box_details = uw.LineBox(f2, title="File Details", title_attr="title")
        self.olay_add_link = popups.UldOverlay(self)
        self.footer = uw.AttrMap(
            uw.Text([
                ("key", "F1"), "Help",
                ("key", "F2"), "Pause",
                ("key", "F3"), "Resume",
                ("key", "F4"), "PauseAll",
                ("key", "F5"), "ResumeAll",
                ("key", "F6"), "AddLink",
                ("key", "F7"), "AddLinkFile",
                ("key", "F8"), "RemoveLink",
                ("key", "F9"), "RemoveFinished",
            ]), "footer")

        uw.connect_signal(self.list_view, 'show_details', self.show_details)
        uw.connect_signal(self.list_view, 'show_details', self.show_summary)

        columns = uw.Columns([('weight', 1, self.box_list), ('weight', 1, self.box_details)])

        super(UldFrame, self).__init__(header=self.box_summary, body=columns, footer=self.footer)

    def show_details(self, country):
        self.detail_view.set_country(country)

    def show_summary(self, data):
        self.summary_view.set_country(data)

    def update_data(self):
        l = []  # https://databank.worldbank.org/embed/Population-and-GDP-by-Country/id/29c4df41
        l.append({"name": "USAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "USAaaaaaaaaaaaaaaaaaaaaaaaaaaa", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        self.list_view.set_data(l)
        
    def keypress(self, size, key):
        if key == "f6":
            self.loop.widget = self.olay_add_link
        super(UldFrame, self).keypress(size, key)
