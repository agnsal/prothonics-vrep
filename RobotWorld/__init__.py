# coding : utf-8

import time
import os
import ctypes as ct
import platform
import vrepConst
from pyswip import Prolog

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')


class World(object):

    '''
    Robot simulator class to communicate with the simulation environment
    '''

    __host = None
    __portNumber = None
    __clientID = None

    def __init__(self, host='127.0.0.1', portNumber=19997):
        self.__host = host
        self.__port = portNumber

    def connect(self):
        '''
        Connect with V-REP Simulator.
        :return: True if the connection has been established, False otherwise.
        '''
        # just in case, close all opened connections
        vrep.simxFinish(-1)
        # Connect to V-REP
        self.__clientID = vrep.simxStart(self.__host, self.__port, True, True, 5000, 5)
        # check clientID for a good connection...
        if self.__clientID == -1:
            return False
        else:
            return True
