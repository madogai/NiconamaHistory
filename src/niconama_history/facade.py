#-*- coding:utf-8
from common_db import CommonDb
from niconama_history import comment_viewer, output, plugin_loader, plugin_base
import inspect
import itertools
import logging
import traceback
logger = logging.getLogger('default')

def main(**options):
    """
    メイン関数
    各種コメビュログを読み込んで
    共通DBにいれて
    解析して
    出力します。
    """
    loader = comment_viewer.createInstance(options.get(u'type'))
    with CommonDb() as commonDb:
        commentList = loader.loadComment(options.get(u'community'))
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

        history = {}
        for plugin in plugin_loader.load_plugins(u'plugins'):
            for plugin in filter(lambda member: issubclass(member, plugin_base.PluginBase) and member is not plugin_base.PluginBase ,zip(*inspect.getmembers(plugin, inspect.isclass))[1]):
                try:
                    pluginInstance = plugin()
                    logger.info(u'{0}プラグインで解析しています。'.format(pluginInstance.__module__))
                    pluginInstance.ready(commonDb)
                    for date, messages in _analyze(dateCommentList=daysCommentList, analyzer=pluginInstance, methodName=u'analyzeDay'):
                        history.setdefault(date, {}).setdefault(u'day', []).extend(messages)
                    for date, messages in _analyze(dateCommentList=monthesCommentList, analyzer=pluginInstance, methodName=u'analyzeMonth'):
                        history.setdefault(date, {}).setdefault(u'month', []).extend(messages)
                    for date, messages in _analyze(dateCommentList=yearsCommentList, analyzer=pluginInstance, methodName=u'analyzeYear'):
                        history.setdefault(date, {}).setdefault(u'year', []).extend(messages)
                    for date, messages in _analyze(dateCommentList=allCommentList, analyzer=pluginInstance, methodName=u'analyzeAll'):
                        history.setdefault(date, {}).setdefault(u'all', []).extend(messages)
                except (ArithmeticError, AssertionError, AttributeError, EOFError, LookupError, NameError, SyntaxError, TypeError, ValueError):
                    logger.error(traceback.format_exc())

        with output.createInstance(options.get(u'output')) as out:
            out.write(history)

def _analyze(dateCommentList, analyzer, methodName):
    """
    プラグインのメソッドを直接呼びだすとプラグインの実装によっては
    strやlistが返ってこない事があるため
    """
    history = []
    for date, rows in dateCommentList:
        messages = analyzer.__getattribute__(methodName)(date, rows)
        if messages:
            if isinstance(messages, str) or isinstance(messages, unicode):
                messages = [messages]

            history.append((date, itertools.ifilter(_decoder, messages)))

    return history

def _decoder(message):
    if isinstance(message, str):
        return message.decode(u'utf-8')
    elif isinstance(message, unicode):
        return message
    else:
        return

if __name__ == '__main__':
    main(dict(type = u'nwhois', community = u'co317507', output = None))
