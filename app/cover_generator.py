import datetime
import svgwrite


class CoverGenerator:
    def __init__(self, story):
        self.story = story

    def generate_cover_svg(self):
        drawing = svgwrite.Drawing()

        group = drawing.g(style="font-family:Times")
        group.add(drawing.text(self.story.title,
                               y=[50],
                               style="font-size: 30; width: 100%; text-align: center;"))
        group.add(drawing.text(self.date_line, dy=[80]))
        drawing.add(group)

        return drawing.tostring()

    @property
    def date_line(self):
        start = datetime.date.fromtimestamp(self.story.date_start).strftime("%Y-%m-%d")
        end = datetime.date.fromtimestamp(self.story.date_end).strftime("%Y-%m-%d")
        fetched = "TODO"

        return f"{start} – {end} (fetched {fetched})"
