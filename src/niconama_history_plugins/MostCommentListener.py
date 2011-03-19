#-*- coding:utf-8
'''
Created on 2011/03/13

@author: madguy
'''
from collections import defaultdict

"""
    community_id TEXT,
    user_id TEXT,
    name TEXT,
    message TEXT,
    option TEXT,
    datetime TEXT
"""

class commentFilter(object):

    def __init__(self, db):
        pass

    def getName(self):
        return 'MostCommentListener'

    def analyzeDay(self, rows):
        pass

    def analyzeMonth(self, rows):
        userDict = defaultdict(int)

        for row in filter(lambda row: (row.name is not None) and (len(row.name) > 0), rows):
            userDict[(row.userId, row.name)] += 1

        userName = max(userDict, key = lambda x: userDict.get(x))[1]
        message = '一番発言したのは{0}さんでした。'.format(userName)
        return message

    def analyzeYear(self, rows):
        pass

    def analyzeAll(self, rows):
        pass

if __name__ == '__main__':
    pass
