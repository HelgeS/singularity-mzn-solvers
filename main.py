import argparse
import os
import re
import shutil
import solvers
import subprocess
import tempfile
import time


def post_constraint(mzn, dzn_name, objective_var, lb=None, ub=None, objvalsel=None, objvalselplaceholder='{{OBJVALSEL}}', hard_lb=False, hard_ub=False):
    mzn_base = os.path.basename(mzn)
    mzn_new = tempfile.NamedTemporaryFile(delete=False, prefix='{}-{}-'.format(mzn_base, dzn_name), suffix='.mzn').name

    mzn_content = open(mzn, 'r').read()

    has_lb = lb is not None
    has_ub = ub is not None

    if not has_lb and not has_ub:
        new_constraint = ""
    elif has_lb and has_ub and hard_lb and hard_ub:
        assert (lb <= ub)

        if lb == ub:
            new_constraint = "constraint {obj} = {bound:d};\n".format(obj=objective_var, bound=ub)
        else:
            new_constraint = "constraint {lb:d} <= {obj} /\ {obj} <= {ub:d};\n".format(lb=lb, ub=ub,
                                                                                       obj=objective_var)
    elif has_ub and hard_ub:
        new_constraint = "constraint {obj} <= {ub:d};\n".format(ub=ub, obj=objective_var)
    elif has_lb and hard_lb:
        new_constraint = "constraint {lb:d} <= {obj};\n".format(lb=lb, obj=objective_var)
    else:
        # We add a search annotation
        new_constraint = "% Boundary Estimation labeling" + os.linesep
        boundvars = []

        if has_ub and not hard_ub:
            new_constraint += "var bool: estimatedUpperBound;" + os.linesep
            new_constraint += "constraint estimatedUpperBound -> objective <= min(max({ub}, lb(objective)), ub(objective));".format(ub=ub)
            new_constraint += os.linesep
            boundvars.append("estimatedUpperBound")

        if has_lb and not hard_lb:
            new_constraint += "var bool: estimatedLowerBound;" + os.linesep
            new_constraint += "constraint estimatedLowerBound -> objective >= max(min({lb}, ub(objective)), lb(objective));".format(lb=lb)
            new_constraint += os.linesep
            boundvars.append("estimatedLowerBound")

        # TODO Adjust search order depending on maximization/minimization problem
        annotation = "ann: boundestann = bool_search([{}], input_order, indomain_max, complete);".format(", ".join(boundvars))

        mzn_content = mzn_content.replace("ann: boundestann;", annotation)

    if objvalsel:
        # Also set value selection heuristic for the objective variable

        if objvalselplaceholder in mzn_content:
            mzn_content = mzn_content.replace(objvalselplaceholder, objvalsel)
        else:
            new_search = "int_search([objective], input_order, {}, complete".format(objvalsel)
            if "int_search([objective], input_order, indomain_min, complete)" in mzn_content:
                mzn_content = mzn_content.replace("int_search([objective], input_order, indomain_min, complete)", new_search)
            elif "int_search([objective], input_order, indomain_max, complete)" in mzn_content:
                mzn_content = mzn_content.replace("int_search([objective], input_order, indomain_max, complete)", new_search)

    if new_constraint:
        mzn_content += os.linesep + new_constraint
    
    open(mzn_new, 'w').write(mzn_content)

    return mzn_new


parser = argparse.ArgumentParser()
parser.add_argument('mzn', help='Path to minizinc model')
parser.add_argument('-d', '--dzn', help='Path to data file', default="")
parser.add_argument('-lb', '--lowerbound', type=int, default=None, help='Lower bound for objective variable')
parser.add_argument('-ub', '--upperbound', type=int, default=None, help='Upper bound for objective variable')
parser.add_argument('--hard-lb', action='store_true', default=False, help="Post lower bound as hard constraint (search annotation otherwise)")
parser.add_argument('--hard-ub', action='store_true', default=False, help="Post upper bound as hard constraint (search annotation otherwise)")
parser.add_argument('-s', '--solver', choices=[s.name for s in solvers.solvers], default='chuffed')
parser.add_argument('-t', '--timeout', type=int, default=0, help='Timeout for solver (in seconds; mzn2fzn not included; 0: disabled)')
parser.add_argument('-f', '--free', action='store_true', default=False, help='Free search')
parser.add_argument('-a', '--all', action='store_true', default=False, help='List all solutions')
parser.add_argument('-c', '--comment', default=None, help='Comment which will be added to output')
parser.add_argument('-o', '--output', default=None, help='Output file for stdout and stderr')
parser.add_argument('-var', '--variable', default='objective', help='Name of objective variable')
parser.add_argument('-single-sol', action='store_true', default=False, help='Only return first solution')
parser.add_argument('-objvalsel', default=None, help="Objective variable value selection heuristic (must be supported by model)")
args = parser.parse_args()
print('Args: {}'.format(args))

solver = next((s for s in solvers.solvers if s.name == args.solver))

if args.dzn:
    dzn_name = os.path.splitext(os.path.basename(args.dzn))[0]
else:
    dzn_name = ''

mzn_new = post_constraint(args.mzn, dzn_name, args.variable, args.lowerbound, args.upperbound, args.objvalsel, args.hard_lb, args.hard_ub)
fzn = mzn_new.replace('.mzn', '.fzn')
ozn = mzn_new.replace('.mzn', '.ozn')

# mzn2fzn
cmd = 'mzn2fzn -I ' + solver.mznlib + ' ' + mzn_new + ' ' + args.dzn + ' -o ' + fzn + ' -O ' + ozn
start = time.time()
subprocess.call(cmd.split())
mzn2fzn_duration = time.time() - start

# flatzinc
fzn_options = solver.statistics.split()

if args.timeout > 0:
    fzn_options.extend(solver.time_limit.format(args.timeout).split())

if args.free:
    fzn_options.append(solver.free_opt)

if args.all:
    fzn_options.append(solver.all_opt)

if args.single_sol:
    fzn_options.extend(solver.single_sol.split())

start = time.time()
cmd = [solver.fzn_exec] + fzn_options + [fzn]
print(cmd)
solver_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.call(['solns2out', '--output-time', ozn], stdin=solver_process.stdout)
solver_process.wait()

print(solver_process.stderr.read().decode())

fzn_duration = time.time() - start

print('Time_mzn2fzn: {:.2f}'.format(mzn2fzn_duration))
print('Time_solver: {:.2f}'.format(fzn_duration))

os.unlink(mzn_new)

