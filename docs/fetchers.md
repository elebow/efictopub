# Fetchers

This document describes the supported fetchers and their options. Don't forget to
look at the general options in the README.

## `reddit_next`

Target is a Reddit submission that contains a link with the text `next` pointing
to the next chapter in the series. The fetcher will follow the links until it reaches
a submission that does not contain one.

##### Fetcher options

* `title` (required) – story title

## `reddit_author`

Target is a Reddit user page. The fetcher will fetch every submission matching the
optional `title_pattern`.

##### Fetcher options

* `title` (required) – story title
* `title_pattern` – regex to filter author's submissions

## `reddit_wiki_page`

Target is a Reddit wiki page containing links to chapters of a story. The fetcher
will fetch every link on the page that is not an intra-wiki link (ie, links that
do not contain the substring `/wiki/`).

##### Fetcher options

* `title` (required) – story title

## `ffnet`

Target is a story on fanfiction.net. The fetcher fetches all chapters.

## `ao3`

Target is a story on archiveofourown.org. The fetcher fetches all chapters.

## `wordpress`

Target is the first entry of a story on a WordPress blog. The fetcher fetches
sequential entries until the URL matches the specified regex or it reaches the most
recent entry.

##### Fetcher options

* `title` (required) – story title
* `last_chapter_pattern` – regex describing the URL of the final chapter of the story

## `spacebattles`

Target is a thread on spacebattles.com. The fetcher fetches posts in the specified
threadmark categories—by default, just "threadmarks".

##### Fetcher options

* `title` (required) – story title
* `categories` – comma- or space-separated list of threadmark categories to include.
  Defaults to just `threadmarks`. Also accepts the special value `all`.
* `order` – controls whether chapters are assembled in order of posting date (`chrono`)
  or category (`sequential`. eg, all threadmarks in posting order, followed by all
  omake in posting order, and so on).

## Implementing a new fetcher

A fetcher is a Python module located in `efictopub/fetchers/` that has the following
properties:

1. Contains a function named `can_handle_url()`, which takes a string URL and returns
   true if the fetcher is capable of handling the URL.
1. Contains a class named `Fetcher`.
   * `Fetcher` inherits from the abstract base class `efictopub.fetchers.BaseFetcher`
   * `Fetcher.fetch_story()` returns a `Story` object.

See `efictopub/fetchers/reddit_author.py` for an almost-minimal example of a fetcher.

A fetcher is usually accompanied by a model in `efictopub/models/` to represent the
fetched object (usually a chapter). These models typically implement an `as_chapter()`
method that returns an instance of `Chapter`. Some simple fetchers may construct
a `Chapter` directly.
