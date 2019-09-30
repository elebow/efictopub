# Efictopub

efictopub is a tool for downloading amateur fiction from the web and generating EPUB
files.

## What are the features though

* Automatically selects a fetching strategy based on URL, including several for Reddit
* Produces standard EPUB files
* Generates text-only covers for visibility in e-reader libraries
* Maintains a local archive in JSON format for integration with other tools
* Uses git to manage local archive history

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
      a. `Fetcher` inherits from the abstract base class `efictopub.fetchers.BaseFetcher`
      a. `Fetcher.fetch_story()` returns a `Story` object.

See `efictopub/fetchers/reddit_author.py` for an almost-minimal example of a fetcher.

A fetcher is usually accompanied by a model in `efictopub/models/` to represent the
fetched object (usually a chapter). These models typically implement an `as_chapter()`
method that returns an instance of `Chapter`. Some simple fetchers may construct
a `Chapter` directly.
