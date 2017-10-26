'''
Module for creating a Solver object for each constituent solver of the
portfolio by automatically generating the src/pfolio_solvers.py file,
according to the conventions specified in the README file of this folder.
'''

import os
import sys

SUNNY_HOME = os.path.realpath(__file__).split('/')[:-2]
SUNNY_HOME = '/'.join(SUNNY_HOME)
pfolio_path = SUNNY_HOME + '/solvers.py'
pfolio_file = open(pfolio_path, 'w')

preamble = """'''
This module contains an object of class Solver for each installed solver of the 
portfolio. Each object of class Solver might be
defined manually, but it is however strongly suggested to first generate
it automatically by using the make_pfolio.py script in solvers folder. 
Then, once the file is created, it is possible to customize each object. 
Note that running make_pfolio.py script will replace the current file.
'''

class Solver(object):
    # Solver name. It must be an unique identifier.
    name = ''
    # Absolute path of the folder containing solver-specific redefinitions.
    mznlib = ''
    # Absolute path of the command used for executing a FlatZinc model.
    fzn_exec = ''
    # Solver-specific FlatZinc translation of the MiniZinc constraint "LHS < RHS".
    constraint = ''
    # Solver-specific option for printing all the solutions (for CSPs only) or all
    # the sub-optimal solutions (for COPs only).
    all_opt = ''
    # Solver-specific option for free search (i.e., to ignore search annotations).
    free_opt = ''    
    # Solver-specific option for statistics output.
    statistics = ''    
    # Solver-specific option for time-bounded search.
    time_limit = 0
"""
pfolio_file.write(preamble + '\n\n')

solvers_path = SUNNY_HOME + '/solvers/'
solvers = os.walk(solvers_path).next()[1]
for solver in solvers:
    print('Adding solver', solver)
    pfolio_file.write(solver + ' = Solver()\n')
    pfolio_file.write(solver + ".name = '" + solver + "'\n")
    pfolio_file.write(
        solver + ".mznlib = '" + solvers_path + solver + "/mzn-lib'\n"
    )
    pfolio_file.write(
        solver + ".fzn_exec = '" + solvers_path + solver + "/fzn-exec'\n"
    )
    opts = open(solvers_path + solver + '/opts', 'r')
    for line in opts:
        pfolio_file.write(solver + '.' + line)
    pfolio_file.write('\n')

pfolio_file.write('solvers = [' + ', '.join(solvers) + ']\n')
