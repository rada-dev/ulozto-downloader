import urwid as uw


class UldOverlay(uw.Overlay):

    def __init__(self, frame):
        self.frame = frame
        self.loop = self.frame.loop
        self.text = uw.AttrMap(uw.LineBox(uw.Edit(""), "Paste Link"), "popup")
        self.footer = uw.AttrMap(
            uw.Text([
                ("key", "F1"), "Paste",
                ("key", "F2"), "Clear",
                ("key", "ESC"), "Close",
            ]), "popup_footer")
        self.pile = uw.Pile([self.text, self.footer])
        super(UldOverlay, self).__init__(self.pile, frame, 'center', 10000, 'middle', None)
