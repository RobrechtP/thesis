# Using the Observation History of a Robot to Recognize Temporal Effects in Its Environment and Adapt Its Behavior

All code used for my master's thesis. This includes many scratch files, unused results and dummy code, for which I apologise. To get an understanding of the actual code please refer to the main.py file in the src directory. This annoted code was used to execute the experiments. The POMDP models can found in the domains dir. Specifically the 4x4MDP.POMDP, 4x4.POMDP and 6x6MDP.POMDP files show the domain variations used in the experiments.

POMDP representation code of mbforbes was used and adapted: 
https://github.com/mbforbes/py-pomdp

POMDP solving happens using included SolvePOMDP solver: 
https://www.erwinwalraven.nl/solvepomdp/

The src/solver.config file configures Gurobi as LP solver. Add (licensed) Gurobi jar to lib folder or configure it for another supported LP solver to run an experiment.
