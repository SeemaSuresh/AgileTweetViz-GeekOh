'''
Name: Setup.py
Description: This file is responsible for creating windows command line exe.
Developer - Harsha Kadekar & Yash
reference - http://logix4u.net/component/content/article/27-tutorials/44-how-to-create-windows-executable-exe-from-python-script
'''

from distutils.core import setup
import py2exe
import numpy
import tweepy
import logging
import zmq.libzmq
import mysql.connector
import mysql.connector.version

setup(console=['HashTagReceiver.py'], options={"py2exe": {'includes': ['zmq.backend.cython'], 'excludes': ['zmq.libzmq'],"dll_excludes": ['libzmq.pyd',
                                                                                                                                          'api-ms-win-core-processthreads-l1-1-2.dll',
                                                                                                                                          'api-ms-win-core-sysinfo-l1-2-1.dll',
                                                                                                                                          'api-ms-win-core-heap-l2-1-0.dll',
                                                                                                                                          'api-ms-win-core-delayload-l1-1-1.dll',
                                                                                                                                          'api-ms-win-core-errorhandling-l1-1-1.dll',
                                                                                                                                          'api-ms-win-core-libraryloader-l1-2-0.dll',
                                                                                                                                          'api-ms-win-core-string-obsolete-l1-1-0.dll',
                                                                                                                                          'api-ms-win-security-activedirectoryclient-l1-1-0.dll']}})