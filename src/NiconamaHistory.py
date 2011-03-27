#-*- coding:utf-8
from niconama_history import Main, CommentViewer
from optparse import OptionParser
import os.path

def main():
    if os.path.exists('config.ini') == False:
        CommentViewer.initializeConfig()

    options = loadOption()
    viewer = CommentViewer.createInstance(options.type)
    viewer.saveConfig(options)

    Main.main(options.community, options.type)

def loadOption():
    optionParser = OptionParser()
    optionParser.add_option('-t', '--type', default='nwhois')
    optionParser.add_option('-p', '--path', default=None)
    optionParser.add_option('-u', '--user', default=None)
    optionParser.add_option('-c', '--community')
    return optionParser.parse_args()[0]

if __name__ == '__main__':
    main()
