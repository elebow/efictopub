import datetime
import svgwrite


class CoverGenerator:
    def __init__(self, story):
        self.story = story

    def generate_cover_svg(self):
        drawing = svgwrite.Drawing()
        group = drawing.g(style="font-family:Times")

        group.add(drawing.text(**self.title_line, dy=[50]))
        group.add(drawing.text(**self.author_line, dy=[80]))
        group.add(drawing.text(**self.permalink_line, dy=[105]))
        group.add(drawing.text(**self.date_line, dy=[130]))

        # TODO complete/incomplete/dead status
        # TODO word and chapter counts

        drawing.add(group)
        return drawing.tostring()

    @property
    def title_line(self):
        return {"text": self.story.title, "style": "font-size: 30; width: 100%; text-anchor: middle;"}

    @property
    def author_line(self):
        return {"text": self.story.author_name}

    @property
    def permalink_line(self):
        return {"text": self.story.chapters[0].permalink}

    @property
    def date_line(self):
        start = datetime.date.fromtimestamp(self.story.date_start).strftime("%Y-%m-%d")
        end = datetime.date.fromtimestamp(self.story.date_end).strftime("%Y-%m-%d")
        fetched = datetime.date.fromtimestamp(self.story.date_fetched).strftime("%Y-%m-%d")

        return {"text": f"{start} – {end} (fetched {fetched})"}
