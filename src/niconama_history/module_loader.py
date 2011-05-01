#-*- coding:utf-8

import imp
import os
import re

def _load_module(moduleName, basePath):
    """
    モジュールをロードして返します。

    :param string moduleName: モジュール名
    :basePath string モジュールを探索するディレクトリ
    :returns: モジュールインスタンス

    >>> _load_module('plugin_loader', './')
    <module 'plugin_loader' from './plugin_loader.py'>
    """
    fileHandler, fileName, description = imp.find_module(moduleName, [basePath])
    return imp.load_module(moduleName, fileHandler, fileName, description)

def load_modules(moduleDir):
    """
    Pload_modulesストにして返します。

    :param string moduleDir: モジュールを探索するディレクトリ
    :returns: モジュールインスタンスのリスト
    """
    cwd = os.getcwd()
    basepath = os.path.join(cwd, moduleDir)

    pluginList = []
    for fileName in os.listdir(basepath):
        try:
            matchObj = re.match(ur'(^[a-zA-Z].*).py$', fileName)
            if matchObj:
                module = _load_module(matchObj.group(1), basepath)
                pluginList.append(module)
            elif os.path.isdir(fileName):
                module = _load_module(fileName)
                pluginList.append(module)
        except ImportError:
            pass
    return pluginList

if __name__ == '__main__':
    import doctest
    doctest.testmod()
