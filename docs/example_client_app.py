from efictopub import Efictopub

args = {
    "target": "http://www.reddit.com/r/whatever/comments/t5555/my_great_story",
    "title": "My Great Story",
}

# instantiate the Efictopub object. This fetches the story.
efictopub = Efictopub(args)

# write the story to the archive
efictopub.archive_story()

# write an EPUB file
efictopub.write_epub()

# return EPUB file contents without writing to disk
# NYI
efictopub.epub()

# return the Story object
efictopub.story
