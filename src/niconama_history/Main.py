#-*- coding:utf-8
from CommonDb import CommonDb
from niconama_history import Output, PluginLoader
import CommentViewer
import logging.config

def main(**options):
    """
    メイン関数
    各種コメビュログを読み込んで
    共通DBにいれて
    解析して
    出力します。
    """
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("simpleExample")
    if options.get('quiet'):
        logger.setLevel(logging.WARNING)

    loader = CommentViewer.createInstance(options.get('type'))
    with CommonDb() as commonDb:
        commentList = loader.loadComment(options.get('community'))
        commonDb.insertComment(commentList)
        logger.info(u'共通DBの構築が完了しました。')

        logger.info(u'日毎に集計しています。')
        daysCommentList = commonDb.selectDays()
        logger.info(u'月毎に集計しています。')
        monthesCommentList = commonDb.selectMonthes()
        logger.info(u'年毎に集計しています。')
        yearsCommentList = commonDb.selectYears()
        logger.info(u'全期間を集計しています。')
        allCommentList = commonDb.selectAll()

        plugins = map(lambda plugin: plugin.CommentFilter(commonDb), PluginLoader.load_plugins('niconama_history_plugins'))

        history = {}
        for plugin in plugins:
            logger.info(u'{}プラグインで解析しています。'.format(plugin.__module__))
            for date, messages in _analyze(dateCommentList=daysCommentList, analyzer=plugin, methodName='analyzeDay'):
                history.setdefault(date, {}).setdefault('day', []).extend(messages)
            for date, messages in _analyze(dateCommentList=monthesCommentList, analyzer=plugin, methodName='analyzeMonth'):
                history.setdefault(date, {}).setdefault('month', []).extend(messages)
            for date, messages in _analyze(dateCommentList=yearsCommentList, analyzer=plugin, methodName='analyzeYear'):
                history.setdefault(date, {}).setdefault('year', []).extend(messages)
            for date, messages in _analyze(dateCommentList=allCommentList, analyzer=plugin, methodName='analyzeAll'):
                history.setdefault(date, {}).setdefault('all', []).extend(messages)

        with Output.createInstance(options.get('output')) as output:
            output.write(history)

def _analyze(dateCommentList, analyzer, methodName):
    """
    プラグインのメソッドを直接呼びだすとプラグインの実装によっては
    strやlistが返ってこない事があるため
    """
    history = []
    for date, rows in dateCommentList:
        messages = analyzer.__getattribute__(methodName)(rows)
        if messages:
            if isinstance(messages, str):
                history.append((date, [messages]))
            elif isinstance(messages, list):
                history.append((date, messages))

    return history

if __name__ == '__main__':
    main({ 'type': 'nwhois', 'community': 'co317507', 'output': None })
