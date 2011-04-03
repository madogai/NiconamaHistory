#-*- coding:utf-8
from niconama_history import Main, CommentViewer
from optparse import OptionParser

def main():
    options = _loadOption()
    viewer = CommentViewer.createInstance(options.type)
    viewer.saveConfig(options)

    Main.main(community = options.community, type = options.type, output = options.output, quiet = options.quiet)

def _loadOption():
    optionParser = OptionParser()
    optionParser.add_option('-t', '--type', default='nwhois', help=u'インポート元のコメントビューア。nwhois, ncv, ankoが指定可能')
    optionParser.add_option('-p', '--path', default=None, help=u'コメントファイルのパス。デフォルト以外の場所にファイルがある場合に使用')
    optionParser.add_option('-u', '--user', default=None, help=u'ユーザーファイルのパス。デフォルト以外の場所にファイルがある場合に使用')
    optionParser.add_option('-c', '--community', help=u'解析するコミュニティのID')
    optionParser.add_option('-o', '--output', default=None, help=u'出力先ファイル。未指定の場合は標準出力に出力')
    optionParser.add_option('-q', '--quiet', action='store_true', dest='quiet', help=u'処理中のメッセージを非表示')
    return optionParser.parse_args()[0]

if __name__ == '__main__':
    main()
