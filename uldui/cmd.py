import sys

import urwid as uw
import signal
try:
    import app
except ImportError:
    from . import app


def run():
    def sigint_handler(sig, frame):
        sys.exit(1)
    signal.signal(signal.SIGINT, sigint_handler)

    a = app.App()
    a.start()


if __name__ == '__main__':
    run()
