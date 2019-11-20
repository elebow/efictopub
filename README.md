# Efictopub

efictopub is a tool for downloading amateur fiction from the web and generating EPUB
files.

## What are the features though

* Supports multiple fetching strategies, for numerous sites:
  * Reddit
    * start at given submission and follow "next" links
    * all submissions from author matching a regex
    * all submissions linked on a wiki page
  * Fanfiction.net
  * WordPress
  * SpaceBattles forums
    * specify one or more threadmark categories
    * multiple ordering options
      * chronologically by post date, with all the categories interleaved
      * sequentially by category (eg, all the main story followed by all the omakes)
* Can include posted comments, or just comment chains that include an author response
* Produces standard EPUB files
* Generates text-only covers for visibility in e-reader libraries
* Maintains a local archive in JSON format for integration with other tools
* Uses git to manage local archive history

## Show me some usage examples

```sh
# Reddit submissions containing "next" links
efictopub https://www.reddit.com/r/some_subreddit/comments/4t39sa/some_submission_title/ --title="My Great Story"

# Reddit submissions by author name and title pattern
efictopub https://www.reddit.com/u/some_redditor --fetcher-opt title_pattern="My Great Story" --title="My Great Story"

# Reddit submissions by reddit wiki page containing a list of links to chapters
efictopub https://www.reddit.com/r/some_subreddit/wiki/some_page --title="My Great Story"

# Fanfiction.net
efictopub https://www.fanfiction.net/s/8601250555/1/My-Great-Story

# Sequential WordPress chapters by start URL and end pattern
efictopub https://some-blog.wordpress.com/2011/06/11/1-1/ --fetcher-opt last_chapter_pattern="2013/11/19/interlude-end" --title="My Great Story"

# Spacebattles thread with categories of threadmarks
efictopub https://forums.spacebattles.com/threads/my-great-story.555/ --title="My Great Story" --fetcher-opt "categories=threadmarks,omake,sidestory" --fetcher-opt "order=chrono"

# Re-render a story from the local efictopub archive
efictopub /path/to/archived/file.json
```

See the built-in help text (`efictopub --help`) for more options.

## A note about copyrights

Many written works are protected by copyright law. It is your responsibility when
using this tool to ensure that your usage is permissible in all applicable jurisdictions.

## A note about courtesy

Even in cases where use of this tool is legally permitted, some authors may prefer
that you not use it under certain circumstances, or at all. For example, an author
may be in the process of seeking a book deal. Please respect the wishes of authors.

## Implementing a new fetcher

A fetcher is a Python module located in `efictopub/fetchers/` that has the following
properties:

1. Contains a function named `can_handle_url()`, which takes a string URL and returns
   true if the fetcher is capable of handling the URL.
1. Contains a class named `Fetcher`.
      - `Fetcher` inherits from the abstract base class `efictopub.fetchers.BaseFetcher`
      - `Fetcher.fetch_story()` returns a `Story` object.

See `efictopub/fetchers/reddit_author.py` for an almost-minimal example of a fetcher.

A fetcher is usually accompanied by a model in `efictopub/models/` to represent the
fetched object (usually a chapter). These models typically implement an `as_chapter()`
method that returns an instance of `Chapter`. Some simple fetchers may construct
a `Chapter` directly.
