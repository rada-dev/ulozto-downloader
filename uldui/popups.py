import urwid as uw
import pyperclip


class UldEdit(uw.Edit):

    def __init__(self, frame, caption="", edit_text="", multiline=False, align=uw.LEFT, wrap=uw.SPACE, allow_tab=False, edit_pos=None, layout=None, mask=None):
        self._frame = frame
        super(UldEdit, self).__init__(caption, edit_text, multiline, align, wrap, allow_tab, edit_pos, layout, mask)

    def keypress(self, size, key):
        if key == "f1":
            clip = pyperclip.paste()
            self.edit_text = clip
        elif key == "f2":
            self.edit_text = ""
        elif key == "esc":
            self._frame.loop.widget = self._frame
        else:
            super(UldEdit, self).keypress(size, key)


class UldOverlay(uw.Overlay):

    def __init__(self, frame):
        self.text = uw.AttrMap(uw.LineBox(UldEdit(frame, ""), "Paste Link"), "popup")
        self.footer = uw.AttrMap(
            uw.Text([
                ("key", "F1"), "Paste",
                ("key", "F2"), "Clear",
                ("key", "ESC"), "Close",
            ]), "popup_footer")
        self.pile = uw.Pile([self.text, self.footer])
        super(UldOverlay, self).__init__(self.pile, frame, 'center', 10000, 'middle', None)
