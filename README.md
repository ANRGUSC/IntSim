# IntSim
A Python-based simulation tool to evaluate intersection control policies

This code is provided as three stand-alone Python based simulations, one for each traffic control policy. The code assumes a single intersection with two one-way roads - one going East-West and one going North-South. 


StaticTrafficControlPolicy.py : policy 1 - in case of conflict at the intersection, always allow traffic in one of the directions through

RandomTrafficControlPolicy.py : policy 2 - in case of conflict at the intersection, choose either direction of traffic with 50 percent probability

DynamicTrafficControlPolicy.py : policy 3 - in case of conflict at the intersection, choose the direction of traffic with the higher congestion to pass through


