#-*- coding:utf-8
from niconama_history import facade, comment_viewer
from optparse import OptionParser
import logging.config
import re
import sys

def main():
    try:
        sysEncode = sys.stdin.encoding
    except AttributeError:
        sysEncode = u'ascii'

    (options, args) = _loadOption()
    isInteractiveMode = options.community is None
    if isInteractiveMode:
        (communityId, viewerType) = _readInteractive(sysEncode)
        options.community = communityId
        options.type = viewerType

    viewer = comment_viewer.createInstance(options.type)
    viewer.saveConfig(options)

    if options.quiet:
        logging.getLogger(u'default').setLevel(logging.WARNING)

    facade.main(community = options.community, type = options.type, output = options.output, quiet = options.quiet)
    if isInteractiveMode:
        raw_input(u'')

def _readInteractive(sysEncode):
    """
    """
    communityId = raw_input(u'コミュニティID(ex. co317507):'.encode(sysEncode)).decode(sysEncode)
    viewerType = raw_input(u'コメントビューワ[nwhois/ncv/anko]:'.encode(sysEncode)).decode(sysEncode)

    if not re.match(ur'co\d+', communityId):
        print u'コミュニティIDの形式が間違っています。'.encode(sysEncode)
        sys.exit()

    return (communityId, viewerType)

def _loadOption():
    optionParser = OptionParser()
    optionParser.add_option(u'-c', u'--community', help=u'コミュニティID')
    optionParser.add_option(u'-t', u'--type', default=u'nwhois', help=u'インポート元のコメントビューア。nwhois, ncv, ankoが指定可能')
    optionParser.add_option(u'-p', u'--path', default=None, help=u'コメントファイルのパス。デフォルト以外の場所にファイルがある場合に使用します')
    optionParser.add_option(u'-u', u'--user', default=None, help=u'ユーザーファイルのパス。デフォルト以外の場所にファイルがある場合に使用します')
    optionParser.add_option(u'-o', u'--output', default=None, help=u'出力先ファイル。未指定の場合は標準出力')
    optionParser.add_option(u'-q', u'--quiet', action=u'store_true', dest=u'quiet', help=u'サイレントモードで動作します')
    return optionParser.parse_args()

if __name__ == '__main__':
    logging.config.fileConfig(u'logging.conf')
    main()
