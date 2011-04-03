#-*- coding:utf-8
from niconama_history import Main, CommentViewer
from optparse import OptionParser
import os.path

def main():
    if os.path.exists('NiconamaHistory.conf') == False:
        CommentViewer.initializeConfig()

    options = loadOption()
    viewer = CommentViewer.createInstance(options.type)
    viewer.saveConfig(options)

    Main.main(community = options.community, type = options.type, output = options.output, quiet = options.quiet)

def loadOption():
    optionParser = OptionParser()
    optionParser.add_option('-t', '--type', default='nwhois', help='インサート元のコメントビューア。nwhois, ncv, ankoが指定可能')
    optionParser.add_option('-p', '--path', default=None, help='コメントファイルのパス。デフォルト以外の場所にファイルがある場合に使用')
    optionParser.add_option('-u', '--user', default=None, help='ユーザーファイルのパス。デフォルト以外の場所にファイルがある場合に使用')
    optionParser.add_option('-c', '--community', help='解析するコミュニティのID')
    optionParser.add_option('-o', '--output', default=None, help='出力先ファイル。未指定の場合は標準出力に出力')
    optionParser.add_option('-q', '--quiet', action='store_false', dest='quiet', help='処理中のメッセージを非表示')
    return optionParser.parse_args()[0]

if __name__ == '__main__':
    main()
