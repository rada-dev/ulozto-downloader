import urwid as uw


class SimpleItem(uw.WidgetWrap):

    def __init__(self, caption, text, attr, focus_attr):
        self.caption = caption
        self.text = text
        line = uw.Columns([self.__caption_text, self.__text_text])
        t = uw.AttrWrap(line, attr, focus_attr)
        uw.WidgetWrap.__init__(self, t)

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    def caption(self, value):
        self.__caption = value
        self.__caption_text = uw.Text(f"{self.caption}")

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.__text_text = uw.Text(self.text)

    def set_value(self, name, value):
        setattr(self, name, value)

    def selectable(self):
        return True


class PartItem(uw.WidgetWrap):

    def __init__(self, i_part, attr, focus_attr):
        self.i_part = i_part
        self.text = "Waiting..."
        self.percentage = 0.0
        self.size_curr = 0
        self.size_total = 0
        self.speed_curr = 0
        self.speed_avg = 0
        self.elapsed = 0
        self.remaining = 0
        line = uw.Columns([self.__i_part_text, self.__text_text, self.__percentage_text, self.__size_curr_text, self.__size_total_text, self.__speed_avg_text, self.__speed_curr_text, self.__elapsed_text, self.__remaining_text])
        line = uw.Columns([('fixed', 6, self.__i_text), ('weight', 10, self.__name_text), ('fixed', 10, self.__speed_text), ('fixed', 10, self.__est_text), ('fixed', 9, self.__progress_text)])
        t = uw.AttrWrap(line, attr, focus_attr)
        uw.WidgetWrap.__init__(self, t)

    @property
    def i_part(self):
        return self.__i_part

    @i_part.setter
    def i_part(self, value):
        self.__i_part = value
        self.__i_part_text = uw.Text(f"Part {self.i_part}")

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.__text_text = uw.Text(self.text)

    @property
    def percentage(self):
        return self.__percentage

    @percentage.setter
    def percentage(self, value):
        self.__percentage = value
        self.__percentage_text = uw.Text(f"{self.i_part:.1f} %")

    @property
    def size_curr(self):
        return self.__size_curr

    @size_curr.setter
    def size_curr(self, value):
        self.__size_curr = value
        self.__size_curr_text = uw.Text(f"{self.size_curr:.2f} MB/", align=uw.RIGHT)

    @property
    def size_total(self):
        return self.__size_total

    @size_total.setter
    def size_total(self, value):
        self.__size_total = value
        self.__size_total_text = uw.Text(f"{self.size_total:.2f} MB")

    @property
    def speed_curr(self):
        return self.__speed_curr

    @speed_curr.setter
    def speed_curr(self, value):
        self.__speed_curr = value
        self.__speed_curr_text = uw.Text(f"{self.speed_curr:.2f} kB/s")

    @property
    def speed_avg(self):
        return self.__speed_avg

    @speed_avg.setter
    def speed_avg(self, value):
        self.__speed_avg = value
        self.__speed_avg_text = uw.Text(f"{self.speed_avg:.2f} kB/s")

    @property
    def elapsed(self):
        return self.__elapsed

    @elapsed.setter
    def elapsed(self, value):
        self.__elapsed = value
        self.__elapsed_text = uw.Text(f"{self.elapsed}")

    @property
    def remaining(self):
        return self.__remaining

    @remaining.setter
    def remaining(self, value):
        self.__remaining = value
        self.__remaining_text = uw.Text(f"{self.remaining}")

    def set_value(self, name, value):
        setattr(self, name, value)

    def selectable(self):
        return True
