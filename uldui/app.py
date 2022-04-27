class App(object):

    def __init__(self, frame):
        self.frame = frame

    def start(self):
        self.frame.loop.run()

    def join(self):
        self.frame.print_part_info_queue.put("quit")
        self.frame.thread.join()
