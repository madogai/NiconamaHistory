#-*- coding:utf-8

class PluginBase(object):
    """
    プラグインの基底クラスです。
    """
    def __init__(self):
        pass

    def ready(self, db):
        """
        プラグイン読み込み時に呼ばれる関数です。
        dbへの参照が引数として与えられます。

        """
        pass

    def analyzeDay(self, date, rows):
        """
        日毎の集計を行います。

        :param datetime date: 日付
        :param list rows: Commentクラスのリスト
        """
        pass

    def analyzeMonth(self, date, rows):
        """
        月毎の集計を行います。

        :param datetime date: 日付
        :param list rows: Commentクラスのリスト
        """
        pass

    def analyzeYear(self, date, rows):
        """
        年毎の集計を行います。

        :param datetime date: 日付
        :param list rows: Commentクラスのリスト
        """
        pass

    def analyzeAll(self, date, rows):
        """
        全期間の集計を行います。

        :param datetime date: 日付
        :param list rows: Commentクラスのリスト
        """
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()