# coding : utf-8

'''
Copyright 2017-2018 Agnese Salutari.
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on 
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and limitations under the License
'''

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

    def act(self, command, dParams):
        '''
        Implements action commands in the robot world
        :param command: action command to execute
        :param dParams: action parameters
        :return: True is action was actuated
        '''
        assert isinstance(command, str)
        assert isinstance(dParams, dict)
        out = True
        pass
        # TODO: implement
        return out

    def sense(self, sensorName):
        '''
        Implements sensor reading from the robot simulator
        :param sensorName: name of the sensor as defined in the simulator
        :return: out:
            The 1st element of out is the state of the reading on the sensor (0 os ok).
            The 2nd element of out is a Boolean that says if the sensor is detecting something in front of it.
            The 3rd element of out is the point of the detected object.
            The 4th element of out is the handle of the detected object.
            The 5th element of out is the normal vector of the detected surface.
        '''
        assert isinstance(sensorName, str)
        state, handle = vrep.simxGetObjectHandle(self.__clientID, sensorName, vrep.simx_opmode_blocking)
        out = vrep.simxReadProximitySensor(self.__clientID, handle, vrep.simx_opmode_blocking)
        return out

    def close(self):
        '''
        Close connection with the robot simulation
        :return:
        '''
        # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
        vrep.simxGetPingTime(self.__clientID)
        # Now close the connection to V-REP:
        vrep.simxFinish(self.__clientID)


class RobotBrain(object):

    '''
    The main intelligent controller of the simulated robot
    '''
    __prologEngine = Prolog()  # The engine given by Pyswip SWI Prolog library
    __stateN = None  # Sate obtained by observing data received by North sensors,
    __stateS = None  # State obtained by observing data received by South sensors
        # Example: [['Pioneer_p3dx_ultrasonicSensor1', 'False'], ['Pioneer_p3dx_ultrasonicSensor2', 'True'],
        # ['Pioneer_p3dx_ultrasonicSensor3', 'True'], ['Pioneer_p3dx_ultrasonicSensor4', 'True'],
        # ['Pioneer_p3dx_ultrasonicSensor5', 'True'], ['Pioneer_p3dx_ultrasonicSensor6', 'True'],
        # ['Pioneer_p3dx_ultrasonicSensor7', 'True'], ['Pioneer_p3dx_ultrasonicSensor8', 'False']]
    # List of default North sensors
    __proximitySensorsN = ['Pioneer_p3dx_ultrasonicSensor1', 'Pioneer_p3dx_ultrasonicSensor2',
                           'Pioneer_p3dx_ultrasonicSensor3', 'Pioneer_p3dx_ultrasonicSensor4',
                           'Pioneer_p3dx_ultrasonicSensor5', 'Pioneer_p3dx_ultrasonicSensor6',
                           'Pioneer_p3dx_ultrasonicSensor7', 'Pioneer_p3dx_ultrasonicSensor8']
    # List of default South sensors
    __proximitySensorsS = ['Pioneer_p3dx_ultrasonicSensor9', 'Pioneer_p3dx_ultrasonicSensor10',
                           'Pioneer_p3dx_ultrasonicSensor11', 'Pioneer_p3dx_ultrasonicSensor12',
                           'Pioneer_p3dx_ultrasonicSensor13', 'Pioneer_p3dx_ultrasonicSensor14',
                           'Pioneer_p3dx_ultrasonicSensor15', 'Pioneer_p3dx_ultrasonicSensor16']
    __velocityList = [5, 10, 15, 20, 25]  # List of velocities from the lowest to the higher
    __decision = None  # The next action to perform

    def __init__(self, proximitySensorsN=[], proximitySensorsS=[]):
        if len(proximitySensorsN) > 0:
            self.setProxinitySensorsN(proximitySensorsN)
        if len(proximitySensorsS) > 0:
            self.setProxinitySensorsS(proximitySensorsS)

    def setStateN(self, newStateN):
        assert isinstance(newStateN, list)
        assert len(newStateN) == len(self.getProximitySensorsN())
        for elem in newStateN:
            assert isinstance(elem, list)
            assert len(elem) == 2
        self.__stateN = newStateN

    def setStateS(self, newStateS):
        assert isinstance(newStateS, list)
        assert len(newStateS) == len(self.getProximitySensorsS())
        for elem in newStateS:
            assert isinstance(elem, list)
            assert len(elem) == 2
        self.__stateS = newStateS

    def getStateN(self):
        return self.__stateN

    def getStateS(self):
        return self.__stateS

    def getProximitySensorsN(self):
        return self.__proximitySensorsN

    def getProximitySensorsS(self):
        return self.__proximitySensorsS

    def setProxinitySensorsN(self, newProximitySensorsN):
        assert isinstance(newProximitySensorsN, list)
        for elem in newProximitySensorsN:
            assert isinstance(elem, str)
        self.__proximitySensorsN = newProximitySensorsN

    def setProxinitySensorsS(self, newProximitySensorsS):
        assert isinstance(newProximitySensorsS, list)
        for elem in newProximitySensorsS:
            assert isinstance(elem, str)
        self.__proximitySensorsS = newProximitySensorsS

    def getDecision(self):
        return self.__decision

    def setDecision(self, newDecision):
        assert isinstance(newDecision, str)
        assert newDecision in ['North', 'South', 'East', 'West', 'Stay']
        self.__decision = newDecision

    def learn(self, prologFilePath):
        '''
        Learns from a SWI Prolog file.
        :param prologFilePath: The path of the Prolog (.pl or .txt) file we need to use.
        :return:
        '''
        assert isinstance(prologFilePath, str)
        self.__prologEngine.consult(prologFilePath)

    def singlePerception(self, externalInput):
        '''
        Read state and build a part of world representation (given only one sensor).
        :param externalInput : what is at the sensor layer:
            [sensorID, [sensorReading]], where:
                sensorID is a string.
                [sensorReading] is a tuple of 5 elements:
                    The 1st element is the state of the reading on the sensor (0 os ok).
                    The 2nd element is a Boolean that says if the sensor is detecting something in front of it.
                    The 3rd element is the point of the detected object.
                    The 4th element is the handle of the detected object.
                    The 5th element is the normal vector of the detected surface.
        :return: what does the robot percept as happened:
            ['<sensorID>', '<sensorReading_second_element>'] if we have a perception from sensor works,
            ['<sensorID>', 'None'] otherwise.
        '''
        # print(externalInput)  # Test
        assert isinstance(externalInput, list)
        assert isinstance(externalInput[0], str)
        assert isinstance(externalInput[1], tuple)
        assert len(externalInput[1]) == 5
        if externalInput[1][0] == 0:  # If sensor returns state_ok
            out = [externalInput[0], str(externalInput[1][1]).replace('"', "'")]
            # The escape is very important for Prolog
        else:
            out = [externalInput[0], 'None']
        return out

    def globalPerception(self, externalInputsList):
        '''
        Read state and build a world representation
        :param A list of externalInputs. An externalInput is what is at the sensor layer:
            [sensorID, [sensorReading]], where:
                sensorID is a string.
                [sensorReading] is a list of 5 elements:
                    The 1st element is the state of the reading on the sensor (0 os ok).
                    The 2nd element is a Boolean that says if the sensor is detecting something in front of it.
                    The 3rd element is the point of the detected object.
                    The 4th element is the handle of the detected object.
                    The 5th element is the normal vector of the detected surface.
        :return: what does the robot percept as happened: [sensorID, sensorReading_second_element] the perception
            from sensor works, None otherwise.
        '''
        assert isinstance(externalInputsList, list)
        out = []
        for input in externalInputsList:
            out.append(self.singlePerception(input))
        return out

    def decision(self):
        '''
        The state contains the worlds representation
        :return: action
        '''
        self.__prologEngine.retractall('perceptionNorth(_)')
        self.__prologEngine.assertz('perceptionNorth(' + str(self.getStateN()) + ')')
        try:
            out = list(self.__prologEngine.query('takeDecision(D)'))
        except:  # Il Prolog doesn't work (maybe because it can't receive data from sensors) the robot has to stay
            out = []
        # print(out)  # test
        if len(out) > 0 :  # If we can take more than one decision, we take the 1st one
            # print(out[0]['D'])  # Test
            toDo = out[0]['D']
        else:
            toDo = 'Stay'
        self.setDecision(toDo)
        return toDo

    def thinkN(self, sensorReadings):
        '''
        It decides with action to take given North sensor readings
        :param sensorReadings: list of sensor values, that is a list of externalInputs.
            An externalInput is what is at the sensor layer:
            [sensorID, [sensorReading]], where:
                sensorID is a string.
                [sensorReading] is a list of 5 elements:
                    The 1st element is the state of the reading on the sensor (0 os ok).
                    The 2nd element is a Boolean that says if the sensor is detecting something in front of it.
                    The 3rd element is the point of the detected object.
                    The 4th element is the handle of the detected object.
                    The 5th element is the normal vector of the detected surface.
        :return: action
        '''
        assert isinstance(sensorReadings, list)
        self.setStateN(self.globalPerception(sensorReadings))
        action = self.decision()
        return action
