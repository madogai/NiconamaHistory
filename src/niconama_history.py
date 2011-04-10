#-*- coding:utf-8
from niconama_history import facade, comment_viewer
from optparse import OptionParser
import logging.config
import re
import sys

def main():
    try:
        sysEncode = sys.stdin.decode
    except AttributeError:
        sysEncode = u'ascii'

    (options, args) = _loadOption()
    if options.community is None:
        (communityId, viewerType) = _readInteractive()
        options.community = communityId.decode(sysEncode)
        options.type = viewerType.decode(sysEncode)

    viewer = comment_viewer.createInstance(options.type)
    viewer.saveConfig(options)

    if options.quiet:
        logging.getLogger(u'default').setLevel(logging.WARNING)

    facade.main(community = options.community, type = options.type, output = options.output, quiet = options.quiet)

def _readInteractive():
    """
    """
    communityId = raw_input(u'コミュニティID co:')
    viewerType = raw_input(u'コメントビューワ[nwhois/ncv/anko]:')

    if not re.match(ur'\d+', communityId):
        print u'コミュニティIDの形式が間違っています。(ex. co317507)'
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
