# Efictopub

efictopub is a tool for downloading amateur fiction from the web and generating EPUB
files.

## What are the features though

* Downloads stories from several supported websites
* Requires only a URL as input
* Produce a standard EPUB files
* Generates text-only covers for visibility in e-reader libraries
* Maintains a local archive in JSON for integration with other tools
* Uses git to manage changes to the local archive

## A note about copyrights

Many written works are protected by copyright law. It is your responsibility when
using this tool to ensure that your usage is permissible in all applicable jurisdictions.

## Implementing a new fetcher

A fetcher is a Python module located in `app/fetchers/` that has the following properties:

1. Contains a function named `can_handle_url()`, which takes a string URL and returns
   true if the fetcher is capable of handling the URL.
1. Contains a class named `Fetcher`.
      a. `Fetcher` inherits from the abstract base class `app.fetchers.BaseFetcher`,
         so it must implement `fetch_story()` and `fetch_chapters()`.
      a. `Fetcher.fetch_story()` returns a `Story` object.
      a. `Fetcher.fetch_chapters()` returns a list of `Chapter` objects.

See `app/fetchers/reddit_author.py` for an almost-minimal example of a fetcher.

A fetcher is usually accompanied by a model in `app/models/` to represent the fetched
object. Models implement an `as_chapter()` method that returns an instance of `Chapter`.
Some simple fetchers may construct a `Chapter` directly.
