import urwid as uw
try:
    import detail_view, list_view
except ImportError:
    from . import detail_view, list_view


class App(object):

    def unhandled_input(self, key):
        if key in ('q',):
            raise uw.ExitMainLoop()

    def show_details(self, country):
        self.detail_view.set_country(country)

    def show_summary(self, data):
        self.summary_view.set_country(data)

    def __init__(self):
        self.palette = {
            ("bg", "default", "default"),
            ("country0", "white", "default"),
            ("country1", "default", "default"),
            ("country_selected", "black", "dark cyan"),
            ("footer", "black", "dark cyan"),
            ("title", "default,bold", "default")
        }

        self.summary_view = detail_view.DetailView()
        self.list_view = list_view.ListView()
        self.detail_view = detail_view.DetailView()
        col_rows = uw.raw_display.Screen().get_cols_rows()
        h = col_rows[0] - 2
        f1 = uw.Filler(self.list_view, valign='top', height=h)
        f2 = uw.Filler(self.detail_view, valign='top')
        self.box_summary = uw.LineBox(self.summary_view, title="Summary", title_attr="title")
        self.box_list = uw.LineBox(f1, title="List of Files", title_attr="title")
        self.box_details = uw.LineBox(f2, title="File Details", title_attr="title")
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
        self.frame = uw.AttrMap(uw.Frame(header=self.box_summary, body=columns, footer=self.footer), 'bg')

        self.loop = uw.MainLoop(self.frame, self.palette, unhandled_input=self.unhandled_input)

    def update_data(self):
        l = []  # https://databank.worldbank.org/embed/Population-and-GDP-by-Country/id/29c4df41
        l.append({"name": "USAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "USAaaaaaaaaaaaaaaaaaaaaaaaaaaa", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})
        l.append({"name": "USA", "pop": "325,084,756", "gdp": "$ 19.485 trillion"})
        l.append({"name": "China", "pop": "1,421,021,791", "gdp": "$ 12.238 trillion"})
        l.append({"name": "Japan", "pop": "127,502,725", "gdp": "$ 4.872 trillion"})
        l.append({"name": "Germany", "pop": "82,658,409", "gdp": "$ 3.693 trillion"})
        l.append({"name": "India", "pop": "1,338,676,785", "gdp": "$ 2.651 trillion"})

        self.list_view.set_data(l)

    def start(self):
        self.update_data()
        try:
            self.loop.run()
        except KeyboardInterrupt:
            pass