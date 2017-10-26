import argparse
import os
import shutil
import solvers
import subprocess
import tempfile
import time


def post_constraint(mzn, dzn_name, objective_var, lb=0, ub=0):
    if lb and ub:
        assert (lb <= ub)

        if lb == ub:
            new_constraint = "constraint {obj} = {bound:d};\n".format(obj=objective_var, bound=ub)
        else:
            new_constraint = "constraint {lb:d} <= {obj} /\ {obj} <= {ub:d};\n".format(lb=lb, ub=ub,
                                                                                       obj=objective_var)
    elif ub:
        new_constraint = "constraint {obj} <= {ub:d};\n".format(ub=ub, obj=objective_var)
    elif lb:
        new_constraint = "constraint {lb:d} <= {obj};\n".format(lb=lb, obj=objective_var)
    else:
        new_constraint = ""

    mzn_base = os.path.basename(mzn)
    mzn_new = tempfile.NamedTemporaryFile(delete=False, prefix='{}-{}-'.format(mzn_base, dzn_name), suffix='.mzn').name

    shutil.copy(mzn, mzn_new)
    open(mzn_new, 'a').write(new_constraint)

    return mzn_new


parser = argparse.ArgumentParser()
parser.add_argument('mzn', help='Path to minizinc model')
parser.add_argument('-d', '--dzn', help='Path to data file')
parser.add_argument('-lb', '--lowerbound', type=int, default=None, help='Lower bound for objective variable')
parser.add_argument('-ub', '--upperbound', type=int, default=None, help='Upper bound for objective variable')
parser.add_argument('-s', '--solver', choices=[s.name for s in solvers.solvers], default='chuffed')
parser.add_argument('-t', '--timeout', type=int, default=0, help='Timeout for solver (in seconds; mzn2fzn not included; 0: disabled)')
parser.add_argument('-f', '--free', action='store_true', default=False, help='Free search')
parser.add_argument('-a', '--all', action='store_true', default=False, help='List all solutions')
parser.add_argument('-c', '--comment', default=None, help='Comment which will be added to output')
parser.add_argument('-o', '--output', default=None, help='Output file for stdout and stderr')
parser.add_argument('-var', '--variable', default='objective', help='Name of objective variable')
args = parser.parse_args()
print('Args: {}'.format(args))

solver = next((s for s in solvers.solvers if s.name == args.solver))

if args.dzn:
    dzn_name = os.path.splitext(os.path.basename(args.dzn))[0]
else:
    dzn_name = ''

mzn_new = post_constraint(args.mzn, dzn_name, args.variable, args.lowerbound, args.upperbound)
fzn = mzn_new.replace('.mzn', '.fzn')

# mzn2fzn
cmd = 'mzn2fzn -I ' + solver.mznlib + ' ' + mzn_new + ' ' + args.dzn + ' -o ' + fzn
start = time.time()
subprocess.call(cmd.split())
mzn2fzn_duration = time.time() - start

# flatzinc
fzn_options = solver.statistics.split()

if args.timeout > 0:
    fzn_options.append(solver.time_limit.format(args.timeout))

if args.free:
    fzn_options.append(solver.free_opt)

if args.all:
    fzn_options.append(solver.all_opt)

cmd = [solver.fzn_exec] + fzn_options + [fzn]
print(cmd)
start = time.time()
subprocess.call(cmd)
fzn_duration = time.time() - start

print('Time_mzn2fzn: {:.2f}'.format(mzn2fzn_duration))
print('Time_solver: {:.2f}'.format(fzn_duration))

os.unlink(mzn_new)

