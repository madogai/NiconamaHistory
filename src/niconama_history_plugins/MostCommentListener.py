#-*- coding:utf-8
'''
Created on 2011/03/13

@author: madguy
'''
from collections import defaultdict
from niconama_history.PluginBase import PluginBase

"""
    community_id TEXT,
    user_id TEXT,
    name TEXT,
    message TEXT,
    option TEXT,
    datetime TEXT
"""

class commentFilter(PluginBase):

    def __init__(self, db):
        pass

    @property
    def name(self):
        return 'MostCommentListener'

    def analyzeMonth(self, rows):
        userDict = defaultdict(int)

        for row in filter(lambda row: (row.name is not None) and (len(row.name) > 0), rows):
            userDict[(row.userId, row.name)] += 1

        userName = max(userDict, key = lambda x: userDict.get(x))[1]
        message = '一番発言したのは{0}さんでした。'.format(userName)
        return message

if __name__ == '__main__':
    pass
