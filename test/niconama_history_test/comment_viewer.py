from niconama_history import comment_viewer
import unittest

class NwhoisTest(unittest.TestCase):
    def setUp(self):
        self.viewer = comment_viewer.Nwhois()

    def test__loadComment(self):
        # arrange
        communityId = u'co1'
        sqlFilePath = u'../data/nwhois/log3.sqlite'
        expected = [
            # communityId, liveId, userId, name, message, option, date
            (u'co1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
            (u'co1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
            (u'co1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
            (u'co1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
            (u'co1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
            (u'co1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
            (u'co1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
            (u'co1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
        ]
        # act
        actual = self.viewer._loadComment(communityId, sqlFilePath)

        # assert
        for tuple1, tuple2 in zip(expected, actual):
            self.assertTupleEqual(tuple1, tuple2)

class NcvTest(unittest.TestCase):
    def setUp(self):
        self.viewer = comment_viewer.NCV()

    def test__loadUserSetting(self):
        # arrange
        communityId = u'co1'
        userSettingFilePath = u'../data/ncv/UserSetting.xml'

        expected = {
            u'1' : u'user1',
            u'2' : u'user2',
            u'3' : u'user3',
            u'4' : u'user4',
        }

        # act
        actual = self.viewer._loadUserSetting(communityId, userSettingFilePath)

        # assert
        self.assertDictEqual(expected, actual)

    def test__loadComment(self):
        # arrange
        communityId = u'co1'
        userSettingFilePath = u'../data/ncv/UserSetting.xml'
        commentLogFolder = u'../data/ncv/'
        expected = [
            # communityId, liveId, userId, name, message, option, date
            (u'co1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
            (u'co1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
            (u'co1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
            (u'co1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
            (u'co1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
            (u'co1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
            (u'co1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
            (u'co1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
        ]

        # act
        actual = self.viewer._loadComment(communityId, userSettingFilePath, commentLogFolder)

        # assert
        for tuple1, tuple2 in zip(expected, actual):
            self.assertTupleEqual(tuple1, tuple2)

class GissiriAnkoTest(unittest.TestCase):
    def setUp(self):
        self.viewer = comment_viewer.GissiriAnko()

    def test__parseComment(self):
        # arrange
        communityId = u'co1'
        liveInfoFilePath = u'../data/anko/nico20110101_1000000001_ticket.xml'
        commentFilePath = u'../data/anko/nico20110101_1000000001_xml.txt'
        expected = [
            (u'co1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
            (u'co1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
        ]

        # act
        actual = self.viewer._parseComment(communityId, liveInfoFilePath, commentFilePath)

        # assert
        for tuple1, tuple2 in zip(expected, actual):
            self.assertTupleEqual(tuple1, tuple2)

    def test__loadComment(self):
        # arrange
        communityId = u'co1'
        logFolderPath = u'../data/anko/'
        expected = [
            # communityId, liveId, userId, name, message, option, date
            (u'co1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
            (u'co1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
            (u'co1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
            (u'co1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
            (u'co1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
            (u'co1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
            (u'co1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
            (u'co1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
        ]

        # act
        actual = self.viewer._loadComment(communityId, logFolderPath)

        # assert
        for tuple1, tuple2 in zip(expected, actual):
            self.assertTupleEqual(tuple1, tuple2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()