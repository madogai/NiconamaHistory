#-*- coding:utf-8
from niconama_history.plugin_base import PluginBase
from dateutil.relativedelta import relativedelta

class CommentFilter(PluginBase):
    """
    放送開始日を抽出するプラグインです。
    """
    def __init__(self):
        self.firstDay = None

    def analyzeDay(self, date, rows):
        if not self.firstDay:
            self.firstDay = date
            return u'放送を開始しました！'
        elif date == self.firstDay + relativedelta(months=3):
            return u'放送開始から3カ月が経過しました！'
        else:
            for i in range(1, 10):
                if date == self.firstDay + relativedelta(years=i):
                    return u'放送{0}周年です！'.format(i)

if __name__ == '__main__':
    pass