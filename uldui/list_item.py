import urwid as uw


class ListItem(uw.WidgetWrap):

    def __init__(self, i, data, attr, focus_attr):
        self.data = data
        self.i = i
        self.name = self.data["name"]
        self.speed = 200
        self.est = "00:00:00"
        self.progress = 100.0
        line = uw.Columns([('fixed', 6, self.__i_text), ('weight', 10, self.__name_text), ('fixed', 10, self.__speed_text), ('fixed', 10, self.__est_text), ('fixed', 9, self.__progress_text)])
        t = uw.AttrWrap(line, attr, focus_attr)
        uw.WidgetWrap.__init__(self, t)

    @property
    def i(self):
        return self.__i

    @i.setter
    def i(self, value):
        self.__i = value
        self.__i_text = uw.Text(f"{self.__i + 1}")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self.__name_text = uw.Text(self.name)

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value
        self.__speed_text = uw.Text(f"{self.speed} kB/s", align=uw.RIGHT)

    @property
    def est(self):
        return self.__est

    @est.setter
    def est(self, value):
        self.__est = value
        self.__est_text = uw.Text(f"{self.est}", align=uw.RIGHT)

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, value):
        self.__progress = value
        self.__progress_text = uw.Text(f"{self.progress} %", align=uw.RIGHT)

    def selectable(self):
        return True

    def keypress(self, size, key):
        # if key not in ("up", "down"):
        #     self.text.set_text(key+"\t\t 50%")
        #     # t = uw.AttrWrap(uw.Text(key), "default", "country_selected")
        #     #
        #     # uw.WidgetWrap.__init__(self, t)
        return key