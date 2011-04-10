#-*- coding:utf-8

from niconama_history.plugin_base import PluginBase
import re

class CommentFilter(PluginBase):
    """
    放送開始日を抽出するプラグインです。
    """
    def analyzeDay(self, date, rows):
        def replaceEducation(row):
            name = row.name if row.name else u'名無しさん'
            match = re.search(u'教育\\s*?[\\(（](.+?)=(.+?)[\\）)]', row.message)
            return u'{0}が 『{1}』 を 『{2}』 と教育しました。'.format(name, match.group(1), match.group(2))

        educationRows = filter(lambda row: re.match(u'教育\\s*?[\\(（].+?=.+?[\\）)]', row.message), rows)
        return map(replaceEducation ,educationRows)

if __name__ == '__main__':
    pass