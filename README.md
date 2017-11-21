# prothonics-vrep
Python 3 robot that gets sensor data from V-REP simulator and takes decisions by making queries to a SWI-Prolog program (act method has not been implemented yet). I used Pioneer P3-DX V-REP model for the robot, but you can easily replace it with the model you prefer just changing the names and the arrangement of the sensors (both in Python and in Prolog program).


V-REP robot simulator, SWI-Prolog and PySWIP Python library are needed: 
-  http://www.coppeliarobotics.com/
-  http://www.swi-prolog.org/
-  https://github.com/yuce/pyswip


Like any V-REP project, you have to put the following files in "SWIPrologPythonRobotForVREP" directory, in order to run it:
-  vrep.py
-  vrepConst.py
-  the appropriate remote API library: "remoteApi.dll" (Windows), "remoteApi.dylib" (Mac) or "remoteApi.so" (Linux)
-  simpleTest.py (or any other example file)
