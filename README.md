# IntSim
A Python-based simulation tool to evaluate intersection control policies

This code is provided as three stand-alone Python based simulations, one for each traffic control policy. The code assumes a single intersection with two one-way roads - one going East-West and one going North-South. 


StaticTrafficControlPolicy.py : policy 1 - in case of conflict at the intersection, always allow traffic in one of the directions through

RandomTrafficControlPolicy.py : policy 2 - in case of conflict at the intersection, choose either direction of traffic with 50 percent probability

DynamicTrafficControlPolicy.py : policy 3 - in case of conflict at the intersection, choose the direction of traffic with the higher congestion to pass through


The following are the key simulation parameters: 

Tsim - the number of time steps until a traffic jam occurs. When it occurs, the trial run will break out of the current loop and continue on to the next trial.

N - a parameter that determines how "long" each road is. The car will move one space down the N-spaced road during each time step of Tsim.

p - the probability that a new car enters the road each Tsim, which controls traffic load on each side of the road.

