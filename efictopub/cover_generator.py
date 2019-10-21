import datetime
import svgwrite


class CoverGenerator:
    def __init__(self, story):
        self.story = story
        self.drawing = svgwrite.Drawing(size=(400, 400), debug=True)
        self.group = self.drawing.g(
            style="font-family: Times; dominant-baseline: hanging"
        )

    def generate_cover_svg(self):
        self.add_title_line()

        self.group.add(self.drawing.text(**self.author_line(), x=["50%"], dy=[self.last_y + 30]))
        self.group.add(self.drawing.text(**self.date_line(), x=[10], y=[self.last_y + 80]))
        self.group.add(self.drawing.text(**self.permalink_line(), x=[10], y=[self.last_y + 100]))
        self.group.add(self.drawing.text(**self.chaptercount_line(), x=[10], y=[self.last_y + 120]))
        self.group.add(self.drawing.text(**self.wordcount_line(), x=[10], y=[self.last_y + 140]))

        self.drawing.add(self.group)
        return self.drawing.tostring()

    def add_title_line(self):
        # SVG doesn't have a way to wrap text, and it's hard to know how wide a text element is going to be
        # So just naively wrap the text at the word breaks closest to 18 characters per line

        lines = self.break_lines(self.story.title)
        for line_num, line in enumerate(lines):
            text_element = self.drawing.text(
                text=line,
                style="font-size: 30; width: 100%; text-anchor: middle;",
                x=["50%"],
                y=[line_num * 30],
            )
            self.group.add(text_element)
        self.last_y = len(lines) * 30

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

    def break_lines(self, line, max_chars=24):
        if len(line) < max_chars:
            return [line]

        words = list(map(str.strip, line.split()))
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) < max_chars:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
