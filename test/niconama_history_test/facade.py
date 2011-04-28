from niconama_history import facade
import unittest

class _decoderTest(unittest.TestCase):
    def test_MessageIsStr(self):
        # ararnge
        message = 'hoge'

        # act
        actual = facade._decoder(message)

        # assert
        self.assertEqual(u'hoge', actual)

    def test_MessageIsUnicode(self):
        # arrange
        message = u'hoge'

        # act
        actual = facade._decoder(message)

        # assert
        self.assertEqual(u'hoge', actual)

    def test_MessageIsNotText(self):
        #arrange
        message = 10

        # act
        actual = facade._decoder(message)

        # assert
        self.assertIsNone(actual)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
