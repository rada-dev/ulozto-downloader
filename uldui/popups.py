import urwid as uw
import pyperclip
from uldlib import page, torrunner


class UldEdit(uw.Edit):

    def __init__(self, frame, caption="", edit_text="", multiline=False, align=uw.LEFT, wrap=uw.SPACE, allow_tab=False, edit_pos=None, layout=None, mask=None):
        self._frame = frame
        super(UldEdit, self).__init__(caption, edit_text, multiline, align, wrap, allow_tab, edit_pos, layout, mask)
        uw.register_signal(self.__class__, ['show_status', 'add_item'])

    def keypress(self, size, key):
        if key == "f1":
            clip = pyperclip.paste()
            self.edit_text = clip
            uw.emit_signal(self, 'show_status', "")
        elif key == "f2":
            self.edit_text = ""
            uw.emit_signal(self, 'show_status', "")
        elif key == "esc":
            self._frame.loop.widget = self._frame
        elif key == "enter":
            try:
                p = page.Page(self.text.strip(), self._frame.TARGET_DIR, self._frame.PARTS, torrunner.TorRunner())
                p.parse()
                uw.emit_signal(self, "add_item", p)
                self.edit_text = ""
                uw.emit_signal(self, 'show_status', "")
                self._frame.loop.widget = self._frame
            except AttributeError:
                uw.emit_signal(self, 'show_status', "Invalid link: Invalid url")
            except RuntimeError as e:
                uw.emit_signal(self, 'show_status', f"Invalid link: File not found")
        else:
            super(UldEdit, self).keypress(size, key)
            uw.emit_signal(self, 'show_status', "")


class UldOverlay(uw.Overlay):

    def __init__(self, frame):
        self.frame = frame
        self.edit = UldEdit(frame, "")
        self.text = uw.AttrMap(uw.LineBox(self.edit, "Paste Link"), "popup")
        uw.connect_signal(self.edit, 'show_status', self.show_status)
        self.keys = uw.AttrMap(
            uw.Text([
                ("key", "F1"), "Paste",
                ("key", "F2"), "Clear",
                ("key", "ENTER"), "AddLink",
                ("key", "ESC"), "Close",
            ]), "popup_footer")
        self.status_text = uw.Text("", uw.CENTER)
        self.status = uw.AttrMap(self.status_text, "popup_status")
        self.footer = uw.Columns([("weight", 1, self.keys), ("weight", 1, self.status)])
        self.pile = uw.Pile([self.text, self.footer])
        super(UldOverlay, self).__init__(self.pile, frame, 'center', 10000, 'middle', None)
        self.flip_palette(False)

    def flip_palette(self, flip):
        self.frame.loop.screen.register_palette_entry('popup_status', 'black', ['dark green', 'light magenta'][flip])
        self.frame.loop.screen.clear()

    def show_status(self, message):
        if message:
            self.flip_palette(True)
        else:
            self.flip_palette(False)
        self.status_text.set_text(message)
