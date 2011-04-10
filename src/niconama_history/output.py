#-*- coding:utf-8
import sys

def createInstance(path=None):
    if path:
        return File(path)
    else:
        return StdOut()

class StdOut(object):
    def __enter__(self):
        self.handle = sys.stdout
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _writePosts(self, callTitle, posts):
        if posts:
            print >> self.handle, callTitle
            for post in posts:
                print >> self.handle, post
            print >> self.handle

    def write(self, history):
        for key in sorted(history.keys()):
            date = history.get(key)
            self._writePosts(u'{0}年{1}月{2}日'.format(key.year, key.month, key.day), date.get(u'day'))
            self._writePosts(u'{0}年{1}月のまとめ'.format(key.year, key.month, key.day), date.get(u'month'))
            self._writePosts(u'{0}年のまとめ'.format(key.year, key.month, key.day), date.get(u'year'))
            self._writePosts(u'放送のまとめ'.format(key.year, key.month, key.day), date.get(u'all'))
        print

class File(StdOut):
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.handle = open(self.path, u'w')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.handle.close()

    def _writePosts(self, callTitle, posts):
        if posts:
            self.handle.write(callTitle.encode(u'utf-8'))
            self.handle.write(u'\n');
            for post in posts:
                self.handle.write(post.encode(u'utf-8'))
                self.handle.write(u'\n');
            self.handle.write(u'\n');
