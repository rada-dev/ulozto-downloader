import time

import urwid as uw
import threading
try:
    import detail_view, list_view, popups
except ImportError:
    from . import detail_view, list_view, popups

from uldlib import page, downloader, torrunner


class UldFrame(uw.Frame):

    TARGET_DIR = ""
    PARTS = 10
    SIMUL = 5

    palette = [
        # ('bg', '#f00', '#f00', '#f00', '#f00', '#f00'),
        # ('orange', '', '', '', '', '#f80'),
        # ('yellow', '', '', '', '', '#ff0'),
        # ('green', '', '', '', '', '#0f0'),
        # ('blue', '', '', '', '', '#00f'),
        # ('purple_dark', '', '', '', '', '#508'),
        # ('purple_light', '', '', '', '', '#90f')

        # ('bg', '', '', '', '#aaa', '#000'),
        # ('title', '', '', '', '#aaa,bold', '#000'),
        # ('country0', '', '', '', 'white', 'default'),
        # ('country1', '', '', '', 'default', 'default'),
        # ('country_selected', '', '', '', 'black', '#f80'),
        # ('footer', '', '', '', 'black', 'dark cyan'),
        # ('popup', '', '', '', 'black', '#666'),
        # ('popup_footer', '', '', '', 'black', 'dark green'),

        ("bg", "default", "default"),
        ("country0", "white", "black"),
        ("country1", "light gray", "black"),
        ("country_selected", "black", "dark green"),
        ("footer", "black", "dark cyan"),
        ("title", "default,bold", "default"),
        ('popup', 'black', 'dark gray'),
        ('popup_footer', 'black', 'dark green'),
        ('banner', 'black', 'light gray'),
    ]

    def __init__(self, downloaders, print_part_info_queue):
        self.downloaders = downloaders
        self.print_part_info_queue = print_part_info_queue
        self.pages = []

        self.thread = threading.Thread(target=self.update_ui)

        self.loop = uw.MainLoop(self, self.palette, unhandled_input=self.unhandled_input, pop_ups=True)
        self.loop.screen.set_terminal_properties(colors=256)

        self.summary_view = detail_view.UldDetailView(3, self.print_part_info_queue)
        self.list_view = list_view.UldListView()
        self.detail_view = detail_view.UldDetailView(10, self.print_part_info_queue)

        col_rows = uw.raw_display.Screen().get_cols_rows()
        h = col_rows[0] - 2
        f1 = uw.Filler(self.list_view, valign='top', height=h)
        f2 = uw.Filler(self.detail_view, valign='top')
        self.box_summary = uw.AttrMap(uw.LineBox(self.summary_view, title="Summary", title_attr="title"), "bg")
        self.box_list = uw.AttrMap(uw.LineBox(f1, title="List of Files", title_attr="title"), "bg")
        self.box_details = uw.AttrMap(uw.LineBox(f2, title="File Details", title_attr="title"), "bg")
        self.olay_add_link = popups.UldOverlay(self)
        self.footer = uw.AttrMap(
            uw.Text([
                ("key", "F1"), "Help",
                ("key", "F2"), "Start",
                ("key", "F3"), "Pause",
                ("key", "F4"), "StartAll",
                ("key", "F5"), "PauseAll",
                ("key", "F6"), "AddLink",
                ("key", "F7"), "AddLinkFile",
                ("key", "F8"), "RemoveLink",
                ("key", "F9"), "RemoveFinished",
            ]), "footer")

        uw.connect_signal(self.list_view, 'show_details', self.show_details)
        uw.connect_signal(self.list_view, 'show_details', self.show_summary)

        columns = uw.Columns([('weight', 1, self.box_list), ('weight', 1, self.box_details)])

        super(UldFrame, self).__init__(header=self.box_summary, body=columns, footer=self.footer)
        self.thread.start()

    def show_details(self, country):
        self.detail_view.set_country(country)

    def show_summary(self, data):
        self.summary_view.set_country(data)

    def AddLink(self, page_):
        self.pages.append(page_)
        self.pages[-1].parse()
        self.list_view.AddItem(self.pages[-1].filename)
        
    def keypress(self, size, key):
        if key == "f6":
            self.loop.widget = self.olay_add_link
        super(UldFrame, self).keypress(size, key)

    def unhandled_input(self, key):
        pass

    def update_ui(self):
        while True:
            i, line = self.print_part_info_queue.get()
            if i == -1 and line == "quit":
                return
            else:
                self.detail_view.write_line(i, line)
