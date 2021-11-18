from pysat.solvers import Glucose3
import itertools
import pprint
import numpy as np
from pysat.pb import *
import math
from utils import *
import argparse

def parse_args():
    # Params
    parser = argparse.ArgumentParser(description='PyTorch DnCNN')
    parser.add_argument('--input', type=str , help='input file path')
    parser.add_argument('--print_clause',action = 'store_true')
    return parser.parse_args()

N = 9
D = 3 #Grid size

clues = [
'000000010',
'400000000',
'020000000',
'000050407',
'008000300',
'001090000',
'300400200',
'050100000',
'000806000']

digits = {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}

args = parse_args()

if args.input:
	file_name = args.input
	clues = []
	with open(file_name, "r") as f:
		for line in f.readlines():
			assert len(line.strip()) == N, "'"+line+"'"
			for c in range(0, N):
				assert(line[c] in digits.keys() or line[c] == '0')
			clues.append(line.strip())
	print(len(clues))
	assert(len(clues) == N)

arr_clues = np.array(clues)
print("Input sudoku board: ")
print_sudoku(arr_clues)

log_n = math.log(N,2)
log_n = math.ceil(log_n)
num_var = N*N*N
new_var = N*N*log_n 
print("Number of new variable for binary encoding: " + str(new_var))

# Build the clauses in a list
cls = []  # The clauses: a list of integer lists
for r in range(1,N+1): # r runs over 1,...,N
    for c in range(1, N+1):
        # The cell at (r,c) has at least one value
        cls.append([var(r,c,v,N) for v in range(1,N+1)])
        # The cell at (r,c) has at most one value
        for v in range(1,N+1):
            temp_cls = AMO_binary(r,c,v,log_n,num_var,N)
            for cl in temp_cls:
                cls.append(cl)

for v in range(1, N+1):
    # Each row has the value v
    for r in range(1, N+1):
        cls.append([var(r,c,v,N) for c in range(1,N+1)])
    # Each column has the value v
    for c in range(1, N+1):
        cls.append([var(r,c,v,N) for r in range(1,N+1)])
    # Each subgrid has the value v
    for sr in range(0,D):
        for sc in range(0,D):
            cls.append([var(sr*D+rd,sc*D+cd,v,N)
                        for rd in range(1,D+1) for cd in range(1,D+1)])
# The clues must be respected
for r in range(1, N+1):
    for c in range(1, N+1):
        if clues[r-1][c-1] in digits.keys():
            cls.append([var(r,c,digits[clues[r-1][c-1]],N)])

# Output the DIMACS CNF representation
# Print the header line
print("p cnf %d %d" % (N*N*N, len(cls)))
# Print the clauses
if args.print_clause:
	for c in cls:
	    print(" ".join([str(l) for l in c])+" 0")

g = Glucose3()
for c in cls:
    g.add_clause(c)
print(g.solve())
result = g.get_model()
if g.solve() == True:
	decoded = decode(result,num_var,N)

	result_sudoku = np.zeros([N,N], dtype = int)

	for data in decoded:
	    r = int(data[0])
	    c = int(data[1])
	    v = data[2]
	    result_sudoku[r-1][c-1] = v

	print_sudoku(result_sudoku)
else:
	print("UNSAT")