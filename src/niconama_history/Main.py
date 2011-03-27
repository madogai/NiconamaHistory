#-*- coding:utf-8
from CommonDb import CommonDb
from collections import defaultdict
import CommentViewer
import PluginLoader

def main(communityId, type):
    """メイン関数
    各種コメビュログを読み込んで
    共通DBにいれて
    解析して
    吐き出します。
    """

    loader = CommentViewer.createInstance(type)
    with CommonDb() as commonDb:
        commentList = loader.loadComment(communityId)
        commonDb.insertComment(commentList)

        print '共通DBの構築が完了しました。'

        plugins = map(lambda plugin: plugin.commentFilter(commonDb), PluginLoader.load_plugins('niconama_history_plugins'))

        print 'プラグインの読み込みが完了しました。'

        history = defaultdict(list)

        print '日毎の集計を行っています。'

        for date, rows in commonDb.selectDays():
            for plugin in plugins:
                messages = plugin.analyzeDay(rows)
                if not messages:
                    continue

                history.setdefault(date, {'year': [], 'month':[], 'day': [], 'all': [] })
                if isinstance(messages, str):
                    history[date]['day'].append(messages)
                elif isinstance(messages, list):
                    history[date]['day'].extend(messages)

        print '月毎の集計を行っています。'

        for date, rows in commonDb.selectMonthes():
            for plugin in plugins:
                messages = plugin.analyzeMonth(rows)
                if not messages:
                    continue

                history.setdefault(date, {'year': [], 'month':[], 'day': [], 'all': [] })
                if isinstance(messages, str):
                    history[date]['month'].append(messages)
                elif isinstance(messages, list):
                    history[date]['month'].extend(messages)

        print '年毎の集計を行っています。'

        for date, rows in commonDb.selectYears():
            for plugin in plugins:
                messages = plugin.analyzeYear(rows)
                if not messages:
                    continue

                history.setdefault(date, {'year': [], 'month':[], 'day': [], 'all': [] })
                if isinstance(messages, str):
                    history[date]['year'].append(messages)
                elif isinstance(messages, list):
                    history[date]['year'].extend(messages)

        print '全体の集計を行っています。'

        for date, rows in commonDb.selectAll():
            for plugin in plugins:
                messages = plugin.analyzeAll(rows)
                if not messages:
                    continue

                history.setdefault(date, {'year': [], 'month':[], 'day': [], 'all': [] })
                if isinstance(messages, str):
                    history[date]['all'].append(messages)
                elif isinstance(messages, list):
                    history[date]['all'].extend(messages)

        for key in sorted(history.keys()):
            date = history.get(key)

            if len(date['day']) > 0:
                print '{0}年{1}月{2}日'.format(key.year, key.month, key.day)
                for post in date['day']:
                    print post
                print

            if len(date['month']) > 0:
                print '{0}年{1}月のまとめ'.format(key.year, key.month)
                for post in date['month']:
                    print post
                print

            if len(date['year']) > 0:
                print '{0}年のまとめ'.format(key.year)
                for post in date['year']:
                    print post
                print

            if len(date['all']) > 0:
                print '放送のまとめ'.format(key.year)
                for post in date['all']:
                    print post

        print

if __name__ == '__main__':
    main('co317507', 'nwhois')
