#coding: UTF-8

from niconama_history import common_db
import datetime
import unittest

class CommonDbTest(unittest.TestCase):
    def setUp(self):
        commentList = [
            # communityId, liveId, userId, name, message, option, date
            (u'1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
            (u'1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
            (u'1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
            (u'1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
            (u'1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
            (u'1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
            (u'1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
            (u'1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
        ]

        commonDb = common_db.CommonDb()
        commonDb.__enter__()
        commonDb.insertComment(commentList)

        self.commonDb = commonDb

    def tearDown(self):
        self.commonDb.__exit__(None, None, None)

    def test_SelectDay(self):
        # arrange
        expectedList = [
            (datetime.datetime(2011, 1, 1, 0, 0), [
                common_db.Comment(u'1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
            ]),
            (datetime.datetime(2011, 1, 31, 0, 0), [
                common_db.Comment(u'1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
                common_db.Comment(u'1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
            ]),
            (datetime.datetime(2011, 2, 1, 0, 0), [
                common_db.Comment(u'1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
                common_db.Comment(u'1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
            ]),
            (datetime.datetime(2012, 1, 1, 0, 0), [
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
            ]),
        ]

        # act
        actualList = self.commonDb.selectDays()

        # assert
        for expected, actual in zip(expectedList, actualList):
            (eDate, eList) = expected
            (aDate, aList) = actual
            self.assertEqual(eDate, aDate)
            for item1, item2 in zip(eList, aList):
                self.assertEqual(item1, item2)

    def test_selectMonthes(self):
        # arrange
        expectedList = [
            (datetime.datetime(2011, 1, 31, 0, 0), [
                common_db.Comment(u'1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
                common_db.Comment(u'1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
                common_db.Comment(u'1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
            ]),
            (datetime.datetime(2011, 2, 28, 0, 0), [
                common_db.Comment(u'1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
                common_db.Comment(u'1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
            ]),
            (datetime.datetime(2012, 1, 31, 0, 0), [
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
            ]),
        ]

        # act
        actualList = self.commonDb.selectMonthes()

        # assert
        for expected, actual in zip(expectedList, actualList):
            (eDate, eList) = expected
            (aDate, aList) = actual
            self.assertEqual(eDate, aDate)
            for item1, item2 in zip(eList, aList):
                self.assertEqual(item1, item2)

    def test_selectYears(self):
        # arrange
        expectedList = [
            (datetime.datetime(2011, 12, 31, 0, 0), [
                common_db.Comment(u'1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
                common_db.Comment(u'1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
                common_db.Comment(u'1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
                common_db.Comment(u'1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
                common_db.Comment(u'1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
            ]),
            (datetime.datetime(2012, 12, 31, 0, 0), [
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
            ]),
        ]

        # act
        actualList = self.commonDb.selectYears()

        # assert
        for expected, actual in zip(expectedList, actualList):
            (eDate, eList) = expected
            (aDate, aList) = actual
            self.assertEqual(eDate, aDate)
            for item1, item2 in zip(eList, aList):
                self.assertEqual(item1, item2)

    def test_selectAll(self):
        # arrange
        expectedList = [
            (datetime.datetime(9999, 12, 31, 0, 0), [
                common_db.Comment(u'1', u'lv1', u'1', u'user1', u'message1', None, u'2011-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv1', u'2', u'user2', u'message2', None, u'2011-01-01 00:00:02'),
                common_db.Comment(u'1', u'lv2', u'1', u'user1', u'message3', None, u'2011-01-31 00:00:01'),
                common_db.Comment(u'1', u'lv2', u'3', u'user3', u'message4', u'184', u'2011-01-31 00:00:02'),
                common_db.Comment(u'1', u'lv3', u'1', u'user1', u'message5', None, u'2011-02-01 00:00:01'),
                common_db.Comment(u'1', u'lv3', u'3', u'user3', u'message6', u'184', u'2011-02-01 00:00:02'),
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message7', None, u'2012-01-01 00:00:01'),
                common_db.Comment(u'1', u'lv4', u'4', u'user4', u'message8', None, u'2012-01-01 00:00:02'),
            ]),
        ]

        # act
        actualList = self.commonDb.selectAll()

        # assert
        for expected, actual in zip(expectedList, actualList):
            (eDate, eList) = expected
            (aDate, aList) = actual
            self.assertEqual(eDate, aDate)
            for item1, item2 in zip(eList, aList):
                self.assertEqual(item1, item2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
