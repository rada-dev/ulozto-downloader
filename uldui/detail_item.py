import urwid as uw


class SimpleItem(uw.WidgetWrap):

    def __init__(self, caption, text, attr, focus_attr):
        self.caption = caption
        self.text = text
        line = uw.Columns([
            ("fixed", 15, self.__caption_text),
            self.__text_text
        ])
        t = uw.AttrWrap(line, attr, focus_attr)
        uw.WidgetWrap.__init__(self, t)

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    def caption(self, value):
        self.__caption = f"{value}"
        try:
            self.__caption_text.set_text(self.caption)
        except AttributeError:
            self.__caption_text = uw.Text(self.caption)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = f"{value}"
        try:
            self.__text_text.set_text(self.text)
        except AttributeError:
            self.__text_text = uw.Text(self.text)

    def set_value(self, name, value):
        setattr(self, name, value)

    def selectable(self):
        return True


class PartItem(uw.WidgetWrap):

    def __init__(self, i_part, attr, focus_attr):
        self.i_part = i_part
        self.text = "Waiting"
        self.percentage = 0
        self.size_curr = 0
        self.size_total = 0
        self.speed_avg = 0
        self.elapsed = 0
        self.remaining = 0
        line = uw.Columns([
            ("fixed", 15, self.__caption_text),
            ("pack", self.__text_text),
            ("pack", self.__percentage_text),
            uw.Divider(),
            ("pack", self.__size_curr_text),
            ("pack", uw.Text("/")),
            ("pack", self.__size_total_text),
            uw.Divider(),
            ("pack", self.__speed_avg_text),
            uw.Divider(),
            ("pack", self.__elapsed_text),
            uw.Divider(),
            ("pack", self.__remaining_text)
        ])
        # line = uw.Columns([('fixed', 6, self.___text), ('weight', 10, self.__name_text), ('fixed', 10, self.__speed_text), ('fixed', 10, self.__est_text), ('fixed', 9, self.__progress_text)])
        t = uw.AttrWrap(line, attr, focus_attr)
        uw.WidgetWrap.__init__(self, t)

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    def caption(self, value):
        self.__caption = f"{value}"
        try:
            self.__caption_text.set_text(self.caption)
        except AttributeError:
            self.__caption_text = uw.Text(self.caption)

    @property
    def i_part(self):
        return self.__i_part

    @i_part.setter
    def i_part(self, value):
        self.__i_part = value
        self.caption = f"Part {self.i_part}:"

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = f"{value}"
        try:
            self.__text_text.set_text(self.text+"... ")
        except AttributeError:
            self.__text_text = uw.Text(self.text+"... ")

    @property
    def percentage(self):
        return self.__percentage

    @percentage.setter
    def percentage(self, value):
        self.__percentage = value
        try:
            self.__percentage_text.set_text(f"{self.percentage:.1f} %")
            self.__percentage_text.render()
        except AttributeError:
            self.__percentage_text = uw.Text(f"{self.percentage:.1f} %")

    @property
    def size_curr(self):
        return self.__size_curr

    @size_curr.setter
    def size_curr(self, value):
        self.__size_curr = value
        try:
            self.__size_curr_text.set_text(f"{self.size_curr:.2f} MB")
        except AttributeError:
            self.__size_curr_text = uw.Text(f"{self.size_curr:.2f} MB")

    @property
    def size_total(self):
        return self.__size_total

    @size_total.setter
    def size_total(self, value):
        self.__size_total = value
        try:
            self.__size_total_text.set_text(f"{self.size_total:.2f} MB")
        except AttributeError:
            self.__size_total_text = uw.Text(f"{self.size_total:.2f} MB")

    @property
    def speed_avg(self):
        return self.__speed_avg

    @speed_avg.setter
    def speed_avg(self, value):
        self.__speed_avg = value
        try:
            self.__speed_avg_text.set_text(f"avg: {self.speed_avg:.2f} kB/s")
        except AttributeError:
            self.__speed_avg_text = uw.Text(f"avg: {self.speed_avg:.2f} kB/s")

    @property
    def elapsed(self):
        return self.__elapsed

    @elapsed.setter
    def elapsed(self, seconds):
        self.__elapsed = seconds
        value = self.seconds_to_hh_mm_ss(seconds)
        try:
            self.__elapsed_text.set_text(f"elapsed: {value}")
        except AttributeError:
            self.__elapsed_text = uw.Text(f"elapsed: {value}")

    @property
    def remaining(self):
        return self.__remaining

    @remaining.setter
    def remaining(self, seconds):
        self.__remaining = seconds
        value = self.seconds_to_hh_mm_ss(seconds)
        try:
            self.__remaining_text.set_text(f"remaining: {value}")
        except AttributeError:
            self.__remaining_text = uw.Text(f"remaining: {value}")

    def set_value(self, name, value):
        setattr(self, name, value)

    @staticmethod
    def seconds_to_hh_mm_ss(seconds):
        hh, ss = divmod(int(round(seconds)), 3600)
        mm, ss = divmod(ss, 60)
        return f"{hh:02d}:{mm:02d}:{ss:02d}"

    def selectable(self):
        return True
