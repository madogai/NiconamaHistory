#-*- coding:utf-8
'''
Created on 2011/03/20

@author: madguy
'''
from niconama_history.plugin_base import PluginBase

class CommentFilter(PluginBase):
    """
    放送開始日を抽出するプラグインです。
    """
    def __init__(self):
        self.firstDay = None

    def analyzeDay(self, date, rows):
        if self.firstDay:
            self.firstDay = date
            return u'放送を開始しました！'

if __name__ == '__main__':
    pass