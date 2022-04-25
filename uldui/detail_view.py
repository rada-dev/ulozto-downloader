import urwid as uw


class DetailView(uw.WidgetWrap):

    def __init__(self):
        t = uw.Text("")
        uw.WidgetWrap.__init__(self, t)

    def set_country(self, data):
        s = f'Name: {data["name"]}\nPop:  {data["pop"]}\nGDP:  {data["gdp"]}'
        self._w.set_text(s)
