# Filename: CSC223f23CSVassn1.py
# ************************************************************
# Author:     D. Parson
# Student coauthor: Marcello Feliciano
# Major:      CS&IT professor
# Creation Date: 7/29/2023
# Due Date: 9/29/2023
# Course:     CSC223 Fall 2023
# Professor Name: D. Parson
# Assignment: #1
# Input: First command line arg is a pseudo-random number seed, mandatory.
# Input: 2nd, optional command line arg for output file name,
#       default to CSC223f23CSVassn1.csv
# Input: CSC223f23CSVpre1.csv's name is hard coded in __main__, read as a CSV
#       file. This script adds columns to that CSC223f23CSVpre1.csv data and
#       writes the expanded table as its output file.
# Output: Named file per Input with a single column of statistical data.
# In this assignment I created the lists using the provided data. I used the generators A and B for for lists A-I. 
# I combined the lists and created a for loop to append new rows. Finally I outputted it to a text file to read the data.
# STUDENT 1: 5% Complete documentation at top of CSC223f23CSVassn1.py.
# Fill in the blank fields in the above header and replace the
# above blank line with a 1-paragraph description of your work in this
# assignment file.
# ************************************************************

import sys          # Used for argv command line arguments
import random       # For its statistical distribution generators.
from math import log2  # For example compression of exponential distribution.
import numpy as np  # For its statistical distribution generators.
import csv
from statistics import mean, median, mode, pstdev
# ^^^ multimode not available in earlier libraries, mode throws a
# StatisticsError on multiple modes; pstdev is *population* standard deviation.

def generateDistributionTable(seed, statsfilename, startingTable,
        numberOfRows=1024):
    '''
    Generate a table of pseudo-random statistical distributions,
    one per column, with the actual distributions hard coded into
    generateDistributionTable.
    Input seed is the pseudo-random seed value for the generators.

    Input parameter startingTable is the output
    CSV data from CSC223f23CSVpre1.py containing random.uniform
    in column 0 and numpy.random.Generator.uniform in column 1,
    in the range [0, 100] for random.uniform and [0, 100) for
    numpy.random.Generator.uniform. startingTable[0] is
    the first row of the incoming CSV data which contains coumn headings.
    HEADINGS            GENARATOR
    'RndUniform'        random.uniform(0, 100)
    https://docs.python.org/3.7/library/random.html
    'NPUniform'         numpy.random.Generator.uniform(0, 100, numberOfRows)
    https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator

    STUDENT 2 40% Distributions you must add with their headings & generators
    appear below. See CSC223f23CSVpre1.py for the 'RndUniform' and 'NPUniform'
    headings and their generators in Python modules random and numpy, found in
    function generateDistributionTable. Make sure to convert the distributions
    to int() as I did for RndUniform and NPUniform. int(FLOATVALE) truncates
    the fraction and constructs an int object. You can call the variables
    listC, listD, etc. or whatever you want, just like listA and listB in
    CSC223f23CSVpre1.py. Make sure to invoke getstats with the correct args
    as in CSC223f23CSVpre1.py; see reffiles/CSC223f23CSVassn1.txt for
    the correct naming conventions.
    You have to merge the incoming startingTable and your
    preliminary result table into a single table by gluing each pair
    of rows into a single result row. See STUDENT 3 below.
    MAKE SURE TO RUN GENERATORS AND RECEIVE DISTRIBUTIONS IN THIS ORDER:
    If you change the order you will come into different regions of the
    pseudo-random sequences for each generator and get different results.

    'RndNormal10'       See generatorA.uniform(0, 100) from CSC223f23CSVpre1.py
                        except use normalvariate generator with a mu (mean)
                        of 50 and a sigma (standard deviation) of 10.
                        This generates a normal (a.k.a. Gaussian or bell-shaped)
                        distribution. Note how far down and up the samples go.
        See https://www.mathsisfun.com/data/standard-normal-distribution.html
        for discussion of how Standard Deviations apply to normal distributions.
    'NPNormal10'        See generatorB.uniform(0, 100, numberOfRows)
                        except use normal generator with a loc (mean) of 50,
                        a scale (standard deviation) of 10, and a size of
                        numberOfRows. This generates a normal distribution.
                        Note how far down and up the samples go.
    'RndNormal20'       See generatorA.uniform(0, 100) from CSC223f23CSVpre1.py
                        except use normalvariate generator with a mu (mean)
                        of 50 and a sigma (standard deviation) of 20.
                        This generates a normal (a.k.a. Gaussian or bell-shaped)
                        distribution. Note how far down and up the samples go.
    'NPNormal20'        See generatorB.uniform(0, 100, numberOfRows)
                        except use normal generator with a loc (mean) of 50,
                        a scale (standard deviation) of 20, and a size of
                        numberOfRows. This generates a normal distribution.
                        Note how far down and up the samples go.
    'RndExponent10'     See generatorA.uniform(0, 100) from CSC223f23CSVpre1.py
                        except use expovariate generator with a lambd
                        parameter of 1.0/10.0 (i.e., 0.1).
                        This generates an exponential distribution with
                        half the samples <= 10.0.
                        Note how far down and up the samples go.
        See https://www.mathsisfun.com/sets/function-exponential.html
    'NPExponent10'      See generatorB.uniform(0, 100, numberOfRows)
                        except use exponential generator with a scale of 10.0
                        for the halfway point (mean) of generated samples
                        and a size of numberOfRows. This generates an
                        exponential distribution with approximately half the
                        samples between 0.0 and 10.0 inclusive and no
                        predefined upper bound.
                        Note how far down and up the samples go.
    'RndExponent20'     See generatorA.uniform(0, 100) from CSC223f23CSVpre1.py
                        except use expovariate generator with a lambd
                        parameter of 1.0/20.0 (i.e., 0.05).
                        This generates an exponential distribution with
                        half the samples <= 20.0.
                        Note how far down and up the samples go.
    'NPExponent20'      See generatorB.uniform(0, 100, numberOfRows)
                        except use exponential generator with a scale of 20.0
                        for the halfway point (mean) of generated samples
                        and a size of numberOfRows. This generates an
                        exponential distribution with approximately half the
                        samples between 0.0 and 20.0 inclusive and no
                        predefined upper bound.
                        Note how far down and up the samples go.
    'NPExp20Log2'       Extract round(log2(NPExponent20+min+1), 6) of
                        NPExponent20 values. NPExp20Log2 illustrates how
                        to use logarithms to compress exponential value
                        ranges to linear ranges. Each argument to log2()
                        is a value from NPExponent20+min(NPExponent20)+1.
                        The reason for the +min(NPExponent20)+1 argument
                        to log2() is to avoid an undefined negative arg.

    Input statsfilename is the name of a text file for reporting
    statistics count, mean, median, mode, and pstdev rounds to 2 places.
    Input numberOfRows is the number of rows of output data, i.e.,
    number of values from each generator, defaulting to 1024.
    Output return value is the resulting table consisting of an outer list
    of rows, where each row is one sample from each distribution generator.
    '''
    def getstats(dataname, datalist, statsfilehndl):
        '''
        Helper function to format and write stats for multiple data lists.
        dataname is name of generator, datalist is the list of numeric
        data, and statsfilehndl is the open file handle for sys.write.
        '''
        minstr = str(round(min(datalist),2))
        maxstr = str(round(max(datalist),2))
        meanstr = str(round(mean(datalist),2))
        medianstr = str(round(median(datalist),2))
        try:
            modestr = str(round(mode(datalist),2))
        except Exception as oops:
            modestr = 'None'
        pstdevstr = str(round(pstdev(datalist),2))
        countstr = str(len(datalist))
        statsfilehndl.write(dataname + ' statistics:\n')
        statsfilehndl.write('    count = ' + countstr + '\n')
        statsfilehndl.write('    min = ' + minstr + '\n')
        statsfilehndl.write('    max = ' + maxstr + '\n')
        statsfilehndl.write('    mean = ' + meanstr + '\n')
        statsfilehndl.write('    median = ' + medianstr + '\n')
        statsfilehndl.write('    mode = ' + modestr + '\n')
        statsfilehndl.write('    pstdev = ' + pstdevstr + '\n')
    statsfileh = open(statsfilename, 'w')
    generatorA = random.Random(seed)    # constructs a Random generator object
    # STUDENT USE generatorA for all the Rnd distributions.
    # Do NOT construct additional random.Random objects.
    # https://docs.python.org/3.7/library/random.html
    generatorB = np.random.default_rng(seed=seed) # factory for Generator
    # STUDENT USE generatorB for all the NP distributions.
    # Do NOT construct additional random.Random objects.
    # https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator
    # generatorB.uniform allows you to get the entire list in one call,
    # but there is no parameter for rounding. We can use the anonymous
    # function or a named function -- here the anonymous lambda expression
    # to round(value, 2) to two decimal places; I settled on int(value)
    # to discard the fraction and construct an int object for cleaner
    # visualization as a histogram of integer counts. The map() function
    # returns a generator that iterates over generatorB.uniform's returned
    # sequence of generated values; wrapping list() around the Map() call
    # converts the map generator's results to a Python list.
    # CSC223f23CSVpre1.py: listA = [int(generatorA.uniform(0, 100))
        # for i in range(0,numberOfRows)]
    # getstats('RndUniform, seed = ' + str(seed), listA, statsfileh)
    # Above LIST COMPREHENSION IS EQUIVALENT TO THIS for loop:
    # listA = []
    # for i in range(0,numberOfRows):
    #   listA.append(int(generatorA.uniform(0, 100)))
    # CSC223f23CSVpre1.py: listB = list(map(lambda value : int(value),
        # generatorB.uniform(0, 100, numberOfRows)))
    # getstats('NPUniform, seed = ' + str(seed), listB, statsfileh)
    # print('DEBUG listA', listA[0:10])
    # print('DEBUG listB', listB[0:10])
    # STUDENT 2 work can go here:
    listA = [int(generatorA.normalvariate(50, 10)) for i in range(0,numberOfRows)]
    getstats('RndNormal10, seed = ' + str(seed), listA, statsfileh)
    listB = [int (generatorB.normal(50, 10, 1)[0])for i in range(0,numberOfRows)]
    getstats('NPNormal10, seed = ' + str(seed), listB, statsfileh)
    listC = [int(generatorA.normalvariate(50, 20)) for i in range(0,numberOfRows)]
    getstats('RndNormal20, seed = ' + str(seed), listC, statsfileh)
    listD = [int (generatorB.normal(50, 20, 1)[0]) for i in range(0,numberOfRows)]
    getstats('NPNormal20, seed = ' + str(seed), listD, statsfileh)
    listE = [int (generatorA.expovariate(0.1)) for i in range(0,numberOfRows)]
    getstats('RndExponent10, seed = ' + str(seed), listE, statsfileh)
    listF = [int (generatorB.exponential(10.0, 1)[0]) for i in range(0,numberOfRows)]
    getstats('NPExponent10, seed = ' + str(seed), listF, statsfileh)
    listG = [int (generatorA.expovariate(0.05)) for i in range(0,numberOfRows)]
    getstats('RndExponent20, seed = ' + str(seed), listG, statsfileh)
    listH = [int (generatorB.exponential(20, 1)[0]) for i in range(0,numberOfRows)]
    getstats('NPExponent20, seed = ' + str(seed), listH, statsfileh)
    listI = [round(log2(value+min(listH) + 1), 6) for value in listH]
    getstats('NPExp20Log2, seed = ' + str(seed), listI, statsfileh) 
    
    result = list(zip(listA, listB, listC, listD, listE, listF, listG, listH, listI))    # zip also returns a generator
    result.insert(0, ('RndUniform', 'NPUniform')) # headings for the columns
    return result
    statsfileh.close()

    # STUDENT 3 15% Combine the incoming startingTable and your preresult table
    # into a single result table to return from this function.
    # After constructing a zipped table of all of your distribution lists
    # and prepending the columns headings as I did for CSC223f23CSVpre1.py:
    # result = list(zip(listA, listB))    # zip also returns a generator
    # result.insert(0, ('RndUniform', 'NPUniform')) # headings for the columns
    # You must then combine the two separate tables into one table and return
    # it. Here is an interactive example I typed up in Python:
    # >>> table1
    # [('RndUniform', 'NPUniform'), (67, 96), (30, 30), (6, 23), (79, 97)]
    # >>> table2
    # [('Happy', 'Camper'), (1, 11), (2, 22), (3, 33), (4, 44)]
    # >>> result = []
    # >>> for index in range(0,len(table1)):
#        # This requires them to have same number of rows.
#         result.append(list(table1[index]) + list(table2[index]))
#   >>> result
#   [('RndUniform', 'NPUniform', 'Happy', 'Camper'), (67, 96, 1, 11),
#       (30, 30, 2, 22), (6, 23, 3, 33), (79, 97, 4, 44)]
# The above example uses the list() converter in case one of the subrows
# being added via '+' is a tuple and the other a list. They need to be the
# same type:
# In [5]: table1
# Out[5]: ((1, 2, 3), (11, 22, 33))
# In [6]: table2
# Out[6]: [[111, 222, 333], [-1, -2, -3]]
# In [7]: result = []
# In [8]: for index in range(0,len(table1)):
#           result.append(table1[index] + table2[index])
#                 TypeError: can only concatenate tuple (not "list") to tuple
# In [9]: for index in range(0,len(table1)):
#           result.append(list(table1[index]) + list(table2[index]))
# In [10]: result
# Out[10]: [[1, 2, 3, 111, 222, 333], [11, 22, 33, -1, -2, -3]]

    result = [('Delete', 'This', 'Line'), (10, 20, 30), (400, 500, 600)]
    return result

def readStartingTable(startingCSVdatafile):
    '''
    Read the CSV data table in named file startingCSVdatafile and
    return it using a csv.reader object to perform input.
    STUDENT 4 20% Must replace explicit line parsing with a csv.reader
    See example code in histogram.py around lines 17 and 18.
    Use this kind of list comprehension to read the whole thing in one line:
    table = [row for row in incsv] # This iterates over incsv's generator.
    You could also use a for loop to iterate over csv.reader incsv.
    All of the cells read via csv.reader are strings, but there is no
    need to convert the non-heading rows' cells to numbers, since they
    are just being loaded here, joined with the normal and exponential
    numeric columns generated in this file, and written. These input
    cells appear identically in the output, i.e., we are not doing any
    numeric calculations with them here.
    '''
    result = []
    datafile = open(startingCSVdatafile, 'r')
    for line in datafile:
        fields = line.strip().split(',')    # strip trailing \n
        # breaks line into list across commas
        result.append(fields)
    datafile.close()    # ALWAYS! close files when done with them.
    return result

__usage__ = 'USAGE: python CSC223f23CSVassn1.py SEED [ OUTFILE.csv ]'
# Symbol names with __underline__ should be private to their context.
if __name__ == '__main__':      # Entry code outside of any function.
    if len(sys.argv) < 2 or len(sys.argv) > 3: # argv[0] is CSC223f23CSVassn1.py
        raise ValueError(__usage__)
        # https://docs.python.org/3.7/library/exceptions.html
    try:
        seed = int(sys.argv[1])
    except ValueError as badint:
        raise ValueError('Invalid, non-integer SEED on command line: '
            + sys.argv[1] + '\n' + __usage__)
    if len(sys.argv) == 3:
        outcsvname = sys.argv[2]
        if not outcsvname.endswith('.csv'):
            raise ValueError('ERROR, OUTFILE must end in ".csv: "'
                + sys.argv[2] + '\n' + __usage__)
    else:
        outcsvname = 'CSC223f23CSVassn1.csv'
    startingtable = readStartingTable('CSC223f23CSVpre1.csv')
    outcsvfile = open(outcsvname, 'w')
    statsfilename = outcsvname.replace('.csv', '.txt')
    table = generateDistributionTable(seed, statsfilename, startingtable, 100000)
    # START OF WHAT PYTHON'S CSV MODULE WILL MAKE SIMPLER.
    # STUDENT 5 20% Replace the following loop with construction of a 
    # csv.writer object wrapped around outcsvfile and then just calling
    # writerows in a single line of code. GET RID OF THIS LOOP BELOW.
    # Here is an example from a spring 2021 course:
    # summarycsvfile = open('csc458ensemble5sp2021.summary.csv', 'w')
    # summarycsv = csv.writer(summarycsvfile, delimiter=',', quotechar='"')
    # summarycsvhdr = ['testkey', 'testdatatype', 'kappa', 'MAE', 'RMSE',
    #    'Instances', 'runtime', 'cputime']
    #    summarycsv.writerow(summarycsvhdr)
    # In your case a single call to writerows() (plural) writes all rows.
    # Make sure to close the file when completed.
    for row in table:
        for cell in row[0:len(row)-1]: # Append ',' to all but the last col.
            outcsvfile.write(str(cell) + ',')   # Must convert to string
        outcsvfile.write(str(row[-1]) + '\n')   # [-1] is last element
    outcsvfile.close()  # always do this to ensure final writes get flushed
    sys.exit(0)         # 0 means NO ERROR in Unix & related environments
