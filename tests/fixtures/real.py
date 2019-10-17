def read_fixture(fname):
    with open(f"tests/fixtures/{fname}", "r") as file:
        return file.read()


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
