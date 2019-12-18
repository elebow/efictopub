# Efictopub

efictopub is a tool for downloading amateur fiction from the web and generating EPUB
files.

This package provides the CLI tool `efictopub` and the Python module `efictopub`.

## What are the features though

* Supports multiple fetching strategies, for numerous sites:
  * Reddit
  * Fanfiction.net
  * Archive of our Own
  * WordPress
  * SpaceBattles forums
* Can include all comments, or just comment chains that include an author response
* Produces standard EPUB files
* Generates text-only covers for visibility in e-reader libraries
* Maintains a local archive in JSON format for integration with other tools
* Uses git to manage local archive history

## CLI usage examples

```sh
# Reddit submissions containing "next" links
efictopub https://www.reddit.com/r/some_subreddit/comments/4t39sa/some_submission_title/ --title="My Great Story"

# Reddit submissions by author name and title pattern
efictopub https://www.reddit.com/u/some_redditor --fetcher-opt title_pattern="My Great Story" --title="My Great Story"

# Reddit submissions by reddit wiki page containing a list of links to chapters
efictopub https://www.reddit.com/r/some_subreddit/wiki/some_page --title="My Great Story"

# Fanfiction.net
efictopub https://www.fanfiction.net/s/8601250555/1/My-Great-Story

# Archive of our Own
efictopub https://archiveofourown.org/works/10896981

# Sequential WordPress chapters by start URL and end pattern
efictopub https://some-blog.wordpress.com/2011/06/11/1-1/ --fetcher-opt last_chapter_pattern="2013/11/19/interlude-end" --title="My Great Story"

# Spacebattles thread with categories of threadmarks
efictopub https://forums.spacebattles.com/threads/my-great-story.555/ --title="My Great Story" --fetcher-opt "categories=threadmarks,omake,sidestory" --fetcher-opt "order=chrono"

# Re-render a story from the local efictopub archive
efictopub /path/to/archived/file.json
```

## Library usage examples

```python
from efictopub import Efictopub

args = {
    "target": "http://www.reddit.com/r/whatever/comments/t5555/my_great_story",
    "title": "My Great Story",
}

# instantiate the Efictopub object.
efictopub = Efictopub(args)

# The Story object. Referencing this lazily fetches the story from the source.
efictopub.story

# write the story to the archive. This will fetch the story, if it hasn't been yet.
efictopub.archive_story()

# write an EPUB file. This will fetch the story, if it hasn't been yet.
efictopub.write_epub()

# return EPUB file contents without writing to disk. This will fetch the story, if it hasn't been yet.
# NYI
efictopub.epub()
```

## Options (CLI)

See also the built-in help text (`efictopub --help`).

* `--fetcher FETCHER`, `-F FETCHER`

   manually specify fetcher to use

* `--config CONFIG_FILE`, `-c CONFIG_FILE`

   override default config file

* `--outfile OUTFILE`, `-o OUTFILE`

   specify output file, for actions that support an output file (default varies per
   action)

* `--no-archive`

   do not write the story to the archive

* `--no-clobber`

   do not clobber uncommitted changes in the archive or existing output files

* `--comments {all,author,none}`

   store and write comments, for fetchers that support comments. Set to `author`
   to only include comment trees that contain a comment by the story author.

* `--no-write-epub`

   do not write an EPUB file

* `--fetcher-opt FETCHER_OPTS`

   specify extra options passed through to fetchers. See <https://github.com/elebow/efictopub/blob/master/docs/fetchers.md>.

* `--title TITLE`, `-t TITLE`

   manually specify story title

* `--author AUTHOR`, `-a AUTHOR`

   manually specify story author

## Options (module API)

The options described above can be passed in to the `Efictopub` constructor as a
dict. See the example client app above.

## Configuration file

Default options can be specified in a config file, which is respected in both CLI
and API modes. See <https://github.com/elebow/efictopub/blob/master/efictopub/config_default.yaml>
for the internal default config file, which also serves as an example.

Options specified in the as command-line arguments or passed to the `Efictopub`
constructor take precedence over the config file.

## A note about copyrights

Many written works are protected by copyright law. It is your responsibility when
using this tool to ensure that your usage is permissible in all applicable jurisdictions.

## A note about courtesy

Even in cases where use of this tool is legally permitted, some authors may prefer
that you not use it under certain circumstances, or at all. For example, an author
may be in the process of seeking a book deal. Please respect the wishes of authors.
