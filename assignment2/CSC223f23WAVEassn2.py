# Filename: CSC223f23WAVEassn2.py
# ************************************************************
# Author:     D. Parson
# Student coauthor: Marcello Feliciano
# Major:  Game Development    
# Creation Date: 8/8/2023
# Due Date: 10/19/23
# Course:     CSC223 Fall 2023
# Professor Name: D. Parson
# Assignment: #2
#   In this assignment I Outputed the points on different types of graphs to a csv file. 
#this includes triangle, sine, cosine, squre, pulse, risingsaw and falling saw types of graphs.
#I started by calculating the points for each graph then outputting the result to a table.
#finally I used if statements to check for each graph on the table.
# STUDENT 1: 5% Complete documentation at top of CSC223f23WAVEassn2.py.
# Fill in the blank fields in the above header and replace the
# above blank line with a 1-paragraph description of your work in this
# assignment file.
# Input: CSC223f23WaveParams.csv name is hard coded in __main__, read as a
#       CSV file. There are five columns per row in this input file:
#       WaveType Frequency SampleRate Duration DutyCycle, where
# Output: CSC223f23WAVEassn2.csv contains the headers + wave samples,
#       one waveform per column, one sample per row.
#       1. WaveType is one of
#           'triangle'      Triangle wave starting at lowest point at time 0.
#               Signal rises linearly from min value to max value at halfway
#               sample, then falls from max to min by the end.
#           'sine'          Sine wave starting at lowest point at time 0.
#               radians([-90,270] degrees for 1 complete cycle
#               https://www.mathopenref.com/triggraphsine.html
#           'cos'           Cosine wave starting at highest point at time 0.
#               radians([0,360] degrees for 1 complete cycle
#               https://www.mathopenref.com/triggraphcosine.html
#           'square'        Square wave starting at lowest point at time 0.
#                           This is identical to a pulse with 0.5 DutyCycle.
#           'pulse'         Pulse wave starting at min level at time 0.
#                           Final samples are at max level for the DutyCycle.
#           'risingsaw'     Rising sawtooth starting at lowest point at time 0.
#               Signal rises linearly from min value to max value at end.
#           'fallingsaw'    Falling sawtooth starting at HIGH point at time 0.
#               Signal falls linearly from max value to min value at end.
#       2. Frequency is the inverse of period from start of first complete
#           waveform to the start of the next, etc. Frequency is relative
#           to SampleRate. Values must be > 0.0 and <= 20000.0 cycles per second
#           (hertz). Test values (float) are in the range [200.0, 5000.0].
#       3. SampleRate (int) one of 44100, 48000, or 96000 for that many samples
#           per second. SampleRate defines 1 second, and 1.0/Frequency
#           gives the period of a complete cycle in (possibly fractional)
#           seconds.
#       4. Duration (int) of the generated wave data in complete cycles of the
#           waveform, not in time. Given Period in secs for one cycle
#           = (1.0 / Frequency),
#           For the CSC223 assignment 2, Duration-in-cycles=1 to minimize
#           file size. All cycles after the first would be identical unless
#           we add noise or add multiple signals together;
#           we are not doing that.
#       5. DutyCycle is percentage of the cycle spent at the top of the
#          pulse waveform in the range (0.0, 1.0), i.e., a fraction GREATER
#          than 0% and less than 100%. A regular square wave has a
#          DutyCycle=0.5. DutyCycle is ignored for all except pulse wave.
#       https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
#
#       Implementation considerations:
#           In [43]: from math import ceil
#           In [44]: period = 1.0/1000.0
#           In [45]: period # frequency=1000 Hz has period=1 millisecond
#           Out[45]: 0.001
#           In [46]: sampleTime = 1.0 / 44100
#           In [47]: sampleTime     # fractional seconds
#           Out[47]: 2.2675736961451248e-05
#           In [48]: samples = period / sampleTime
#           In [49]: samples
#           Out[49]: 44.1
#           In [50]: ceil(samples)
#           Out[50]: 45
#       If we are generating > 1 Duration cycles of a waveform, we apply
#       ceil() only for the very last sample, and set it at -32767 since
#       that is where we start. Since period is for 1 waveform, for
#       Duration > 1, samples = ceil((period*Duration)/sampleTime).

# ************************************************************
import sys          # Used for argv command line arguments
import csv
from statistics import mean, median, pstdev, stdev
import random       # May inject some random white noise in a later extension.
import math         # from math import ceil, pi, sin, cos
import numpy as np  # For its arrays of type
# https://numpy.org/doc/stable/reference/arrays.html
# https://numpy.org/doc/stable/reference/arrays.scalars.html#numpy.int16
# We will compute each sample in the np.int16 range (-32768, 32767], i.e.,
# [-32767, 32767], to keep it symmetric for later application to .wav file
# generation per SciPy .wav file reading and writing.
# https://docs.scipy.org/doc/scipy/reference/io.html#module-scipy.io.wavfile
# However, the computation will range from [-1.0, 1.0] * 32767.0, with
# rounding to the nearest int and clamping to np.int16 via min() and max().

def __scalePercentToWavRange__(percentAsAFraction):
    assert (percentAsAFraction >= -1.0 and percentAsAFraction <= 1.0),  \
        '__scalePercentToWavRange__ percentAsAFraction outside range '  \
        '[-1.0, 1.0]: ' + str(percentAsAFraction)
    tmp = round(percentAsAFraction * 32767)
    return np.int16(min(max(-32767,tmp), 32767))

def __getstats__(dataname, datalist, statsfilehndl):
    '''
    Helper function to format and write stats for a column of data.
    dataname is name of column, datalist is the vector of numeric
    data, and statsfilehndl is the open file handle for sys.write.
    '''
    minstr = str(round(min(datalist),2))
    maxstr = str(round(max(datalist),2))
    meanstr = str(round(mean(datalist),2))
    medianstr = str(round(median(datalist),2))
    # mode has problems in some versions of the statistics library
    # For the mode since these curves are symmetric,
    # most do not have peaks. Some starting and ending
    # at -32767 will have that as the mode.
#   try:
#       modestr = str(round(mode(datalist),2))
#   except Exception as oops:
#       modestr = 'None'
    try:
        pstdevstr = str(round(pstdev(datalist),2))
        # pstdev and stdev are choking on these data?
    except Exception as oops:
        pstdevstr = 'None'
    countstr = str(len(datalist))
    statsfilehndl.write(dataname + ' statistics:\n')
    statsfilehndl.write('    count = ' + countstr + '\n')
    statsfilehndl.write('    min = ' + minstr + '\n')
    statsfilehndl.write('    max = ' + maxstr + '\n')
    statsfilehndl.write('    mean = ' + meanstr + '\n')
    statsfilehndl.write('    median = ' + medianstr + '\n')
#   statsfilehndl.write('    mode = ' + modestr + '\n')
    statsfilehndl.write('    pstdev = ' + pstdevstr + '\n')

# STUDENT NOTE FOR COMPUTING INDICES INTO THE SAMPLE VECTOR.
# Use "//" integer division or math.floor() or math.ceil() WHERE
# NEEDED to get int (not float) indices into the vector.
# Not all waveform types need that.
def genSamples(wavetype, samples, wavecol, table2D, dutyCycle, statsfileh=None):
    # Each nested helper function has access to input parameters.
    # STUDENT 2: 19% Write function genTri() to generate a triangle wave
    # that starts at the min sample value of -32767
    # (i.e., __scalePercentToWavRange__(-1.0)), rises to 32767 at the
    # halfway sample (__scalePercentToWavRange__(1.0)), then descends to
    # -32767 at the final sample.
    # Add documentation comments below the function declaration
    # as I have for genSine() and genRiseSaw(), per the Output documentation
    # starting below line 18 above for this waveform type.
    
    def genTri(samples, table2D, wavecol):#create Triangle function and calculate 
        halfway = samples // 2            #values for a triangle graph
        increment = (32767 * 2) / halfway
        

        for i in range(samples):
            if i < halfway:
                current_val = -32767 + i * increment
            else:
                current_val = 32767 - (i - halfway) * increment
            table2D[i][wavecol] = int(current_val)  #print to table
        
    def genSine(samples, table2D, wavecol):#create sine function and calculate values for a sine graph
        '''
        Sine wave starting at lowest point at time 0.
        radians([-90,270] degrees for 1 complete cycle
        https://www.mathopenref.com/triggraphsine.html
        '''
        startRadians = - math.pi / 2.0 #2PI is 360 degrees, this is -90
        stepRadians = (2.0 * math.pi) / (samples-1) # full 360 cut into pieces
        curRadians = startRadians
        for step in range(0, samples):
            table2D[step][wavecol] = __scalePercentToWavRange__(
                math.sin(curRadians))
            curRadians += stepRadians
    # STUDENT 3: 19% Write function genCosine() to generate a cosine wave
    # that starts at the max sample value of 32767
    # (i.e., __scalePercentToWavRange__(-1.0)), falls to -32767 at the
    # halfway point (__scalePercentToWavRange__(1.0)), then ascends to
    # 32767 at the final sample. YOU MUST USE THE math.cos() function.
    # Add documentation comments below the function declaration
    # as I have for genSine() and genRiseSaw(), per the Output documentation
    # starting below line 18 above for this waveform type.
    def genCosine(samples, table2D, wavecol):#create cosine function and calculate values for a cosine graph
        radians = (2 * math.pi )/ (samples - 1)
        current_radians = 0
        for i in range(samples):
            cos_value = math.cos(current_radians)
            table2D[i][wavecol] = __scalePercentToWavRange__(cos_value)#print to table
            current_radians += radians
    # STUDENT 4: 19% Write function genSquare() to generate a square wave
    # that starts at the min sample value of -32767
    # (i.e., __scalePercentToWavRange__(-1.0)), rises immediately to 32767 at
    # the halfway point (__scalePercentToWavRange__(1.0)), then stays at
    # 32767 through the final sample.
    # Add documentation comments below the function declaration
    # as I have for genSine() and genRiseSaw(), per the Output documentation
    # starting below line 18 above for this waveform type.
    def genSquare(samples, table2D, wavecol):#create square function and calculate values for a square graph
        halfway = samples // 2
        
        for i in range(samples):
            if i < halfway:
                current_val = -32767
            else:
                current_val = 32767
            table2D[i][wavecol] = current_val#print to table
    # STUDENT 5: 19% Write function genPulse() to generate a pulse wave
    # that starts at the min sample value of -32767
    # (i.e., __scalePercentToWavRange__(-1.0)), rises immediately to 32767 at
    # the DutyCycle point before the end (__scalePercentToWavRange__(1.0)),
    # then stays at 32767 through the final sample.
    # Add documentation comments below the function declaration
    # as I have for genSine() and genRiseSaw(), per the Output documentation
    # starting below line 18 above for this waveform type.
    def genPulse(samples, table2D, wavecol):#create pulse function and calculate values for a pulse graph
        DutyCycle = 0.25
        duty_cycle_index = int((1 - dutyCycle) * samples)
        for i in range(samples):
            if i < duty_cycle_index:
                current_val = -32767
            else:
                current_val = 32767
                
            table2D[i][wavecol] = current_val #print to table
            
            
    def genRiseSaw(samples, table2D, wavecol):#create risingsaw function and calculate values for a risingsaw graph
        stepsize = (2) / (samples-1)
        current_value = -1.0
        for step in range(0, samples):
            intvalue = __scalePercentToWavRange__(current_value)
            table2D[step][wavecol] = intvalue#print to table
            current_value += stepsize
    # STUDENT 6: 19% Write function genFallSaw() to generate a falling sawtooth
    # wave that starts at the max sample value of 32767
    # (i.e., __scalePercentToWavRange__(1.0)), falls incrementally to -32767
    # at the final sample.
    # Add documentation comments below the function declaration
    # as I have for genSine() and genRiseSaw(), per the Output documentation
    # starting below line 18 above for this waveform type.
    def genFallSaw(samples, table2D, wavecol):#create fallingsaw function and calculate values for a fallingsaw graph
        
        stepsize = (-2.0) / (samples-1)
        current_value = 1.0
        for step in range(0, samples):
            intvalue = __scalePercentToWavRange__(current_value)
            table2D[step][wavecol] = intvalue#print to table
            current_value += stepsize
            
    generators = {'triangle' : genTri,
        'sine' : genSine, 'cos': genCosine,
        'square' : genSquare, 'pulse' : genPulse,
        'risingsaw' : genRiseSaw, 'fallingsaw' : genFallSaw}
    # def genSamples(wavetype, samples, wavecol, table2D, dutyCycle, statsfileh=None):
        # if wavetype not in generators:
            # raise ValueError('Invalid wavetype: ' + wavetype)
    f = generators[wavetype]    # Select generator based on its string name.
    f(samples, table2D, wavecol)        # Invoke that column data generator.
    if statsfileh != None:
        column = table2D.take(indices=wavecol, axis=1).astype(float)
        # axis gives dimension, indices gives where in that dimension
        # extract column data into a vector, converting elements
        # to float. stdev() and pstdev() choke on int16 and float32
        # for some reason but deal fine with float
        # https://numpy.org/doc/stable/reference/generated/numpy.take.html
        # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html
        # print("DEBUG COLUMN", wavecol, column)
        __getstats__(wavetype, column, statsfileh)
    # check for each type of graph values 
    if wavetype == 'triangle':
        genTri(samples, table2D, wavecol)
    elif wavetype == 'sine':
        genSine(samples, table2D, wavecol)
    elif wavetype == 'cos':
        genCosine(samples, table2D, wavecol)
    elif wavetype == 'square':
        genSquare(samples, table2D, wavecol)
    elif wavetype == 'pulse':
        genPulse(samples, table2D, wavecol)
    elif wavetype == 'risingsaw':
        genRiseSaw(samples, table2D, wavecol)
    elif wavetype == 'fallingsaw':
        genFallSaw(samples, table2D, wavecol) 
    else:
        raise ValueError(f"Unsupported waveform type: {wavetype}")
    
__usage__ = 'USAGE: python CSC223f23WAVEassn2.py'
# Symbol names with __underline__ should be private to their context.
if __name__ == '__main__':      # Entry code outside of any function.
    if len(sys.argv) != 1:
        raise ValueError(__usage__)
        # https://docs.python.org/3.7/library/exceptions.html
    infile = open('CSC223f23WaveParams.csv', 'r')
    incsv = csv.reader(infile)
    inheader = incsv.__next__()     # Read header line before data
    expected = ['WaveType','Frequency','SampleRate','Duration','DutyCycle']
    if inheader != expected:
        raise ValueError('CSC223f23WaveParams.csv header ERROR, Expected '
            + str(expected) + ', Got ' + str(inheader))
    # For CSC223 just hard coding some things to keep life simpler.
    WaveType = ('triangle', 'sine', 'cos', 'square', 'pulse',
        'risingsaw', 'fallingsaw')
    WaveColumn = {}
    for ix in range(0, len(WaveType)):
        WaveColumn[WaveType[ix]] = ix
    SampleRate = 44100
    Frequency = 1000.0
    Duration = 1
    DutyCycle = 0.25
    outheading = ['timestep']
    # Compute following ahead of time so we can prebuild a 2D nparray.
    period = 1.0 / Frequency     # ipython comments are from above
    # In [44]: period = 1.0/1000.0
    sampleTime = 1.0 / SampleRate
    # In [46]: sampleTime = 1.0 / 44100
    samples = math.ceil(period / sampleTime)
    # In [48]: samples = period / sampleTime
    table2D = np.ndarray(shape=(samples, len(WaveType)+1), # 1 for timestep
        dtype=np.int16, order='C') # C is row major, 'F' col major, benchmark!
    table2D.fill(0)
    for rowix in range(0, samples):
        table2D[rowix][0] = rowix   # Populate the timestep column with data.
    statsfileh = open('CSC223f23WAVEassn2.txt', 'w')
    wavecol = 1     # timestep already populated
    
    
    for inrow in incsv:
        wavetype, freq, srate, dur, duty = inrow
        freq = float(freq)  # They come in as strings.
        srate = int(srate)
        dur = int(dur)
        duty = float(duty)
        print("DEBUG inline", wavetype, freq, srate, dur, duty);
        if ((WaveColumn[wavetype] != (wavecol-1))
            or not (freq == Frequency and srate == SampleRate
                and dur == Duration and duty == DutyCycle)):
            raise ValueError('CSC223f23WaveParams.csv config data ERROR: '
                + str(inrow))
        outheading.append(wavetype)

        genSamples(wavetype, samples, wavecol, table2D, duty, statsfileh)
        wavecol += 1
        
        
        
        
        
        
    infile.close()
    outfile = open('CSC223f23WAVEassn2.csv', 'w')
    outcsv = csv.writer(outfile, delimiter=',', quotechar='"')
    outcsv.writerow(outheading)
    outcsv.writerows(table2D)
    outfile.close()
    statsfileh.close()

