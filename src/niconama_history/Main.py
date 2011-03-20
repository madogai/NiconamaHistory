#-*- coding:utf-8
from CommonDb import CommonDb
from collections import defaultdict
import DataLoader
import PluginLoader

def main():
    loader = DataLoader.createInstance('nwhois')
    if loader == None:
        pass

    commentList = loader.load('co317507')

    with CommonDb() as commonDb:
        commonDb.insertComment(commentList)

        print '共通DBの構築が完了しました。'

        plugins = map(lambda plugin: plugin.commentFilter(commonDb), PluginLoader.load_plugins('niconama_history_plugins'))

        print 'プラグインの読み込みが完了しました。'

        history = defaultdict(list)

        print '日毎の集計を行っています。'

        for date, rows in commonDb.selectDays():
            for plugin in plugins:
                messages = plugin.analyzeDay(rows)
                if messages is None:
                    continue

                history.setdefault(date, {'year': [], 'month':[], 'day': [] })
                if isinstance(messages, str):
                    history[date]['day'].append(messages)
                elif isinstance(messages, list):
                    history[date]['day'].extend(messages)

        print '月毎の集計を行っています。'

        for date, rows in commonDb.selectMonthes():
            for plugin in plugins:
                messages = plugin.analyzeMonth(rows)
                if messages is None:
                    continue

                history.setdefault(date, {'year': [], 'month':[], 'day': [] })
                if isinstance(messages, str):
                    history[date]['month'].append(messages)
                elif isinstance(messages, list):
                    history[date]['month'].extend(messages)

        print '年毎の集計を行っています。'

        for date, rows in commonDb.selectYears():
            for plugin in plugins:
                messages = plugin.analyzeYear(rows)
                if messages is None:
                    continue

                history.setdefault(date, {'year': [], 'month':[], 'day': [] })
                if isinstance(messages, str):
                    history[date]['month'].append(messages)
                elif isinstance(messages, list):
                    history[date]['month'].extend(messages)

        print

        for key in sorted(history.keys()):
            for post in history.get(key)['day']:
                if post is not None:
                    print '{0}年{1}月{2}日'.format(key.year, key.month, key.day)
                    print post

            for post in history.get(key)['month']:
                print '{0}年{1}月のまとめ'.format(key.year, key.month)
                print post

            for post in history.get(key)['year']:
                print '{0}年のまとめ'.format(key.year)
                print post

        print

if __name__ == '__main__':
    main()
