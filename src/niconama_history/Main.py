#-*- coding:utf-8
from CommonDb import CommonDb
from niconama_history import Output, CommentAnalyzer, PluginLoader
import CommentViewer

def main(**options):
    """
    メイン関数
    各種コメビュログを読み込んで
    共通DBにいれて
    解析して
    出力します。
    """
    loader = CommentViewer.createInstance(options.get('type'))
    with CommonDb() as commonDb:
        commentList = loader.loadComment(options.get('community'))
        commonDb.insertComment(commentList)
        print '日毎に集計しています。'
        daysCommentList = commonDb.selectDays()
        print '月毎に集計しています。'
        monthesCommentList = commonDb.selectMonthes()
        print '年毎に集計しています。'
        yearsCommentList = commonDb.selectYears()
        print '全期間を集計しています。'
        allCommentList = commonDb.selectAll()

        plugins = map(lambda plugin: plugin.CommentFilter(commonDb), PluginLoader.load_plugins('niconama_history_plugins'))

        history = {}
        for plugin in plugins:
            print '{}プラグインで解析しています。'.format(plugin.__module__)
            for date, messages in CommentAnalyzer.analyze(dateCommentList=daysCommentList, analyzer=plugin, methodName='analyzeDay'):
                history.setdefault(date, {}).setdefault('day', []).extend(messages)
            for date, messages in CommentAnalyzer.analyze(dateCommentList=monthesCommentList, analyzer=plugin, methodName='analyzeMonth'):
                history.setdefault(date, {}).setdefault('month', []).extend(messages)
            for date, messages in CommentAnalyzer.analyze(dateCommentList=yearsCommentList, analyzer=plugin, methodName='analyzeYear'):
                history.setdefault(date, {}).setdefault('year', []).extend(messages)
            for date, messages in CommentAnalyzer.analyze(dateCommentList=allCommentList, analyzer=plugin, methodName='analyzeAll'):
                history.setdefault(date, {}).setdefault('all', []).extend(messages)

        with Output.createInstance(options.get('output')) as output:
            output.write(history)

if __name__ == '__main__':
    main({ 'type': 'nwhois', 'community': 'co317507', 'output': None })
