import urwid as uw


class UldDetailView(uw.WidgetWrap):

    def __init__(self):
        t = uw.Text("")
        super(UldDetailView, self).__init__(t)

    def set_country(self, data):
        s = f'Name: {data["name"]}\nPop:  {data["pop"]}\nGDP:  {data["gdp"]}'
        self._w.set_text(s)
