import datetime
import svgwrite


class CoverGenerator:
    def __init__(self, story):
        self.story = story

    def generate_cover_svg(self):
        drawing = svgwrite.Drawing(size=(300, 200), debug=True)
        group = drawing.g(style="font-family:Times")

        group.add(drawing.text(**self.title_line(), x=["50%"], y=[60]))
        group.add(drawing.text(**self.author_line(), x=["50%"], y=[90]))
        group.add(drawing.text(**self.date_line(), x=[10], y=[140]))
        group.add(drawing.text(**self.permalink_line(), x=[10], y=[160]))

        # TODO word and chapter counts

        drawing.add(group)
        return drawing.tostring()

    def title_line(self):
        return {
            "text": self.story.title,
            "style": "font-size: 30; width: 100%; text-anchor: middle;",
        }

    def author_line(self):
        return {"text": self.story.author, "style": "text-anchor: middle;"}

    def permalink_line(self):
        return {"text": self.story.chapters[0].permalink}

    def date_line(self):
        start = datetime.date.fromtimestamp(self.story.date_start).strftime("%Y-%m-%d")
        end = datetime.date.fromtimestamp(self.story.date_end).strftime("%Y-%m-%d")
        fetched = datetime.date.fromtimestamp(self.story.date_fetched).strftime(
            "%Y-%m-%d"
        )

        return {"text": f"{start} – {end} (fetched {fetched})"}
