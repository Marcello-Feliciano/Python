# DataflowGeneratorsDAG.py D. Parson Fall 2023
# demonstrate a non-preemptive dataflow using Python coroutines
# in a DAG that has forks out from a source to multiple downstream
# generators and also multiple inputs to a file sync at the end.
# Compare to DataflowGeneratorsNoFeedback.py that uses straight
# generators, not coroutines.
import sys
import string   # to get character types
# https://docs.python.org/3/library/string.html
import random
import tempfile
import time
from functools import reduce
# https://docs.python.org/3.0/library/functools.html

def genASCII(ID, maxStringLength, stringsPerPacket,
        totalCountOfDataPackets, TraceFile, seed=220223523):
    '''
    genASCII is a regular generator, not a coroutine,
    because it generates its own "input data".

    ID is a unique int per generator to aid debugging.

    generate totalCountOfDataPackets of strings from length 1 to
    maxStringLength, create a temporary file for each packet
    containing stringsPerPacket strings, one per line, and yield
    the handle to the temporary file which the receiver must close.
    There will be totalCountOfDataPackets files created. This
    is inefficient and is being used for demo purposes.

    TraceFile is an open file handle for writing debug information.
    '''
    rgen = random.Random(seed)
    universe = string.ascii_letters + string.digits + string.punctuation    \
        + '     ' # allow for multiple spaces and tabs between words.
    # https://docs.python.org/3/library/string.html
    # universe does not include tabs, newlines, carriage returns, form feeds
    for packet in range(0, totalCountOfDataPackets):
        tmpfile = tempfile.TemporaryFile(mode='w+', newline='',
            dir='.', suffix='.tmp') # useful for debugging
        # w+ makes it writable, and readable further down in the dataflow
        # https://docs.python.org/3/library/tempfile.html#tempfile-examples
        for scount in range(0, stringsPerPacket):
            slen = rgen.randint(1,maxStringLength)
            s = ''
            for sstep in range(0,slen):
                s += universe[rgen.randint(0,len(universe)-1)]
            TraceFile.write('DEBUG s: ' + str(s) + '\n')
            tmpfile.write(s + '\n')
        tmpfile.flush()
        # tmpfile.seek(0) # read pointer at start for next dataflow stage
        # ^^^ NO! When there is > 1 receiver, they need to do the seek(0)!
        yield(tmpfile)

def genASCII2Count(ID, charFilter, TraceFile):
    '''
    genASCII2Count is a coroutine because its caller pushes data from
    an upstream generator to it via send().

    ID is a unique int per generator to aid debugging.

    charFilter is a Python filter function used to pass only certain characters.
    genASCII2Count's yield returns a 3-tuple:
        (linecount, wordcount, charcount)
    as in the Unix "wc" utility. The counts are after applying charFilter.
    '''
    f = yield 0 # input f as the first output of genASCII, 0 is just filler
    f.seek(0)
    # for f in predecessor:
    while f:
        lines = []
        for line in f.readlines():
            line = line.strip()
            if line:        # Not Blank.
                l = ''.join(filter(charFilter, line))
                # filter returns a sequence of single chars,
                # and ''.join joins them into a string
                if l:   # filter may have created an empty string
                    lines.append(l)
                    TraceFile.write('DEBUG genASCII2Count: ' + str(l) + '\n')
        linecount = len(lines)
        wordcount = 0
        charcount = 0
        for l in lines:
            charcount += len(l)
            words = l.split(' ')
            for w in words:
                if w:   # don't count empty strings which are adjacent spaces
                    wordcount += 1
        f = yield ((linecount, wordcount, charcount)) # __main__ feeds me data
        f.seek(0)

def sinkOutput2File(ID, outputFileHandle):
    '''
    sinkOutput2File is a coroutine because its caller pushes data from
    an upstream generator to it via send().

    ID is a unique int per generator to aid debugging.

    sinkOutput2File writes output from predecessor into outputFileHandle
        and also yields it, both after converting to str().
    sinkOutput2File does not close outputFileHandle at the end.

    TraceFile is an open file handle for writing debug information.
    '''
    data = yield 0  # __main_ send my input, this "primes the pump"
    # for data in predecessor:
    while data:
        mydata = str(data)
        outputFileHandle.write(mydata + '\n')
        data = yield(mydata)

if __name__ == '__main__':
    tracefile = open(sys.argv[1], 'w', newline='')
    gen1 = genASCII(1, 15, 10, 5, tracefile)
    gen2 = genASCII2Count(2, lambda x : True, tracefile) # no filtering
    gen3 = sinkOutput2File(3, tracefile)
    def filterAlphaNumerics(charToFilter):
        constraint = string.ascii_letters + string.digits + ' '
        return charToFilter in constraint
    gen4 = genASCII2Count(4, filterAlphaNumerics, tracefile)
    gen2.__next__() # advance to first yield
    gen3.__next__() # advance to first yield
    gen4.__next__() # advance to first yield
    # PUSH data through the pipeline
    for gen1data in gen1:
        gen2data = gen2.send(gen1data)
        gen3data = gen3.send(gen2data)
        gen4data = gen4.send(gen1data)
        gen3data = gen3.send(gen4data)
    # Following NOT needed because gen3 writes to a file.
    # for gen2data in gen2:
        # gen3.send(gen2data)
    # for gen3data in gen3:
        # pass
    tracefile.close()
