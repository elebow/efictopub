from ebooklib import epub
import functools


class EpubWriter:
    def __init__(self, story, outfile_name):
        self.story = story
        self.book = epub.EpubBook()
        self.outfile_name = outfile_name

    def write_epub(self):
        self.book.set_title(self.story.title)
        self.book.set_language("en")

        self.book.add_author(self.story.author_name)
        #self.story.date_start  # TODO decide which should be the publish date
        #self.story.date_end

        self.add_chapters()

        self.book.spine = ["nav"] + self.book.items

        epub.write_epub(self.outfile_name, self.book)

    def add_chapters(self):
        for chapter in self.epub_chapters():
            self.book.add_item(chapter)

    @functools.lru_cache()
    def build_epub_html(self, chapter, num):
        file_name = "chap_%d.xhtml" % num  # TODO pad the number
        epub_html = epub.EpubHtml(title=chapter.title, file_name=file_name, lang="en")
        epub_html.content = chapter.text
        return epub_html

    @functools.lru_cache()
    def epub_chapters(self):
        return [self.build_epub_html(chapter, num)
                for num, chapter
                in enumerate(self.story.chapters)]
