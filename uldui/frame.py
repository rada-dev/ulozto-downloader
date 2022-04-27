import time

import urwid as uw
import threading
try:
    import detail_view, list_view, popups
except ImportError:
    from . import detail_view, list_view, popups


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

        self.list_view = list_view.UldListView()
        self.detail_view = detail_view.UldDetailView(self.PARTS, self.print_part_info_queue)

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

        uw.connect_signal(self.list_view, 'show_details', self.detail_view.show_details)
        uw.connect_signal(self.olay_add_link.edit, 'add_item', self.list_view.AddItem)
        uw.connect_signal(self.list_view, 'added_item', self.detail_view.added_item)

        self.pile = uw.Pile([('weight', 1, self.box_list), ('weight', 1, self.box_details)], focus_item=0)

        super(UldFrame, self).__init__(body=self.pile, footer=self.footer)
        self.thread.start()
        
    def keypress(self, size, key):
        if key == "f2":
            if len(self.list_view.walker) > 0:
                i_highlighted = self.list_view.walker.focus
                item = self.list_view.walker[i_highlighted]
                url = item.data.url
                parts = item.data.parts
                target_dir = item.data.target_dir
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
            content = self.print_part_info_queue.get()
            if content == "quit":
                return
            else:
                self.detail_view.update(*content)
