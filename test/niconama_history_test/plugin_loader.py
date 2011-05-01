#-*- coding:utf-8

from niconama_history import plugin_loader
import unittest

class _plugin_loaderTest(unittest.TestCase):
    def test_ModuleLoadIsSuccess(self):
        # arrange
        module_name = u'plugin_loader'
        basepath = u'./'

        # act
        actual = plugin_loader._load_module(module_name, basepath)

        # assert
        self.assertEqual('plugin_loader', actual.__name__)

class load_pluginsTest(unittest.TestCase):
    def test_LoadPluginTestFolder(self):
        # arrange
        pluginDir = u'../plugins_test'

        # act
        modules = plugin_loader.load_modules(pluginDir)
        actual = map(lambda module: module.__name__, modules)

        # assert
        self.assertListEqual(['mockPlugin1', 'mockPlugin2'], actual)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
