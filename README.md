# docker-mzn-solvers

Tools to generate Docker or Singularity containers with minizinc and several compatible solvers.

The structure and the scripts are closely adapted from SUNNY-CP (https://github.com/CP-Unibo/sunny-cp), 
but there is no functionality for portfolio solving, feature extraction or anything else. If you need this, go to SUNNY-CP.

This container is targeted to run one solver on one instance (mzn + dzn) with an optional time limit and the option to output the solver statistics.
That's all.
