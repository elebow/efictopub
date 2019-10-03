from efictopub.models.chapter import Chapter
from efictopub.models.comment import Comment
from efictopub.models.story import Story


def read_fixture(fname):
    with open(f"tests/fixtures/{fname}", "r") as file:
        return file.read()


def chapter_real(n=0):
    return Chapter(
        comments=comments_real(3),
        date_published=f"{n}0",
        date_updated=f"{n}1",
        permalink=f"permalink {n}",
        score=5,
        text=f"<p>chapter content {n}</p>",
        title=f"chapter title {n}",
    )


def chapters_real(count):
    return [chapter_real(n) for n in range(0, count)]


def comment_real(n):
    return Comment(
        author=f"author {n}",
        date_published=f"published date {n}",
        date_updated=f"updated date {n}",
        permalink=f"permalink {n}",
        replies=[comment_real(m) for m in range(0, n - 1)] if n > 0 else [],
        score=f"score {n}",
        text=f"text {n}",
    )


def comments_real(count):
    return [comment_real(n) for n in range(0, count)]


def story_real():
    return Story(
        title="My Great Story",
        author="Great Author",
        summary="A great story.",
        chapters=chapters_real(3),
    )


ffnet_chapter_html_real = read_fixture("www.fanfiction.net_1.html")
ffnet_chapter_2_html_real = read_fixture("www.fanfiction.net_2.html")
ffnet_chapter_3_html_real = read_fixture("www.fanfiction.net_3.html")
ffnet_chapter_reviews_html_real = read_fixture("www.fanfiction.net_reviews.html")
ffnet_single_chapter_story_html_real = read_fixture("www.fanfiction.net_single.html")
ffnet_single_chapter_story_reviews_html_real = read_fixture(
    "www.fanfiction.net_single_reviews.html"
)

spacebattles_threadmarks_index_html = read_fixture(
    "spacebattles_threadmarks_index.html"
)
spacebattles_thread_reader_1_html = read_fixture("spacebattles_thread_reader_1.html")
spacebattles_thread_reader_2_html = read_fixture("spacebattles_thread_reader_2.html")

wordpress_chapter_html_real_1 = read_fixture("wordpress_1.html")
wordpress_chapter_html_real_2 = read_fixture("wordpress_2.html")
