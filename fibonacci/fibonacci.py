# -*- coding: utf-8 -*-
"""
/*
 * Software License Agreement (BSD License)
 *
 * Copyright (c) 2019 Oliver Mayer, Akademie der Bildenden Kuenste Nuernberg. 
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 
 * - Redistributions of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 * - Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
 

Iteration vs recursion: Sums and Fibonacci numbers
https://en.wikipedia.org/wiki/Fibonacci_number

required modules:
    pygame   https://pypi.org/project/pygame/
    numpy    https://pypi.org/project/numpy/
 
"""

import sys
import getopt


def sumIterative(N, printSteps):
    sum = 0

    if printSteps:
        print("0", end="")

    for i in range(1, N+1):
        if printSteps:
            print(" +", i, end="")
        sum += i
    
    return sum


def sumRecursive(N, printSteps):

    if N == 0:
        if printSteps:
            print("0", end="")
        return 0
    else:
        if printSteps:
            print(N, " + ( ", end="")
    
        val = N + sumRecursive(N-1, printSteps)
    
        if printSteps:
            print(" )", end="")
        return val

        



# iterative fibonacci computation
def fibonacciIterative(N, printSteps):
    fn = [0]
    if printSteps:
        print( fn[len(fn) - 1], "", end="")

    if (N >= 1):
        fn.append(1)
        if printSteps:
            print( fn[len(fn) - 1], "", end="")

    if N > 1:
        for i in range(2, N+1):
            fn.append(fn[i-1] + fn[i-2])
            if printSteps:
                print( fn[len(fn) - 1], "", end="")

    return fn


# recursive fibonacci computation
def fibonacciRecursive(N, printSteps):
    fn = -1

    if N == 0:
        if printSteps:
            print("0", end="")
        fn = 0
    elif N == 1:
        if printSteps:
            print("1", end="")
        fn = 1
    else:
        if printSteps:
            print(" ( ", end="")

        fn1 = fibonacciRecursive(N-1, printSteps) 

        if printSteps:
            print("  +  ", end="")

        fn2 = fibonacciRecursive(N-2, printSteps)
        
        if printSteps:
            print(" ) ", end="")

        fn = fn1 + fn2

        if printSteps:
            print("=", fn, end="")
        else:
            print(fn, "")


    return fn



computeFibonacci = 0
useRecursive = 0
n = 0

# parse commandline arguments

if len(sys.argv) != 4:
    print("Usage: ", sys.argv[0], " operation use_recursive N")
    print("  operation:     'sum' for sum from 1 to N or 'fib' for N-th fibonacci number")
    print("  use_recursive: 0 for iterative computation, 1 for recursive computation")
    print("  N:             integer > 0")
    sys.exit()


computeFibonacci = (sys.argv[1] == "fib")
useRecursive = int(sys.argv[2])
n = int(sys.argv[3])


# compute

if computeFibonacci:
    print("Computing Fibonacci number from 0 to N =", n)

    if useRecursive != 0:
        print("Using recursive algorithm")
        fibonacciRecursive(n, True)
    else:
        print("Using iterative algorithm")
        fibonacciIterative(n, True)

else:
    print("Computing sum over numbers 0 to N =", n)

    if useRecursive != 0:
        print("Using recursive algorithm")
        sum = sumRecursive(n, True)
        print(" =", sum)
    else:
        print("Using iterative algorithm")
        sum = sumIterative(n, True)
        print(" =", sum)







