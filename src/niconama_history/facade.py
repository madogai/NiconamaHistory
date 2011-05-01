#-*- coding:utf-8
from common_db import CommonDb
from niconama_history import comment_viewer, output, module_loader, plugin_base
import inspect
import itertools
import logging
import traceback
logger = logging.getLogger('default')

def main(**options):
    """
    メイン関数
    各種コメビュログを読み込んで、共通DBにいれて、解析して、出力します。

    :params dictionary options: オプションの辞書
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
        for module in module_loader.load_modules(u'plugins'):
            for plugin in filter(lambda member: issubclass(member, plugin_base.PluginBase) and member is not plugin_base.PluginBase ,zip(*inspect.getmembers(module, inspect.isclass))[1]):
                try:
                    pluginInstance = plugin()
                    logger.info(u'{0}モジュールの、{1}プラグインで解析しています。'.format(pluginInstance.__module__, pluginInstance.__class__.__name__))
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
    プラグインでコメントを解析します。
    """
    history = []
    for date, rows in dateCommentList:
        messages = analyzer.__getattribute__(methodName)(date, rows)
        if messages:
            if isinstance(messages, str) or isinstance(messages, unicode):
                messages = [messages]

            history.append((date, itertools.ifilter(_decode, messages)))

    return history

def _decode(message):
    """
    unicode文字列を返します。
    引数が文字列でない場合空文字列を返します。

    :returns: unicode文字列

    >>> _decode('hoge')
    u'hoge'
    >>> _decode(u'hoge')
    u'hoge'
    >>> _decode(0)
    u''
    """
    if isinstance(message, str):
        return message.decode(u'utf-8')
    elif isinstance(message, unicode):
        return message
    else:
        return u''

if __name__ == '__main__':
    import doctest
    doctest.testmod()