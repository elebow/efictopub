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
        group.add(drawing.text(f"{self.story.date_start} – {self.story.date_end}",
                               dy=[-20]))
        drawing.add(group)

        return drawing.tostring()
