try:
    import app
except ImportError:
    from . import app


def run():
    a = app.App()
    a.start()


if __name__ == '__main__':
    run()
