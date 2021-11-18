from pysat.solvers import Glucose3
import itertools
import pprint
import numpy as np
from pysat.pb import *
import math

def var(r, c, v, N):
    assert(1 <= r and r <= N and 1 <= c and c <= N and 1 <= v and v <= N)
    return (r-1)*N*N+(c-1)*N+(v-1)+1

def binary_encoding(v,log_n):
    encoded = []
    variables = np.zeros([log_n],dtype = int)
    bin_val = bin(v-1)[2:]
    bin_val = str(bin_val)
    excess = log_n - len(bin_val)
    for i in range(len(bin_val)):
        variables[excess+i] = bin_val[i]

    return variables

def AMO_binary(r,c,v,log_n,num_var,N):
    cls = []
    y = binary_encoding(v,log_n)
    x = var(r,c,v,N)
    for i in range(log_n):
        new_x = (r-1)*N*log_n+(c-1)*log_n+1 + i + num_var
        val = 0
        if y[i] == 0:
            y_var = -1*new_x
        if y[i] == 1:
            y_var = 1*new_x
        cls.append([-x,y_var])
    return cls

def decode(input_result,num_var,N):
    result = []
    for i in range(1,num_var+1):
        if input_result[i-1] > 0:
            r = int((i-1)/(N*N))
            c = int((i-r*N*N-1)/N)
            v = i-r*N*N-c*N
            result.append([r+1,c+1,v])
    return result

def print_sudoku(board):
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")