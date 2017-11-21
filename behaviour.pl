hasValue('sensor1', S1) :- perceptionNorth([['Pioneer_p3dx_ultrasonicSensor1', S1], _, _, _, _, _, _, _]).
hasValue('sensor2', S2) :- perceptionNorth([_, ['Pioneer_p3dx_ultrasonicSensor2', S2], _, _, _, _, _, _]).
hasValue('sensor3', S3) :- perceptionNorth([_, _, ['Pioneer_p3dx_ultrasonicSensor3', S3], _, _, _, _, _]).
hasValue('sensor4', S4) :- perceptionNorth([_, _, _, ['Pioneer_p3dx_ultrasonicSensor4', S4], _, _, _, _]).
hasValue('sensor5', S5) :- perceptionNorth([_, _, _, _, ['Pioneer_p3dx_ultrasonicSensor5', S5], _, _, _]).
hasValue('sensor6', S6) :- perceptionNorth([_, _, _, _, _, ['Pioneer_p3dx_ultrasonicSensor6', S6], _, _]).
hasValue('sensor7', S7) :- perceptionNorth([_, _, _, _, _, _, ['Pioneer_p3dx_ultrasonicSensor7', S7], _]).
hasValue('sensor8', S8) :- perceptionNorth([_, _, _, _, _, _, _, ['Pioneer_p3dx_ultrasonicSensor8', S8]]).

takeDecision('North') :-
    hasValue('sensor2', 'False'), hasValue('sensor3', 'False'), hasValue('sensor4', 'False'),
    hasValue('sensor5', 'False'), hasValue('sensor6', 'False'), hasValue('sensor7', 'False'), !.

takeDecision('West') :-
    hasValue('sensor1', 'False'), !.

takeDecision('Est') :-
hasValue8('sensor8', 'False').
