#-*- coding:utf-8
from ConfigParser import SafeConfigParser
from niconama_history import Main
from optparse import OptionParser

def main():
    optionParser = OptionParser()
    optionParser.add_option('-t', '--type', default='nwhois')
    optionParser.add_option('-p', '--path', dest='filepath')
    (options, args) = optionParser.parse_args()

    config = SafeConfigParser()
    config.read('config.ini')

    Main.main()

if __name__ == '__main__':
    main()
