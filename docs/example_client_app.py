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
