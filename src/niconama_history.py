#-*- coding:utf-8
from niconama_history import facade, comment_viewer
from optparse import OptionParser
import sys

def main():
    (options, args) = _loadOption()
    if len(args) == 0:
        print u'コミュニティIDを引数に指定する必要があります。'
        sys.exit()

    viewer = comment_viewer.createInstance(options.type)
    viewer.saveConfig(options)

    community = args[0]

    facade.main(community = community, type = options.type, output = options.output, quiet = options.quiet)

def _loadOption():
    optionParser = OptionParser()
    optionParser.add_option('-t', '--type', default='nwhois', help=u'インポート元のコメントビューア。nwhois, ncv, ankoが指定可能')
    optionParser.add_option('-p', '--path', default=None, help=u'コメントファイルのパス。デフォルト以外の場所にファイルがある場合に使用します')
    optionParser.add_option('-u', '--user', default=None, help=u'ユーザーファイルのパス。デフォルト以外の場所にファイルがある場合に使用します')
    optionParser.add_option('-o', '--output', default=None, help=u'出力先ファイル。未指定の場合は標準出力')
    optionParser.add_option('-q', '--quiet', action='store_true', dest='quiet', help=u'サイレントモードで動作します')
    return optionParser.parse_args()

if __name__ == '__main__':
    main()
