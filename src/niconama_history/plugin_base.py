#-*- coding:utf-8
'''
Created on 2011/03/20

@author: madguy
'''

class PluginBase(object):
    """
    プラグインの基底クラスです。
    """
    def __init__(self):
        pass

    def ready(self, db):
        pass

    def analyzeDay(self, date, rows):
        pass

    def analyzeMonth(self, date, rows):
        pass

    def analyzeYear(self, date, rows):
        pass

    def analyzeAll(self, date, rows):
        pass