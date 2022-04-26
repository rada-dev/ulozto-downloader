import urwid as uw
try:
    import frame
except ImportError:
    from . import frame


class App(object):

    def __init__(self):
        self.frame = frame.UldFrame()
        self.loop = uw.MainLoop(self.frame, self.frame.palette, unhandled_input=self.unhandled_input, pop_ups=True)
        self.frame.loop = self.loop

    def start(self):
        self.frame.update_data()
        self.loop.run()

    def unhandled_input(self, key):
        if key == "esc":
            self.loop.widget = self.frame
