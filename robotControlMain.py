# coding : utf-8
import time
import RobotWorld

def main():
    DELAY = 0.001 # in seconds
    #Se il Delay è piccolo, il cervello è più veloce ma consuma più CPU -> dobbiamo bilanciare il tutto,
    #facendo di volta in volta verifiche (metodo euristico).

    simWorld = RobotWorld.World(host='127.0.0.1', portNumber=19997)
    robBrain = RobotWorld.RobotBrain()
    robBrain.learn('behaviour.pl')
    connectionState = simWorld.connect()
    while connectionState == -1:
        print('Trying to connect to V-REP Simulator...')
        connectionState = simWorld.connect()
    print('Connected to V-REP Simulator.')
    stepCount = 1
    while True:
        print('################## Step: ' + str(stepCount) + ' ##################')
        northPerceptions = []
        for ns in robBrain.getProximitySensorsN():
            data = simWorld.sense(ns)
            northPerceptions.append([ns, data])
        print('State:')
        print(robBrain.getStateN())
        robBrain.thinkN(northPerceptions)
        print('Robot Decision:')
        print(robBrain.getDecision())
        stepCount += 1
        time.sleep(DELAY)

if __name__ == '__main__':
    main()
