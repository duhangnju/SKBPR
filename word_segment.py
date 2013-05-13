"""
Word Segmentation Stuff.
"""

class WordSegmenter(object):
    def segment(self, string):
        raise NotImplemented

class SpaceWordSegmenter(WordSegmenter):
    def segment(self, string):
        return string.split()
