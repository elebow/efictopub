import datetime
import svgwrite


class CoverGenerator:
    def __init__(self, story):
        self.story = story

    def generate_cover_svg(self):
        drawing = svgwrite.Drawing(size=(400, 220), debug=True)
        group = drawing.g(style="font-family: Times; dominant-baseline: hanging")

        group.add(drawing.text(**self.title_line(), x=["50%"], y=[0]))
        group.add(drawing.text(**self.author_line(), x=["50%"], dy=[30]))
        group.add(drawing.text(**self.date_line(), x=[10], y=[80]))
        group.add(drawing.text(**self.permalink_line(), x=[10], y=[100]))
        group.add(drawing.text(**self.chaptercount_line(), x=[10], y=[120]))
        group.add(drawing.text(**self.wordcount_line(), x=[10], y=[140]))

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

    def chaptercount_line(self):
        chaptercount = len(self.story.chapters)
        if chaptercount > 1:
            chapters_string = "chapters"
        else:
            chapters_string = "chapter"
        return {"text": f"{chaptercount} {chapters_string}"}

    def wordcount_line(self):
        wordcount = sum([len(chapter.text.split()) for chapter in self.story.chapters])
        return {"text": f"{wordcount} words"}
