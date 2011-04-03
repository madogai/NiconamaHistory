#-*- coding:utf-8
'''
Created on 2011/03/20

@author: madguy
'''
from niconama_history.PluginBase import PluginBase

class CommentFilter(PluginBase):
    """
    コメントの統計を出力するプラグインです
    """

    def __init__(self, db):
        PluginBase.__init__(self)
        self.__flag = True

    @property
    def name(self):
        return 'TotalComment'

    def analyzeAll(self, rows):
        return u'コメント数の総計は{0}件でした。'.format(len(rows))

if __name__ == '__main__':
    pass