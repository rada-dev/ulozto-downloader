import urwid as uw
try:
    import frame
except ImportError:
    from . import frame


class App(object):

    def __init__(self):
        self.frame = frame.UldFrame()

    def start(self):
        self.frame.update_data()
        self.frame.loop.run()
