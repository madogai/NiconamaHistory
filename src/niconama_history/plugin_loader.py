#-*- coding:utf-8
'''
Created on 2011/03/19

@author: madguy
'''
import imp
import os
import re

def load_module(module_name, basepath):
        """
        モジュールをロードして返します。
        """
        fileHandler, fileName, description = imp.find_module(module_name, [basepath])
        return imp.load_module(module_name, fileHandler, fileName, description)

def load_plugins(plugindir):
        """
        Pluginをロードしてリストにして返します。
        """

        cwd = os.getcwd()
        basepath = os.path.join(cwd, plugindir)

        pluginList = []
        for fileName in os.listdir(basepath):
            try:
                matchObj = re.match(r'(^[a-zA-Z].*).py$', fileName)
                if matchObj:
                    module = load_module(matchObj.group(1), basepath)
                    pluginList.append(module)
                elif os.path.isdir(fileName):
                    module = load_module(fileName)
                    pluginList.append(module)
            except ImportError:
                pass
        return pluginList