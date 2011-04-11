#-*- coding:utf-8

from niconama_history.plugin_base import PluginBase

class CommentFilter(PluginBase):
    """
    コメントの統計を出力するプラグインです
    """

    def __init__(self):
        self.__flag = True

    def analyzeAll(self, date, rows):
        return u'コメント数の総計は{0}件でした。'.format(len(rows))

if __name__ == '__main__':
    pass