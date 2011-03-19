#-*- coding:utf-8
import datetime

'''
Created on 2011/03/18

@author: madguy
'''

def dateRange(firstDay, lastDay):
    '''dateリストを返します。

    >>> dateRange(datetime.date(2000, 1, 1), datetime.date(2000, 1, 3))
    [datetime.date(2000, 1, 1), datetime.date(2000, 1, 2), datetime.date(2000, 1, 3)]

    '''
    delta = (lastDay - firstDay).days + 1
    return map(lambda i: firstDay + datetime.timedelta(i), range(0, delta))

if __name__ == '__main__':
    import doctest
    doctest.testmod()