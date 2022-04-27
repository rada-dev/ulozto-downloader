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
        ("bg", "light gray", "black"),
        ("item0", "white", "black"),
        ("item1", "light gray", "black"),
        ("item_selected", "black", "dark green"),
        ("footer", "black", "dark cyan"),
        ("title", "default,bold", "default"),
        ('popup', 'black', 'dark gray'),
        ('popup_footer', 'black', 'dark green'),
    ]

    def __init__(self, downloaders, print_part_info_queue):
        self.downloaders = downloaders
        self.print_part_info_queue = print_part_info_queue
        self.pages = []

        self.thread = threading.Thread(target=self.update_ui)

        self.loop = uw.MainLoop(self, self.palette, unhandled_input=self.unhandled_input, pop_ups=True)
        self.loop.screen.set_terminal_properties(colors=256)

        self.list_view = list_view.UldListView()
        self.detail_view = detail_view.UldDetailView(10, self.print_part_info_queue)

        f1 = uw.Filler(self.list_view, valign="top", height=1000)
        f2 = uw.Filler(self.detail_view, valign="top", height=1000)
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
                ("key", "Tab"), "Switch",
            ]), "footer")

        uw.connect_signal(self.list_view, 'show_details', self.show_details)

        self.pile = uw.Pile([('weight', 1, self.box_list), ('weight', 1, self.box_details)], focus_item=0)

        super(UldFrame, self).__init__(body=self.pile, footer=self.footer)
        self.thread.start()

    def show_details(self, data):
        self.detail_view.show_details()

    def AddLink(self, page_):
        self.pages.append(page_)
        self.pages[-1].parse()
        self.list_view.AddItem(self.pages[-1].filename)
        
    def keypress(self, size, key):
        if key == "f2":
            i_highlighted = self.list_view.walker.focus
            url = self.pages[i_highlighted].url
            parts = self.pages[i_highlighted].parts
            target_dir = self.pages[i_highlighted].target_dir
            self.downloaders[i_highlighted].download_thread(url, parts, target_dir)
        elif key == "f6":
            self.loop.widget = self.olay_add_link
        elif key == "tab":
            if self.pile.focus_position == 0:   # upper listbox in focus
                self.pile.set_focus(1)
                if len(self.detail_view.walker) > 0:
                    self.detail_view.lb.set_focus(0)
            else:
                self.pile.set_focus(0)
                if len(self.list_view.walker) > 0:
                    self.list_view.lb.set_focus(0)
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
