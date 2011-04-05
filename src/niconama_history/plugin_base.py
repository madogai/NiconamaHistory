#-*- coding:utf-8
'''
Created on 2011/03/20

@author: madguy
'''

class PluginBase(object):
    """
    プラグインの基底クラスです。
    """
    @property
    def name(self):
        return ''

    def analyzeDay(self, rows):
        pass

    def analyzeMonth(self, rows):
        pass

    def analyzeYear(self, rows):
        pass

    def analyzeAll(self, rows):
        pass