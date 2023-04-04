programName = 'ezGal230403a.py'
programRevision = programName

# ezRA - Easy Radio Astronomy ezGal GALaxy explorer program,
#   to read ezCon format *Gal.npz condensed data text file(s),
#   and optionally create .png plot files.
# https://github.com/tedcline/ezRA

# Copyright (c) 2023, Ted Cline   TedClineGit@gmail.com

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# TTD:
#       remove many global in main() ?????????
#       plotCountdown, 'plotting' lines only if plotting

# ezGal230403b.py, ezGal610 with all 4 quadrants
# ezGal230402a.py, fixed plotCountdown
# ezGal230401b.py, 4 quadrants: plotEzGal61XgLonSpectraCascade() 611, 612, 613, 614
# ezGal230401a.py, 4 quadrants: plotEzGal60XgLonSpectra() 601, 602, 603, 604
# ezGal230331a.py, 4 quadrants: plotEzGal70XgLonSpectrums() 701, 702, 703, 704
# ezGal230330a.py, more quadrants - no success
# ezGal230329a.py, more quadrants
# ezGal230328a.py, more quadrants
# ezGal230327a.py, rewrote ezGal540, ezGal541, ezGal550, and ezGal560
# ezGal230325a.py, plotEzGal560galMass()
# ezGal230324a.py, plotEzGal560galMass()
# ezGal230316a.py, -eX, cmdLineArg
# ezGal230311a.py, oops ezGal516 ezGal516 ezGal516 were not finished, commented them out,
#   for ezGal520velGLonPolar.png and ezGal521velGLonPolarCount.png,
#   "MatplotlibDeprecationWarning: Auto-removal of grids by pcolor() and
#   pcolormesh() is deprecated since 3.5 and will be removed two minor releases later;
#   please call grid(False) first.", so put "plt.grid(0)" in front of each "im = plt.pcolormesh(",
#   `scipy.ndimage` not deprecated `scipy.ndimage.filters`,
#   plotCountdown tuning
# ezGal230308a.py, cleanup
# ezGal230305a.py, boilerplate from ezSky
# ezGal230217a.py, add ezGal516velGLonAvg, ezGal517velGLonMax
# ezGal221123a.py, to ezGal690, and to X axis using -byFreqBinX
# ezGal221117a.py, "Galaxy Crossing" to "Galaxy Plane"
# ezGal221117a.py,
#   ezGal530velDecGLon.png to ezGal530galDecGLon.png,
#   ezGal550velGRot_*.png to ezGal550galRot_*.png,
#   ezGal690GLonDegP180_*ByFreqBinAvg.png to ezGal590gLonDegP180_*ByFreqBinAvg.png
# ezGal221017a.py, polishing
# ezGal221016a.py, polishing
# ezGal221013a.py, polishing
# ezGal221012a.py, polishing
# Jul-28-2022a, ezGal10z05b.py,
#   removed warning for missing ezDefaults.txt, ezCon to ezGal, ezVel to ezGal,
#   galGLon to velGLon, velDecP90GLonP180Count to galDecP90GLonP180Count
# ezGal10z05a.py, first try with *Gal.npz input, Jul-15-2022a  N0RQV
#   from "ezVelV7 (2).py"
#   Vel.npz changed to Gal.npz,
#   in ezVel512velGLonPolar plt.pcolormesh() gets shading='auto'
#   in ezVel513velGLonCountPolar plt.pcolormesh() gets shading='auto'
# May- 6-2021a  N0RQV
# ezVelV7.py, added fileObsName to loaded Vel.npz file format for plot titles,
#   fileObsName can be overwritten by optional ezRAObsName argument,
#   commented out unused arguments


import seaborn as sb

import os                       # used to grab all files in the current directory

import sys                

import time
import datetime

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
#plt.rcParams['agg.path.chunksize'] = 20000    # to support my many data points

from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
#from astropy import modeling

import numpy as np

from scipy.interpolate import griddata
#from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import gaussian_filter

import math



def printUsage():
    print()
    print()
    print('##############################################################################################')
    print()
    print('USAGE:')
    print('  Windows:   py      ezGal.py [optional arguments] radioDataFileDirectories')
    print('  Linux:     python3 ezGal.py [optional arguments] radioDataFileDirectories')
    print()
    print('  Easy Radio Astronomy (ezRA) ezGal GALaxy explorer program,')
    print('  to read ezCon format *Gal.npz condensed data text file(s),')
    print('  and optionally create .png plot files.')
    print()
    print('  "radioDataFileDirectories" may be one or more *Gal.npz condensed data text files:')
    print('         py  ezGal.py  bigDish220320_05Gal.npz')
    print('         py  ezGal.py  bigDish220320_05Gal.npz bigDish220321_00Gal.npz')
    print('         py  ezGal.py  bigDish22032*Gal.npz')
    print('  "radioDataFileDirectories" may be one or more directories:')
    print('         py  ezGal.py  .')
    print('         py  ezGal.py  bigDish2203')
    print('         py  ezGal.py  bigDish2203 bigDish2204')
    print('         py  ezGal.py  bigDish22*')
    print('  "radioDataFileDirectories" may be a mix of *Gal.npz condensed data text files and directories')
    print()
    print('  Arguments and "radioDataFileDirectories" may be in any mixed order.')
    print()
    print('  Arguments are read first from inside the ezGal program,')
    print("  then in order from the ezDefaults.txt in the ezGal.py's directory,")
    print('  then in order from the ezDefaults.txt in current directory,')
    print('  then in order from the command line.  For duplicates, last read wins.')
    print()
    print('EXAMPLES:')
    print()
    print('    -ezRAObsName         bigDish    (observatory name for plot titles)')
    print()
    print('    -ezGalPlotRangeL     0  500     (save only this range of ezGal plots to file, to save time)')
    print('    -ezGalDispGrid          1       (turn on graphical display plot grids)')
    print()
    print('    -ezGalVelGLonEdgeFrac   0.5     (velGLon level fraction for ezGal540velGLonEdgesB)')
    #print('    -ezGalVelGLonEdgeFrac   0.5    ')
    #print('         (velGLon level fraction for ezGal540velGLonEdgesB)')
    #print('    -ezGalVelGLonEdgeLevel  0.5    ')
    #print('         (velGLon level for ezGal540velGLonEdgesB, if 0 then use only ezGalVelGLonEdgeFrac)')
    print()
    print('    -ezGal61XGain           150     (maximum height in ezGal61XgLonSpectraCascade plots)')
    print()
    print('    -ezDefaultsFile ../bigDish8.txt (additional file of ezRA arguments)')
    print()
    print('    -eXXXXXXXXXXXXXXzIgonoreThisWholeOneWord')
    print('         (any one word starting with -eX is ignored, handy for long command line editing)')
    print()
    print()
    print(' programRevision =', programRevision)
    print()
    print()
    print()
    print()
    print()
    print('       The Society of Amateur Radio Astronomers (SARA)')
    print('                    radio-astronomy.org')
    print()
    print()
    print()
    print()
    print()
    print('##############################################################################################')
    print()

    exit()



def printHello():

    global programRevision          # string
    global commandString            # string

    print()
    print('         For help, run')
    print('            ezGal.py -help')

    print()
    print('=================================================')
    print(' Local time =', time.asctime(time.localtime()))
    print(' programRevision =', programRevision)
    print()

    commandString = '  '.join(sys.argv)
    print(' This Python command = ' + commandString)



def ezGalArgumentsFile(ezDefaultsFileNameInput):
    # process arguments from file

    global ezRAObsName                      # string

    global ezGalDispGrid                    # integer

    global ezGalVelGLonEdgeFrac             # float
    #global ezGalVelGLonEdgeLevel            # float
    global ezGal61XGain                     # float

    global ezGalPlotRangeL                  # integer list


    print()
    print('   ezGalArgumentsFile(' + ezDefaultsFileNameInput + ') ===============')

    # https://www.zframez.com/tutorials/python-exception-handling.html
    try:
        fileDefaults = open(ezDefaultsFileNameInput, 'r')

        # process each line in ezDefaultsFileNameInput
        
        print('      success opening ' + ezDefaultsFileNameInput)

        while 1:
            fileLine = fileDefaults.readline()

            # LF always present: 0=EOF  1=LF  2=1Character
            if not fileLine:              # if end of file
                break                     # get out of while loop

            thisLine = fileLine.split()
            if not thisLine:              # if line all whitespace
                continue                  # skip to next line

            if thisLine[0][0] == '#':    # ignoring whitespace, if first character of first word
                continue                  # it is a comment, skip to next line


            thisLine0Lower = thisLine[0].lower()

            # ezRA arguments used by multiple programs:
            if thisLine0Lower == '-ezRAObsName'.lower():
                ezRAObsName = thisLine[1]
                #ezRAObsName = uni.encode(thisLine[1])
                #ezRAObsName = str.encode(thisLine[1])


            # integer arguments:
            elif thisLine0Lower == '-ezGalDispGrid'.lower():
                ezGalDispGrid = int(thisLine[1])


            # float arguments:
            elif thisLine0Lower == '-ezGalVelGLonEdgeFrac'.lower():
                ezGalVelGLonEdgeFrac = float(thisLine[1])

            #elif thisLine0Lower == '-ezGalVelGLonEdgeLevel'.lower():
            #    ezGalVelGLonEdgeLevel = float(thisLine[1])

            elif thisLine0Lower == '-ezGal61XGain'.lower():
                ezGal61XGain = float(thisLine[1])


            # list arguments:
            ###elif thisLine0Lower == 'ezGalUseSamplesRawL'.lower():
            ###    ezGalUseSamplesRawL.append(int(thisLine[1]))
            ###    ezGalUseSamplesRawL.append(int(thisLine[2]))

            elif thisLine0Lower == '-ezGalPlotRangeL'.lower():
                ezGalPlotRangeL[0] = int(thisLine[1])
                ezGalPlotRangeL[1] = int(thisLine[2])


            elif 6 <= len(thisLine0Lower) and thisLine0Lower[:6] == '-ezGal'.lower():
                print()
                print()
                print()
                print()
                print()
                print(' ========== FATAL ERROR:  Defaults file ( ' + ezDefaultsFileNameInput + ' )')
                print(" has this line's unrecognized first word:")
                print(fileLine)
                print()
                print()
                print()
                print()
                exit()


            else:
                pass    # unrecognized first word, but no error

    except (FileNotFoundError, IOError):
    	#print ()
    	#print ()
    	#print ()
    	#print ()
    	#print ('   Warning: Error in opening file or reading ' + ezDefaultsFileName + ' file.')
    	##print ('   ... Using defaults ...')
    	#print ()
    	#print ()
    	#print ()
    	#print ()
    	pass

    else:
        fileDefaults.close()       #   then have processed all available lines in this Defaults file



def ezGalArgumentsCommandLine():
    # process arguments from command line

    global commandString                    # string

    global ezRAObsName                      # string

    global ezGalVelGLonEdgeFrac             # float
    #global ezGalVelGLonEdgeLevel            # float
    global ezGal61XGain                     # float

    global ezGalPlotRangeL                  # integer list
    global ezGalDispGrid                    # integer

    global cmdDirectoryS                    # string            creation


    print()
    print('   ezGalArgumentsCommandLine ===============')

    cmdLineSplit = commandString.split()
    cmdLineSplitLen = len(cmdLineSplit)
        
    if cmdLineSplitLen < 2:
        # need at least one data directory or file
        printUsage()

    cmdLineSplitIndex = 1
    cmdDirectoryS = ''

    while cmdLineSplitIndex < cmdLineSplitLen:
        #print(' cmdLineSplit[cmdLineSplitIndex] =', cmdLineSplit[cmdLineSplitIndex])
        if cmdLineSplit[cmdLineSplitIndex][0] != '-':
            # ignoring whitespace, first character of cmdLineSplit word is not '-'
            if cmdLineSplit[cmdLineSplitIndex][0] == '#':
                # rest of cmdLineSplit is a comment, get out of while loop
                break
            else:
                # must be a data directory or file, remember it
                cmdDirectoryS = cmdDirectoryS + cmdLineSplit[cmdLineSplitIndex] + ' '

        else:
            # Ignoring whitespace, first character of cmdLineSplit word is '-'.
            # Must be an option.
            # Remove '-'
            cmdLineArg = cmdLineSplit[cmdLineSplitIndex][1:]
            # ignoring whitespace, first character of cmdLineSplit word was '-', now removed
            if cmdLineArg[0] == '-':
                cmdLineArg = cmdLineArg[1:]
                # ignoring whitespace, first 2 characters of cmdLineSplit word were '--', now removed

            cmdLineArgLower = cmdLineArg.lower()
            cmdLineSplitIndex += 1      # point to first option value


            if cmdLineArgLower == 'help':
                printUsage()

            elif cmdLineArgLower == 'h':
                printUsage()


            # ezRA arguments used by multiple programs:
            elif cmdLineArgLower == 'ezRAObsName'.lower():
                ezRAObsName = cmdLineSplit[cmdLineSplitIndex]   # cmd line allows only one ezRAObsName word
                #ezRAObsName = uni.encode(thisLine[1])
                #ezRAObsName = str.encode(thisLine[1])
            

            # integer arguments:
            elif cmdLineArgLower == 'ezGalDispGrid'.lower():
                ezGalDispGrid = int(cmdLineSplit[cmdLineSplitIndex])


            # float arguments:
            elif cmdLineArgLower == 'ezGalVelGLonEdgeFrac'.lower():
                ezGalVelGLonEdgeFrac = float(cmdLineSplit[cmdLineSplitIndex])

            #elif cmdLineArgLower == 'ezGalVelGLonEdgeLevel'.lower():
            #    ezGalVelGLonEdgeLevel = float(cmdLineSplit[cmdLineSplitIndex])

            elif cmdLineArgLower == 'ezGal61XGain'.lower():
                ezGal61XGain = float(cmdLineSplit[cmdLineSplitIndex])


            # list arguments:
            elif cmdLineArgLower == 'ezGalPlotRangeL'.lower():
                ezGalPlotRangeL[0] = int(cmdLineSplit[cmdLineSplitIndex])
                cmdLineSplitIndex += 1
                ezGalPlotRangeL[1] = int(cmdLineSplit[cmdLineSplitIndex])

            elif cmdLineArgLower == 'ezDefaultsFile'.lower():
                ezGalArgumentsFile(cmdLineSplit[cmdLineSplitIndex])


            # ignore silly -eX* arguments, for handy neutralization of command line arguments,
            #   but remove spaces before argument numbers
            #   (can not use '-x' which is a preface to a negative hexadecimal number)
            elif 2 <= len(cmdLineArgLower) and cmdLineArgLower[:2] == 'ex':
                cmdLineSplitIndex -= 1
                #pass

            # before -eX, old spelling:
            # ignore silly -ezez* arguments, for handy neutralization of command line arguments,
            #   but remove spaces before argument numbers
            elif 4 <= len(cmdLineArgLower) and cmdLineArgLower[:4] == 'ezez':
                cmdLineSplitIndex -= 1
                #pass


            else:
                print()
                print()
                print()
                print()
                print()
                print(' ========== FATAL ERROR:  Command line has this unrecognized first word:')
                print('-' + cmdLineArg)
                print()
                print()
                print()
                print()
                exit()
                
        cmdLineSplitIndex += 1



def ezGalArguments():
    # argument: (Computing) a value or address passed to a procedure or function at the time of call

    #global programRevision                  # string
    #global commandString                    # string

    global ezRAObsName                      # string

    global ezGalVelGLonEdgeFrac             # float
    #global ezGalVelGLonEdgeLevel            # float
    global ezGal61XGain                     # float

    global ezGalPlotRangeL                  # integer list
    global plotCountdown                    # integer
    global ezGalDispGrid                    # integer


    # defaults
    #ezRAObsName = 'LebanonKS'
    #ezRAObsName = 'defaultKS'
    ezRAObsName = ''                # overwritten by optional argument

    ezGalVelGLonEdgeFrac  = 0.5     # velGLon level fraction for ezGal540velGLonEdgesB
    #ezGalVelGLonEdgeLevel = 0.      # velGLon level for ezGal540velGLonEdgesB, if not 0 then
                                     #   ezGalVelGLonEdgeFrac ignored
    ezGal61XGain          = 120.     # maximum height in ezGal61XgLonSpectraCascade plots
    
    ezGalPlotRangeL = [0, 9999]     # save this range of plots to file
    plotCountdown = 19              # number of plots still to print + 1
    ezGalDispGrid = 0

    # process arguments from ezDefaults.txt file in the same directory as this ezGal program
    ezGalArgumentsFile(os.path.dirname(__file__) + os.path.sep + 'ezDefaults.txt')

    # process arguments from ezDefaults.txt file in the current directory
    ezGalArgumentsFile('ezDefaults.txt')

    ezGalArgumentsCommandLine()             # process arguments from command line
    
    # print status
    print()
    print('   ezRAObsName =', ezRAObsName)
    print()
    print('   ezGalVelGLonEdgeFrac  =', ezGalVelGLonEdgeFrac)
    #print('   ezGalVelGLonEdgeLevel =', ezGalVelGLonEdgeLevel)
    print('   ezGal61XGain          =', ezGal61XGain)
    print()
    print('   ezGalPlotRangeL =', ezGalPlotRangeL)
    print('   ezGalDispGrid   =', ezGalDispGrid)



def readDataDir():
    # Open each data file in directory and read individual lines.

    global ezRAObsName              # string
    global fileObsName              # string                                    creation
    global fileFreqMin              # float                                     creation
    global fileFreqMax              # float                                     creation
    global fileFreqBinQty           # integer                                   creation

    global velGLonP180              # float 2d array                            creation
    global velGLonP180Count         # integer array                             creation
    global velGLonP180CountSum      # integer                                   creation
    global galDecP90GLonP180Count   # integer 2d array                          creation
    global antXTVTName              # string                                    creation

    global fileNameLast             # string                                    creation

    print()
    print('   readDataDir ===============')

    #directoryList = sorted(cmdDirectoryS.split())           # sorted needed on Linux
    directoryList = cmdDirectoryS.split()
    directoryListLen = len(directoryList)
    
    VelNpz_Qty = 0
    for directoryCounter in range(directoryListLen):
        directory = directoryList[directoryCounter]

        # if arguments are .txt filenames,
        # pass each of them through together as a mini directory list of .txt files.
        # Allows one .txt file from a directory of .txt files.
        if directory.endswith('Gal.npz'):
            fileList = [directory]
            directory = '.'
        else:
            fileList = sorted(os.listdir(directory))        # sorted needed on Linux
        fileListLen = len(fileList)
        for fileCounter in range(fileListLen):
            fileReadName = fileList[fileCounter]
            #print('\r file =', fileCounter + 1, ' of', fileListLen,
            #    ' in dir', directoryCounter + 1, ' of', directoryListLen,
            #    ' =', directory + os.path.sep + fileReadName, '                                      ',
            #    end='')   # allow append to line
            print(f'\r {VelNpz_Qty + 1}  file = {fileCounter + 1} of {fileListLen}',
                f' in dir {directoryCounter + 1} of {directoryListLen} =',
                directory + os.path.sep + fileReadName, '                                      ',
                end='')   # allow append to line

            if not fileReadName.endswith('Gal.npz'):
                continue                                # skip to next file

            npzfile = np.load(fileReadName)

            if not VelNpz_Qty:                      # if first *Gal.npz file
                fileObsName    = npzfile['fileObsName'].tolist()
                if ezRAObsName:
                    fileObsName = ezRAObsName       # overwrite fileObsName with argument
                fileFreqMin    = float(npzfile['fileFreqMin'])
                fileFreqMax    = float(npzfile['fileFreqMax'])
                fileFreqBinQty = int(npzfile['fileFreqBinQty'])

                # Velocity by Galactic Longitude (gLon) grid.
                # gLon is -180thru+180, adding 180, gives gLonP180 as 0thru360 which is more convenient.
                # velGLonP180 is fileFreqBinQty by 0thru360 gLonP180
                #velGLonP180 = np.zeros([fileFreqBinQty, 361], dtype = float)
                velGLonP180 = npzfile['velGLonP180']
                
                # incoming velGLonP180 is now still the summed antXTVT frequency spectra, with decending frequency.
                # For each spectrum, velGLonP180Count[gLonP180] recorded the quantity summed.

                # velGLonP180Count is count of saved spectra in velGLonP180
                #velGLonP180Count = np.zeros([361], dtype = int)
                velGLonP180Count = npzfile['velGLonP180Count']
                # Declination (dec) is -90thru+90, adding 90, gives decP90 as 0thru180 which is more convenient.
                # galDecP90GLonP180Count is 0thru180 decP90 by 0thru360
                #galDecP90GLonP180Count = np.zeros([181, 361], dtype = int)
                galDecP90GLonP180Count = npzfile['galDecP90GLonP180Count']
                #print(npzfile.files)
                #print('antXTVTName' in npzfile.files)
                if 'antXTVTName' in npzfile.files:     # was added to file definition later on 230401
                    antXTVTName = npzfile['antXTVTName']
                else:
                    antXTVTName = 'AntXTVT'
            else:
                # ignore npzfile['fileFreqMin'] 
                # ignore npzfile['fileFreqMax']
                # ignore npzfile['fileFreqBinQty'] 
                velGLonP180            += npzfile['velGLonP180']
                velGLonP180Count       += npzfile['velGLonP180Count']
                galDecP90GLonP180Count += npzfile['galDecP90GLonP180Count']
                if 'antXTVTName' in npzfile.files:     # was added to file definition later on 230401
                    antXTVTName = npzfile['antXTVTName']
                else:
                    antXTVTName = 'AntXTVT'

            VelNpz_Qty += 1
            fileNameLast = fileReadName
            print()

    # have now read all Gal.npz files

    # maybe blank out the last filename
    if not fileReadName.endswith('Gal.npz'):
        print('\r                                                                              ' \
            + '                                                                                ')
    else:
        print()
    
    if not VelNpz_Qty:                      # if no first *Gal.npz file
        print()
        print()
        print(" ========== FATAL ERROR: no data file loaded")
        print()
        print()
        print()
        exit()


    print(' fileNameLast =', fileNameLast)
    print(' VelNpz_Qty   =', VelNpz_Qty)

    print()
    print(' fileFreqMin = ', fileFreqMin)
    print(' fileFreqMax = ', fileFreqMax)
    print(' fileFreqBinQty = ', fileFreqBinQty)

    print()
    print(' velGLonP180.shape = ', velGLonP180.shape)
    print(' velGLonP180Count.shape = ', velGLonP180Count.shape)
    print(' galDecP90GLonP180Count.shape = ', galDecP90GLonP180Count.shape)
    print(' antXTVTName =', antXTVTName)

    print()
    velGLonP180CountSum = velGLonP180Count.sum()
    print(' velGLonP180CountSum =', velGLonP180CountSum)

    if not velGLonP180CountSum:       # if nothing in velGLonP180 to save or plot
        print()
        print()
        print(" ========== FATAL ERROR: no data loaded")
        print()
        print()
        print()
        exit()


    # for fileNameLast of  data/2021_333_00.txt  create fileVelWriteName as  data/2021_333_00GalC.npz
    fileVelWriteName = fileNameLast.split(os.path.sep)[-1][:-7] + 'GalC.npz'   # ezGal combines *Gal.npz
    print(' fileObsName = ', fileObsName)
    np.savez_compressed(fileVelWriteName, fileObsName=np.array(fileObsName),
        fileFreqMin=np.array(fileFreqMin), fileFreqMax=np.array(fileFreqMax),
        fileFreqBinQty=np.array(fileFreqBinQty),
        velGLonP180=velGLonP180, velGLonP180Count=velGLonP180Count,
        galDecP90GLonP180Count=galDecP90GLonP180Count)

    # Prepare velGLonP180 for later plots.
    # velGLonP180 has been filled with sums of samples.  Now for each column, convert to sum's average.
    for gLonP180 in range(361):
        if velGLonP180Count[gLonP180]:
            velGLonP180[:, gLonP180] /= velGLonP180Count[gLonP180]

    if 1:
        # mask low values with Not-A-Number (np.nan) to not plot
        #maskOffBelowThis = 0.975    # N0RQVHC
        #maskOffBelowThis = 0.9      # WA6RSV
        maskOffBelowThis = 1.0      # LTO15HC
        print('   maskOffBelowThis = ', maskOffBelowThis)
        maskThisOff = (velGLonP180 < maskOffBelowThis)
        #velGLonP180[maskThisOff] = np.nan                   # maskOffBelowThis is the do not plot
        velGLonP180[maskThisOff] = maskOffBelowThis         # maskOffBelowThis is the minumum everywhere



def plotPrep():
    # creates titleS, velocitySpanMax, velocityBin

    global fileObsName              # string
    global fileFreqMin              # float
    global fileFreqMax              # float
    global fileFreqBinQty           # integer

    global freqStep                 # float                 creation
    #global dopplerSpanD2            # float                 creation
    global freqCenter               # float                 creation

    global velocitySpanMax          # float                 creation
    global velocityBin              # float array           creation

    global titleS                   # string                creation

    #global byFreqBinX               # float array           creation

    print()
    print('   plotPrep ===============')

    print('                         fileFreqMin =', fileFreqMin)
    print('                         fileFreqMax =', fileFreqMax)

    #freqStep = 0.00234375           # 2.4 MHz / 1024 = 0.00234375 MHz
    # fileFreqMin = 1419.205         #0000      -1.2 Doppler
    #                                #0512       0.0 Doppler
    # fileFreqMax = 1421.60265625    #1023       1.2 Doppler
    # (1421.60265625 - 1419.205 ) * 512 / 1023 = 1.2
    # 1.2  + 1419.205 = 1420.405 ------- yup
    #freqStep = (fileFreqMax - fileFreqMin) / (freqBinQtyPre + fileFreqBinQty - 1)
    freqStep = (fileFreqMax - fileFreqMin) / (fileFreqBinQty - 1)
    print('                         freqStep =', freqStep)
    #dopplerSpanD2 = (freqBinQtyPre + fileFreqBinQty) * 0.5 * freqStep
    #dopplerSpanD2 = fileFreqBinQty * 0.5 * freqStep         # Doppler spans -dopplerSpanD2 thru +dopplerSpanD2
    dopplerSpanD2 = (fileFreqMax - fileFreqMin) / 2.        # Doppler spans -dopplerSpanD2 thru +dopplerSpanD2
    print('                         dopplerSpanD2 =', dopplerSpanD2)
    #freqCenter = fileFreqMin + dopplerSpanD2
    freqCenter = (fileFreqMin + fileFreqMax) / 2.
    print('                         freqCenter =', freqCenter)

    #titleS = '  ' + fileNameLast.split('\\')[-1] + u'           N\u00D8RQV          (' + programName + ')'
    #titleS = '  ' + fileNameLast.split('\\')[-1] + u'           WA6RSV          (' + programName + ')'
    titleS = '  ' + fileNameLast.split(os.path.sep)[-1] + u'           ' + fileObsName \
        + '          (' + programName + ')'

    # increasing freq
    #byFreqBinX = np.arange(fileFreqBinQty) * freqStep - dopplerSpanD2

    velocitySpanMax = +dopplerSpanD2 * (299792458. / freqCenter) / 1000.  # = 253.273324388 km/s
    velocityBin = np.linspace(-velocitySpanMax, velocitySpanMax, fileFreqBinQty)








def plotEzGal510velGLon():

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global velocitySpanMax          # float
    global velocityBin              # float array

    global titleS                   # string
    global ezGalDispGrid            # integer
    #global fileFreqBinQty           # integer
    #global freqStep                 # float
    #global dopplerSpanD2            # float
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to save or plot
    if ezGalPlotRangeL[0] <= 510 and 510 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal510velGLon.png'
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()

        # if any Galactic plane crossings, velGLonP180 has been (partially?) filled with averages
        velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
        print('                         velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )
        print()

        xi = np.arange(-180, +181, 1)           # +180 thru -180 degrees in degrees, galaxy centered
        #yi = np.arange(0, fileFreqBinQty, 1)    # 0 to fileFreqBinQty in freqBins
        # speed of light = 299,792,458 meters per second
        #    rawPlotPrep ===============
        #       fileFreqMin = 1419.2
        #       fileFreqMax = 1421.6
        #       freqStep = 0.009411764705881818
        #       dopplerSpanD2 = 1.1999999999999318
        #       freqCenter = 1420.4
        # velocity = (fileFreqBin doppler MHz) * (299792458. m/s / 1420.406 MHz) / 1000. = km/s
        # velocity spans = -dopplerSpanD2 * (299792458. / freqCenter) thru
        #                  +dopplerSpanD2 * (299792458. / freqCenter)
        #velocitySpanMax = +1.1999999999999318 * (299792458. / 1420.406) / 1000.  # = 253.273324388 km/s
        #velocitySpanMax = +dopplerSpanD2 * (299792458. / freqCenter) / 1000.  # = 253.273324388 km/s
        #yi = np.linspace(-velocitySpanMax, velocitySpanMax, fileFreqBinQty)
        yi = velocityBin + 0.

        xi, yi = np.meshgrid(xi, yi)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        print('                         np.nanmax(velGLonP180) =', np.nanmax(velGLonP180))
        #print('                         np.mean(velGLonP180[~np.isnan(velGLonP180)]) =',
        #    np.mean(velGLonP180[~np.isnan(velGLonP180)]))
        print('                         np.mean(velGLonP180) =', np.mean(velGLonP180))
        print('                         np.nanmin(velGLonP180) =', np.nanmin(velGLonP180))
        pts = plt.contourf(xi, yi, velGLonP180, 100, cmap=plt.get_cmap('gnuplot'))
        #pts = plt.contourf(xi, yi, velGLonP180, 100, cmap=plt.get_cmap('gnuplot'), vmin=1.025, vmax=1.21)

        # horizonal thin black line
        plt.axhline(y =   0, linewidth=0.5, color='black')

        # vertical thin black lines
        plt.axvline(x =  90, linewidth=0.5, color='black')
        plt.axvline(x =   0, linewidth=0.5, color='black')
        plt.axvline(x = -90, linewidth=0.5, color='black')

        cbar = plt.colorbar(pts, orientation='vertical', pad=0.06)

        plt.title(titleS)
        #plt.grid(ezGalDispGrid)
        plt.grid(0)

        plt.xlabel('Galactic Longitude (degrees)')
        plt.xlim(180, -180)        # in degrees
        plt.xticks([ 180,   90,   0,   -90,   -180],
                   ['180', '90', '0', '-90', '-180'])

        plt.ylim(-velocitySpanMax, velocitySpanMax)        # in velocity

        #    plt.ylabel('Interpolated Velocity (km/s) by Galactic Longitude' \
        #        + f'\n\nVelocity Count Sum = {velGLonP180CountSum}' \
        #        + f'\n\nVelocity Count Nonzero = {velGLonP180CountNonzero}' \
        #        + f' of {len(velGLonP180Count)}',
        #        rotation=90, verticalalignment='bottom')
        plt.ylabel('Interpolated Velocity (km/s) by Galactic Longitude' \
            + f'\nVelocity Count: Sum={velGLonP180CountSum:,}'
            + f' Nonzero={velGLonP180CountNonzero} of {len(velGLonP180Count)}',
            rotation=90, verticalalignment='bottom')

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal511velGLonCount():

    global plotCountdown            # integer
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global titleS                   # string
    global ezGalDispGrid            # integer
    #global fileFreqBinQty           # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 511 and 511 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal511velGLonCount.png'
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()
        plt.plot(np.arange(-180, +181, 1), velGLonP180Count)

        plt.title(titleS)
        #plt.grid(ezGalDispGrid)
        plt.grid(0)

        plt.xlabel('Galactic Longitude (degrees)')
        plt.xlim(180, -180)        # in degrees
        plt.xticks([ 180,   90,   0,   -90,   -180],
                   ['180', '90', '0', '-90', '-180'])

        # if any Galactic plane crossings, velGLonP180 has been (partially?) filled with averages
        velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
        print('                         velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )
        print()

        plt.ylabel('Velocity Data Counts by Galactic Longitude' \
            + f'\nVelocity Count: Sum={velGLonP180CountSum:,}' \
            + f' Nonzero = {velGLonP180CountNonzero} of {len(velGLonP180Count)}')
        #    rotation=90, verticalalignment='bottom')

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')


        # print out velGLonCount status
        fileWriteGLonName = 'ezGal511velGLonCount.txt'
        fileWriteGLon = open(fileWriteGLonName, 'w')
        if not (fileWriteGLon.mode == 'w'):
            print()
            print()
            print()
            print()
            print()
            print(' ========== FATAL ERROR:  Can not open ')
            print(' ' + fileWriteGLonName)
            print(' file to write out velGLonCount data')
            print()
            print()
            print()
            print()
            exit()


        fileWriteGLonHashS = '########################################' \
            + '########################################'                        # 40 + 40 = 80 '#'

        fileWriteGLon.write('\ngLonDeg (-180thru180)   velGLonCount   gLonDegForHaystackSrt.cmd '\
            + '(180thru359to0thru180)       (RtoL)\n\n')

        for gLonP180 in range(180):                               # for every column, RtoL, 0 thru 179
            fileWriteGLonS = f'{gLonP180 - 180:4d}  {velGLonP180Count[gLonP180]:5d}  {gLonP180 + 180:4d}  ' \
                + fileWriteGLonHashS[:velGLonP180Count[gLonP180]] + '\n'
            fileWriteGLon.write(fileWriteGLonS)

        fileWriteGLonS = f'0000  {velGLonP180Count[180]:5d}  0000  ' \
            + fileWriteGLonHashS[:velGLonP180Count[180]] + '\n'
        fileWriteGLon.write(fileWriteGLonS)

        for gLonP180 in range(181, 361):                          # for every column, RtoL, 181 thru 360
            fileWriteGLonS = f'{gLonP180 - 180:4d}  {velGLonP180Count[gLonP180]:5d}  {gLonP180 - 180:4d}  ' \
                + fileWriteGLonHashS[:velGLonP180Count[gLonP180]] + '\n'
            fileWriteGLon.write(fileWriteGLonS)


        # print out velGLonCount Things-To-Do for Haystack srt.cmd command file
        velGLonCountTrigger = 15
        fileWriteGLon.write( \
            '\n\n\n\n\n* velGLonCount Things-To-Do for Haystack srt.cmd command file    (RtoL)')
        fileWriteGLon.write('\n* velGLonCountTrigger = ' + str(velGLonCountTrigger))
        fileWriteGLon.write('\n\n:5              * short pause of 5 seconds')
        fileWriteGLon.write('\n: record')
        fileWriteGLon.write('\n* later, do not forget at the end,       : roff\n\n')
        fileWriteGLon.write( \
            '\n* 600 + 240 + 060 = 900 seconds = 10 + 4 + 1 minutes = 15 min data collection\n\n')

        for gLonP180 in range(180):                               # for every column, RtoL, 0 thru 179
            if velGLonP180Count[gLonP180] <= velGLonCountTrigger:
                fileWriteGLon.write(f': G{gLonP180 + 180:03d}    * have {velGLonP180Count[gLonP180]:5d}\n')
                fileWriteGLon.write(':600\n')
                fileWriteGLon.write(':240\n')
                fileWriteGLon.write(':060\n')
                fileWriteGLon.write('*\n')
        for gLonP180 in range(180, 361):                          # for every column, RtoL, 180 thru 360
            if velGLonP180Count[gLonP180] <= velGLonCountTrigger:
                fileWriteGLon.write(f': G{gLonP180 - 180:03d}    * have {velGLonP180Count[gLonP180]:5d}\n')
                fileWriteGLon.write(':600\n')
                fileWriteGLon.write(':240\n')
                fileWriteGLon.write(':060\n')
                fileWriteGLon.write('*\n')

        fileWriteGLon.close()   



def plotEzGal516velGLonAvg():
    # spectrum Averages in dots

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global titleS                   # string
    global ezGalDispGrid            # integer
    #global fileFreqBinQty           # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 516 and 516 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal516velGLonAvg.png'
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()
        #plt.plot(np.arange(-180, +181, 1), velGLonP180Count)








        print('velGLonP180.shape = ', velGLonP180.shape)


        print('velGLonP180')
        print(velGLonP180)
        #print('~np.isnan(velGLonP180)')
        #print(~np.isnan(velGLonP180))
        #print('velGLonP180[~np.isnan(velGLonP180)]')
        #print(velGLonP180[~np.isnan(velGLonP180)])

        print('velGLonP180[0]')
        print(velGLonP180[0])
        print('velGLonP180[1]')
        print(velGLonP180[1])
        
        
        print('np.mean(velGLonP180, axis=0)')
        print(np.mean(velGLonP180, axis=0))
        print('shape = ', np.mean(velGLonP180, axis=0).shape)   # shape = (361,) <=================
 
 
 

        print('np.mean(velGLonP180, axis=1)')
        print(np.mean(velGLonP180, axis=1))
        print('shape = ', np.mean(velGLonP180, axis=1).shape)   # shape = (256,)




        #        print('velGLonP180[~np.isnan(velGLonP180[0])]')
        #        print(velGLonP180[~np.isnan(velGLonP180[0])])
        #        print('velGLonP180[~np.isnan(velGLonP180[1])]')
        #        print(velGLonP180[~np.isnan(velGLonP180[1])])

        #        print('velGLonP180[~np.isnan(velGLonP180)][0]')
        #        print(velGLonP180[~np.isnan(velGLonP180)][0])
        #        print('velGLonP180[~np.isnan(velGLonP180)][1]')
        #        print(velGLonP180[~np.isnan(velGLonP180)][1])
        #        print('np.mean(velGLonP180[~np.isnan(velGLonP180)][1])')
        #        print(np.mean(velGLonP180[~np.isnan(velGLonP180)][1]))


        
        #plt.plot(np.arange(-180, +181, 1), np.mean(velGLonP180[~np.isnan(velGLonP180)][1]))
        plt.plot(np.arange(-180, +181, 1), np.mean(velGLonP180[1]))













        plt.title(titleS)
        #plt.grid(ezGalDispGrid)
        plt.grid(0)

        plt.xlabel('Galactic Longitude (degrees)')
        plt.xlim(180, -180)        # in degrees
        plt.xticks([ 180,   90,   0,   -90,   -180],
                   ['180', '90', '0', '-90', '-180'])

        # if any Galactic plane crossings, velGLonP180 has been (partially?) filled with averages
        velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
        print(' velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )
        print()

        plt.ylabel('Average Velocity (km/s) by Galactic Longitude' \
            + f'\nVelocity Count: Sum={velGLonP180CountSum:,}' \
            + f' Nonzero = {velGLonP180CountNonzero} of {len(velGLonP180Count)}')
        #    rotation=90, verticalalignment='bottom')

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal517velGLonMax():
    # spectrum Maximums in dots

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global titleS                   # string
    global ezGalDispGrid            # integer
    #global fileFreqBinQty           # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 517 and 517 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal517velGLonMax.png'
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()
        #plt.plot(np.arange(-180, +181, 1), velGLonP180Count)
        #plt.plot(np.arange(-180, +181, 1), np.maximum(velGLonP180[~np.isnan(velGLonP180)][0]))
        plt.plot(np.arange(-180, +181, 1), np.maximum(velGLonP180[0]))

        plt.title(titleS)
        #plt.grid(ezGalDispGrid)
        plt.grid(0)

        plt.xlabel('Galactic Longitude (degrees)')
        plt.xlim(180, -180)        # in degrees
        plt.xticks([ 180,   90,   0,   -90,   -180],
                   ['180', '90', '0', '-90', '-180'])

        # if any Galactic plane crossings, velGLonP180 has been (partially?) filled with averages
        velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
        print(' velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )
        print()

        plt.ylabel('Maximum Velocity (km/s) by Galactic Longitude' \
            + f'\nVelocity Count: Sum={velGLonP180CountSum:,}' \
            + f' Nonzero = {velGLonP180CountNonzero} of {len(velGLonP180Count)}')
        #    rotation=90, verticalalignment='bottom')

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal518velGLonMin():
    # spectrum Maximums in dots

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global titleS                   # string
    global ezGalDispGrid            # integer
    #global fileFreqBinQty           # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 518 and 518 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal518velGLonMin.png'
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()
        #plt.plot(np.arange(-180, +181, 1), velGLonP180Count)
        #plt.plot(np.arange(-180, +181, 1), np.minimum(velGLonP180[~np.isnan(velGLonP180)][0]))
        plt.plot(np.arange(-180, +181, 1), np.minimum(velGLonP180[0]))

        plt.title(titleS)
        #plt.grid(ezGalDispGrid)
        plt.grid(0)

        plt.xlabel('Galactic Longitude (degrees)')
        plt.xlim(180, -180)        # in degrees
        plt.xticks([ 180,   90,   0,   -90,   -180],
                   ['180', '90', '0', '-90', '-180'])

        # if any Galactic plane crossings, velGLonP180 has been (partially?) filled with averages
        velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
        print(' velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )
        print()

        plt.ylabel('Minimum Velocity (km/s) by Galactic Longitude' \
            + f'\nVelocity Count: Sum={velGLonP180CountSum:,}' \
            + f' Nonzero = {velGLonP180CountNonzero} of {len(velGLonP180Count)}')
        #    rotation=90, verticalalignment='bottom')

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal520velGLonPolar():

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180CountSum      # integer

    global titleS                   # string
    global ezGalDispGrid            # integer
    global fileFreqBinQty           # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 520 and 520 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal520velGLonPolar.png'     # Velocity by Galactic Longitude with pcolormesh
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()

        fig = plt.figure()
        ax = fig.add_subplot(projection='polar')

        rad = np.arange(0, fileFreqBinQty, 1)        # 0 to fileFreqBinQty in freqBins
        azm = np.linspace(0, np.pi + np.pi, 361, endpoint=True)
        r, theta = np.meshgrid(rad, azm)

        plt.grid(0)
        im = plt.pcolormesh(theta, r, velGLonP180.T, cmap=plt.get_cmap('gnuplot'), shading='auto')

        fig.colorbar(im, ax=ax, pad=0.1)

        polarPlot = plt.plot(azm, r, color='black', linestyle='none')
        plt.grid(1)


        plt.title(titleS)

        ax.set_rgrids((fileFreqBinQty/2.,), ('',))
        ax.set_theta_zero_location('S', offset=0.)
        ax.set_thetagrids((90, 180, 270, 360), ('-90', '0', '90', '180 and -180'))

        ax.set_xlabel('Galactic Longitude (degrees) of Galaxy Plane Spectra')
        ax.set_ylabel('Radius Is Increasing "Velocity",\n\n' \
            + 'Radius Is Increasing Receding,\n\n' \
            + 'Radius Is Decreasing Doppler\n\n')

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal521velGLonPolarCount():

    global plotCountdown            # integer
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global titleS                   # string
    global ezGalDispGrid            # integer
    global fileFreqBinQty           # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 521 and 521 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal521velGLonPolarCount.png'     # Velocity by Galactic Longitude with pcolormesh
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()

        fig = plt.figure()
        ax = fig.add_subplot(projection='polar')

        rad = np.arange(0, fileFreqBinQty, 1)        # 0 to fileFreqBinQty in freqBins
        azm = np.linspace(0, np.pi + np.pi, 361, endpoint=True)
        r, theta = np.meshgrid(rad, azm)

        velGLonP180CountPolar = np.zeros_like(velGLonP180.T, dtype=int)
        for gLonP180 in range(361):
            if velGLonP180Count[gLonP180]:
                velGLonP180CountPolar[gLonP180, :] += velGLonP180Count[gLonP180]

        plt.grid(0)
        im = plt.pcolormesh(theta, r, velGLonP180CountPolar, cmap=plt.get_cmap('gnuplot'), shading='auto')

        fig.colorbar(im, ax=ax, pad=0.1)

        polarPlot = plt.plot(azm, r, color='black', linestyle='none')
        plt.grid(1)

        plt.title(titleS)

        ax.set_rgrids((fileFreqBinQty/2.,), ('',))
        ax.set_theta_zero_location('S', offset=0.)
        ax.set_thetagrids((90, 180, 270, 360), ('-90', '0', '90', '180 and -180'))

        ax.set_xlabel('Galactic Longitude (degrees) of Galaxy Plane Spectra')
        ax.set_ylabel('Velocity Data Counts by Galactic Longitude' \
            + f'\n\nVelocity Count Sum = {velGLonP180CountSum:,}' \
            + f'\n\nVelocity Count Nonzero = {np.count_nonzero(velGLonP180Count)}' \
            + f' of {len(velGLonP180Count)}\n\n')

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal530galDecGLon():

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer
    global galDecP90GLonP180Count   # integer 2d array

    global titleS                   # string
    global ezGalDispGrid            # integer
    #global fileFreqBinQty           # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 530 and 530 <= ezGalPlotRangeL[1] and velGLonP180CountSum:

        pltNameS = 'ezGal530galDecGLon.png'
        print()
        print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

        plt.clf()

        xi = np.arange(-180, +181, 1)           # +180 thru -180 degrees in degrees, galaxy centered
        yi = np.arange(0, 181, 1)               # 0 thru 180 decP90

        xi, yi = np.meshgrid(xi, yi)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        if 0:
            maskOffBelowThis = 0.975    # N0RQVHC
            maskOffBelowThis = 0.9      # WA6RSV
            maskOffBelowThis = -10
            print(' maskOffBelowThis = ', maskOffBelowThis)
            maskThisOff = (velGLonP180 < maskOffBelowThis)
            velGLonP180[maskThisOff] = np.nan

        pts = plt.contourf(xi, yi, galDecP90GLonP180Count, 20, cmap=plt.get_cmap('gnuplot'))

        plt.axhline(y =  90, linewidth=0.5, color='black')
        plt.axvline(x =  90, linewidth=0.5, color='black')
        plt.axvline(x =   0, linewidth=0.5, color='black')
        plt.axvline(x = -90, linewidth=0.5, color='black')

        cbar = plt.colorbar(pts, orientation='vertical', pad=0.06)

        plt.title(titleS)
        #plt.grid(ezGalDispGrid)
        plt.grid(0)

        plt.xlabel('Galactic Longitude (degrees)')
        plt.xlim(180, -180)        # in degrees
        plt.xticks([180,   90,   0,   -90,   -180],
                   ['180', '90', '0', '-90', '-180'])

        plt.ylabel('Velocity Counts on Declination by Galactic Longitude' \
            + f'\nVelocity Count Sum = {velGLonP180CountSum:,}')
        #    rotation=90, verticalalignment='bottom')
        plt.ylim(0, 180)                # in decP90
        plt.yticks([0,     30,    60,    90,  120,  150,  180],
                   ['-90', '-60', '-30', '0', '30', '60', '90'])

        if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def findVelGLonEdges():
    # if needed, calculate velGLonUEdge and velGLonLEdgeFreqBin

    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global fileFreqBinQty           # integer
    global freqStep                 # float
    global freqCenter               # float
    global ezGalPlotRangeL          # integer list

    global ezGalVelGLonEdgeFrac     # float
    global velGLonUEdge             # float array
    global velGLonLEdge             # float array

    # calculate velGLonUEdge and velGLonLEdge, needed later for
    #   plotEzGal540velGLonEdgesB()
    #   plotEzGal540velGLonEdgesB()
    #   plotEzGal541velGLonEdges()
    #   plotEzGal550galRot()
    #   plotEzGal560galMass()
    if not (ezGalPlotRangeL[0] <= 569 and 540 <= ezGalPlotRangeL[1] and velGLonP180CountSum):
        return(0)       # calculation not needed

    print()
    print('                          findVelGLonEdges ================================')

    # if any Galactic plane crossings, velGLonP180 has been (partially?) filled with averages
    velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
    print('                         velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )
    velGLonP180Max  = np.nanmax(velGLonP180)
    #velGLonP180Mean = np.mean(velGLonP180[~np.isnan(velGLonP180)])
    velGLonP180Mean = np.mean(velGLonP180)
    velGLonP180Min  = np.nanmin(velGLonP180)
    print('                         velGLonP180Max  =', velGLonP180Max)
    print('                         velGLonP180Mean =', velGLonP180Mean)
    print('                         velGLonP180Min  =', velGLonP180Min)

    #velGLonP180Max = velGLonP180.max()
    #velGLonP180Min = velGLonP180.min()
    if 0:
        # ezGalVelGLonEdgeLevel value trumps any ezGalVelGLonEdgeFrac value,
        # if ezGalVelGLonEdgeLevel not 0, then ezGalVelGLonEdgeFrac ignored
        if ezGalVelGLonEdgeLevel:
            velGLonEdgeLevel = ezGalVelGLonEdgeLevel
            ylabel2S = f'ezGalVelGLonEdgeLevel = {ezGalVelGLonEdgeLevel:0.6f}'
        else:
            velGLonEdgeLevel = ezGalVelGLonEdgeFrac * (velGLonP180Max - velGLonP180Min) + velGLonP180Min
            ylabel2S += f'ezGalVelGLonEdge: Frac={ezGalVelGLonEdgeFrac:0.4f} Level={ezGalVelGLonEdgeLevel:0.4f}'
            #ylabel2S  = f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.4f}\n\n'
            #ylabel2S += f'velGLonEdgeLevel = {velGLonEdgeLevel:0.6f}'
        print(' ezGalVelGLonEdgeFrac  =', ezGalVelGLonEdgeFrac)
        print(' ezGalVelGLonEdgeLevel =', ezGalVelGLonEdgeLevel)
        print('                         velGLonEdgeLevel =', velGLonEdgeLevel)

    # only ezGalVelGLonEdgeFrac supported
    if 1:
        velGLonEdgeLevel = ezGalVelGLonEdgeFrac * (velGLonP180Max - velGLonP180Min) + velGLonP180Min
        print()
        print('                         ezGalVelGLonEdgeFrac  =', ezGalVelGLonEdgeFrac)
        print('                         velGLonEdgeLevel      =', velGLonEdgeLevel)

    velGLonUEdgeFreqBin = np.full(361, np.nan)      # unused nan will not plot
    velGLonLEdgeFreqBin = np.full(361, np.nan)      # unused nan will not plot

    # for Galactic plane crossings, velGLonUEdge will be the max velocity vs Galactic Longitude.
    # Page 46 of
    #   https://f1ehn.pagesperso-orange.fr/pages_radioastro/Images_Docs/Radioastro_21cm_2012b.pdf

    for gLonP180 in range(361):
        if velGLonP180Count[gLonP180]:
            # calculate Upper and Lower Detection Doppler of this velGLonP180 spectrum, in freqBin
            # https://thispointer.com/find-the-index-of-a-value-in-numpy-array/
            # Tuple of arrays returned :  (array([ 4,  7, 11], dtype=int32),)
            # velGLonP180AboveLevelFreqBins are the freqBins with velGLonP180 >= velGLonEdgeLevel
            velGLonP180AboveLevelFreqBins = np.where(velGLonEdgeLevel <= velGLonP180[:, gLonP180])[0]

            if velGLonP180AboveLevelFreqBins.any():
                velGLonUEdgeFreqBinThis = velGLonP180AboveLevelFreqBins[-1] # use last  element of list
                velGLonLEdgeFreqBinThis = velGLonP180AboveLevelFreqBins[ 0] # use first element of list

                # for the current gLonP180, ignoring nan,
                #   remember the max velGLonUEdgeFreqBinThis and min velGLonLEdgeFreqBinThis

                if np.isnan(velGLonUEdgeFreqBin[gLonP180]):     # if empty
                    velGLonUEdgeFreqBin[gLonP180] = velGLonUEdgeFreqBinThis
                else:
                    # keep max value
                    velGLonUEdgeFreqBin[gLonP180] = \
                        max(velGLonUEdgeFreqBin[gLonP180], velGLonUEdgeFreqBinThis)

                if np.isnan(velGLonLEdgeFreqBin[gLonP180]):     # if empty
                    velGLonLEdgeFreqBin[gLonP180] = velGLonLEdgeFreqBinThis
                else:
                    # keep min value
                    velGLonLEdgeFreqBin[gLonP180] = \
                        min(velGLonLEdgeFreqBin[gLonP180], velGLonLEdgeFreqBinThis)

    # convert velGLonUEdgeFreqBin and velGLonLEdgeFreqBin in freqBin to velocity (km/s)
    #   speed of light = 299,792,458 meters per second
    #   freqStep = 0.009411764705881818     # from plotPrep()
    #   freqCenter = 1420.406               # from plotPrep()
    freqBinVelocityStep = freqStep * (299792458. / freqCenter) / 1000.                     # km/s
    # velocity = (fileFreqBin doppler MHz) * (299792458. m/s / 1420.406 MHz) / 1000. = km/s
    velGLonUEdge = (velGLonUEdgeFreqBin - int(fileFreqBinQty / 2)) * freqBinVelocityStep   # km/s
    velGLonLEdge = (velGLonLEdgeFreqBin - int(fileFreqBinQty / 2)) * freqBinVelocityStep   # km/s



def plotEzGal540velGLonEdgesB():

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global velocitySpanMax          # float
    global velocityBin              # float array

    global titleS                   # string
    global ezGalDispGrid            # integer
    global ezGalPlotRangeL          # integer list

    global ezGalVelGLonEdgeFrac     # float
    global velGLonUEdge             # float array
    global velGLonLEdge             # float array

    #global dopplerSpanD2            # float
    #global freqCenter               # float
    #global fileFreqBinQty           # integer

    plotCountdown -= 1

    # if not wanted, or nothing in velGLonP180 to save or plot
    if not (ezGalPlotRangeL[0] <= 540 and 540 <= ezGalPlotRangeL[1] and velGLonP180CountSum):
        return(0)       # plot not needed

    pltNameS = f'ezGal540velGLonEdgesB_{ezGalVelGLonEdgeFrac:0.4f}.png'
    print()
    print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

    plt.clf()

    xi = np.arange(-180, +181, 1)           # +180 thru -180 degrees in degrees, galaxy centered
    #yi = np.arange(0, fileFreqBinQty, 1)    # 0 to fileFreqBinQty in freqBins
    # speed of light = 299,792,458 meters per second
    #    rawPlotPrep ===============
    #       fileFreqMin = 1419.2
    #       fileFreqMax = 1421.6
    #       freqStep = 0.009411764705881818
    #       dopplerSpanD2 = 1.1999999999999318
    #       freqCenter = 1420.4
    # velocity = (fileFreqBin doppler MHz) * (299792458. m/s / 1420.406 MHz) / 1000. = km/s
    # velocity spans = -dopplerSpanD2 * (299792458. / freqCenter) thru
    #                  +dopplerSpanD2 * (299792458. / freqCenter)
    #velocitySpanMax = +1.1999999999999318 * (299792458. / 1420.406) / 1000.  # = 253.273324388 km/s
    #velocitySpanMax = +dopplerSpanD2 * (299792458. / freqCenter) / 1000.  # = 253.273324388 km/s
    #yi = np.linspace(-velocitySpanMax, velocitySpanMax, fileFreqBinQty)
    yi = velocityBin + 0.

    xi, yi = np.meshgrid(xi, yi)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    pts = plt.contourf(xi, yi, velGLonP180, 100, cmap=plt.get_cmap('gnuplot'))
    #pts = plt.contourf(xi, yi, velGLonP180, 100, cmap=plt.get_cmap('gnuplot'), vmin=1.025, vmax=1.21)

    # horizonal thin black line
    plt.axhline(y =   0, linewidth=0.5, color='black')

    # vertical thin black lines
    plt.axvline(x =  90, linewidth=0.5, color='black')
    plt.axvline(x =   0, linewidth=0.5, color='black')
    plt.axvline(x = -90, linewidth=0.5, color='black')

    cbar = plt.colorbar(pts, orientation='vertical', pad=0.06)

    plt.title(titleS)
    #plt.grid(ezGalDispGrid)
    plt.grid(0)

    plt.xlabel('Galactic Longitude (degrees)')
    plt.xlim(180, -180)        # in degrees
    plt.xticks([ 180,   90,   0,   -90,   -180],
               ['180', '90', '0', '-90', '-180'])

    plt.ylim(-velocitySpanMax, velocitySpanMax)        # in velocity

    # all used velGLonUEdgeFreqBin, are red  shifted
    plt.plot(np.arange(-180, +181, 1), velGLonUEdge, 'r.')

    # all used velGLonLEdgeFreqBin, are blue shifted
    plt.plot(np.arange(-180, +181, 1), velGLonLEdge, 'b.')


    plt.title(titleS)
    #plt.grid(ezGalDispGrid)
    plt.grid(0)

    plt.xlabel('Galactic Longitude (degrees)')
    plt.xlim(180, -180)        # in degrees
    plt.xticks([ 180,   90,   0,   -90,   -180],
               ['180', '90', '0', '-90', '-180'])

    ylabelS = 'Velocity Edges: Upper (Red) and Lower (Blue) (km/s)\n'
    #    # if ezGalVelGLonEdgeLevel not 0, then ezGalVelGLonEdgeFrac ignored
    #    if ezGalVelGLonEdgeLevel:
    #        ylabelS += f'ezGalVelGLonEdgeLevel = {ezGalVelGLonEdgeLevel:0.6f}'
    #    else:
    #        ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.6f}\n\n'
    #        ylabelS += f'velGLonEdgeLevel = {velGLonEdgeLevel:0.6f}'
    #ylabelS += f'ezGalVelGLonEdge: Frac={ezGalVelGLonEdgeFrac:0.4f} Level={ezGalVelGLonEdgeLevel:0.4f}'
    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.4f}'
    plt.ylabel(ylabelS)
    #plt.ylim(-270, 270)

    if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
        os.remove(pltNameS)
    plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal541velGLonEdges():

    global plotCountdown            # integer
    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer

    global ezGalVelGLonEdgeFrac     # float
    #global ezGalVelGLonEdgeLevel    # float
    global velGLonUEdge             # float array
    global velGLonLEdge             # float array

    global titleS                   # string
    global ezGalDispGrid            # integer
    global fileFreqBinQty           # integer
    global dopplerSpanD2            # float
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if not wanted, or nothing in velGLonP180 to save or plot
    if not (ezGalPlotRangeL[0] <= 541 and 541 <= ezGalPlotRangeL[1] and velGLonUEdge.any()):
        return(0)       # plot not needed

    pltNameS = f'ezGal541velGLonEdges_{ezGalVelGLonEdgeFrac:0.4f}.png'
    print()
    print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

    plt.clf()

    # horizonal thin black line
    plt.axhline(y =   0, linewidth=0.5, color='black')

    # vertical thin black lines
    plt.axvline(x =  90, linewidth=0.5, color='black')
    plt.axvline(x =   0, linewidth=0.5, color='black')
    plt.axvline(x = -90, linewidth=0.5, color='black')

    # all used velGLonUEdgeFreqBin, are red  shifted
    plt.plot(np.arange(-180, +181, 1), velGLonUEdge, 'r.')

    # all used velGLonLEdgeFreqBin, are blue shifted
    plt.plot(np.arange(-180, +181, 1), velGLonLEdge, 'b.')


    plt.title(titleS)
    #plt.grid(ezGalDispGrid)
    plt.grid(0)

    plt.xlabel('Galactic Longitude (degrees)')
    plt.xlim(180, -180)        # in degrees
    plt.xticks([ 180,   90,   0,   -90,   -180],
               ['180', '90', '0', '-90', '-180'])

    ylabelS = 'Velocity Upper Edge (Red) and Lower Edge (Blue)  (km/s)\n'
    #    # if ezGalVelGLonEdgeLevel not 0, then ezGalVelGLonEdgeFrac ignored
    #    if ezGalVelGLonEdgeLevel:
    #        ylabelS += f'ezGalVelGLonEdgeLevel = {ezGalVelGLonEdgeLevel:0.6f}'
    #    else:
    #        ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.6f}\n\n'
    #        ylabelS += f'velGLonEdgeLevel = {velGLonEdgeLevel:0.6f}'
    #ylabelS += f'ezGalVelGLonEdge  Frac={ezGalVelGLonEdgeFrac:0.4f}  Level={ezGalVelGLonEdgeLevel:0.4f}'
    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.4f}'
    plt.ylabel(ylabelS)
    plt.ylim(-270, 270)

    if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
        os.remove(pltNameS)
    plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal550galRot():

    global plotCountdown            # integer
    #global velGLonP180              # float 2d array
    #global velGLonP180Count         # integer array
    #global velGLonP180CountSum      # integer

    global ezGalVelGLonEdgeFrac     # float
    #global ezGalVelGLonEdgeLevel    # float
    global velGLonUEdge             # float array
    #global velGLonLEdge             # float array

    global titleS                   # string
    global ezGalDispGrid            # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if not wanted, or nothing in velGLonP180 to save or plot
    if not (ezGalPlotRangeL[0] <= 550 and 550 <= ezGalPlotRangeL[1] and velGLonUEdge.any()):
        return(0)       # plot not needed

    pltNameS = f'ezGal550galRot_{ezGalVelGLonEdgeFrac:0.4f}.png'
    print()
    print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')
    #print('                         velGLonUEdge =', velGLonUEdge)

    plt.clf()

    # Status: for Galactic plane crossings, velGLonUEdge are max velocities vs Galactic longitude.
    # Page 45 of https://f1ehn.pagesperso-orange.fr/pages_radioastro/Images_Docs/Radioastro_21cm_2012b.pdf
    #   says for 0 <= gLon <= 90 ("quadrant I"), the max Galactic velocity around Galactic center
    #   = galVelMax
    #   = galGasVelMaxKm + (Sun Galactic rotation speed) * sin(gLon)
    # https://en.wikipedia.org/wiki/Galactic_year says (Sun Galactic rotation speed) is 230 km/s
    #   = galGasVelMaxKm + (230 km/s)                    * sin(gLon)
    galGasVelMaxKm = np.add(velGLonUEdge[180:180 + 91], 230 * np.sin(np.radians(np.arange(91))))   # in km/s

    #print('                         velGLonUEdge[180:180 + 91] =', velGLonUEdge[180:180 + 91])
    #print('                         np.sin(np.radians(np.arange(91)) =', np.sin(np.radians(np.arange(91))))
    #print('                         galGasVelMaxKm =', galGasVelMaxKm)

    # Page 54 says for 0 <= gLon <= 90 ("quadrant I"), the Galactic gas radius from Galactic center
    #   = galGasRadiusKm
    #   = (Solar radius from Galactic center) * (Sun Galactic rotation speed) * sin(gLon) /
    #       (Sun Galactic rotation speed) * sin(gLon) + velGLonUEdge[180:180 + 91]
    # https://en.wikipedia.org/wiki/Galactic_Center says (Solar radius from Galactic center) is 26,000 ly
    # https://en.wikipedia.org/wiki/Light-year says light year lt is 9.46e12 km
    #   = (26000 ly * 9.46e12 km/ly)          * (230 km/s)                    * sin(gLon) /
    #       (230 km/s)                    * sin(gLon) + velGLonUEdge[180:180 + 91]
    galGasRadiusKm = (26000. * 9.46e12) * 230. * np.sin(np.radians(np.arange(91))) \
        / 230. * np.sin(np.radians(np.arange(91))) + velGLonUEdge[180:180 + 91]     # in km
    galGasRadiusLy = galGasRadiusKm / 9.46e12                                       # in light years
    print('                         galGasRadiusLy.max() =', galGasRadiusLy.max())

    plt.plot(galGasRadiusLy, galGasVelMaxKm, 'g.')

    plt.title(titleS)
    plt.grid(ezGalDispGrid)
    plt.xlabel('Gas Radius from Galactic Center (Light Years)  (Sun = 26,000 ly)')
    plt.xlim(0, 26000)        # radius from 0 to Solar radius from Galactic center (=26000 light years)
    plt.xticks([0,   5000.,   10000.,   15000.,   20000.,   25000.],
               ['0', '5,000', '10,000', '15,000', '20,000', '25,000'])

    ylabelS = 'Gas Max Velocity around Galactic Center (km/s)\n'
    # if ezGalVelGLonEdgeLevel not 0, then ezGalVelGLonEdgeFrac ignored
    #if ezGalVelGLonEdgeLevel:
    #    ylabelS += f'ezGalVelGLonEdgeLevel = {ezGalVelGLonEdgeLevel:0.6f}'
    #else:
    #    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.6f}\n\n'
    #    ylabelS += f'velGLonEdgeLevel = {velGLonEdgeLevel:0.6f}'
    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.4f}'
    plt.ylabel(ylabelS)

    if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
        os.remove(pltNameS)
    plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal551galRot2():
    # Galaxy Rotation in 2 quadrants (gLon from 0 to 180)

    global plotCountdown            # integer
    #global velGLonP180              # float 2d array
    #global velGLonP180Count         # integer array
    #global velGLonP180CountSum      # integer

    global ezGalVelGLonEdgeFrac     # float
    #global ezGalVelGLonEdgeLevel    # float
    global velGLonUEdge             # float array
    #global velGLonLEdge             # float array

    global titleS                   # string
    global ezGalDispGrid            # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if not wanted, or nothing in velGLonP180 to save or plot
    if not (ezGalPlotRangeL[0] <= 551 and 551 <= ezGalPlotRangeL[1] and velGLonUEdge.any()):
        return(0)       # plot not needed

    pltNameS = f'ezGal551galRot2_{ezGalVelGLonEdgeFrac:0.4f}.png'
    print()
    print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')
    print('                         velGLonUEdge =', velGLonUEdge)

    plt.clf()

    # https://en.wikipedia.org/wiki/Galactic_quadrant
    #   where l is galactic longitude:
    #       1st galactic quadrant   I –   0 ≤ l ≤  90 degrees
    #       2nd galactic quadrant  II –  90 ≤ l ≤ 180 degrees
    #       3rd galactic quadrant III – 180 ≤ l ≤ 270 degrees
    #       4th galactic quadrant  IV – 270 ≤ l ≤ 360 degrees

    # Status: for Galactic plane crossings, velGLonUEdge are max radial-from-Sun velocities vs Galactic longitude.
    # Page 45 of https://f1ehn.pagesperso-orange.fr/pages_radioastro/Images_Docs/Radioastro_21cm_2012b.pdf
    #   says for 0 <= gLon <= 90 ("quadrant I"), the max gas velocity around Galactic center
    #   = galVelMax
    #   = galGasVelMaxKm + (Sun Galactic rotation speed) * sin(gLon)
    # https://en.wikipedia.org/wiki/Galactic_year says (Sun Galactic rotation speed) is 230 km/s
    #   = galGasVelMaxKm + (230 km/s)                    * sin(gLon)
    galGasVelMaxUKm = np.add(velGLonUEdge[180:180 + 91], 230 * np.sin(np.radians(np.arange(91))))   # in km/s
    galGasVelMaxLKm = np.add(velGLonLEdge[90:90 + 91][::-1], 230 * np.sin(np.radians(np.arange(91))))   # in km/s






    #   for 90 <= gLon <= 180 ("quadrant II"), the max Galactic velocity around Galactic center
    #   = galVelMax
    #   = galGasVelMaxKm / sin(gLon) + (Sun Galactic rotation speed) * sin(gLon)
    #   = galGasVelMaxKm / sin(gLon) + (230 km/s)                    * sin(gLon)
    #############galGasVelMax2QKm = np.add(velGLonUEdge[180 + 91:180 + 181] / np.sin(np.radians(np.arange(91, 181))), \
    #############    230 * np.sin(np.radians(np.arange(91, 181))))   # in km/s





    #   for 90 <= gLon <= 180 ("quadrant II"), the max Galactic velocity around Galactic center
    #   = galVelMax
    #   = galGasVelMaxKm + (Sun Galactic rotation speed) / sin(gLon)
    #   = galGasVelMaxKm + (230 km/s)                    / sin(gLon)
    #galGasVelMax2QKm = np.add(velGLonUEdge[180 + 91:180 + 180], 230 / np.sin(np.radians(np.arange(91, 180))))   # in km/s







    #galGasVelMaxKm = np.concatenate([galGasVelMaxKm, galGasVelMax2QKm])
    #print('                         velGLonUEdge[180:180 + 91] =', velGLonUEdge[180:180 + 91])
    #print('                         np.sin(np.radians(np.arange(91)) =', np.sin(np.radians(np.arange(91))))
    print('                         galGasVelMaxUKm =', galGasVelMaxUKm)






    plt.plot(galGasVelMaxUKm, 'r.')
    plt.plot(galGasVelMaxLKm, 'b.')

    galGasRadiusUKm = (26000. * 9.46e12) * 230. * np.sin(np.radians(np.arange(91))) \
        / 230. * np.sin(np.radians(np.arange(91))) + galGasVelMaxUKm             # in km
    galGasRadiusLKm = (26000. * 9.46e12) * 230. * np.sin(np.radians(np.arange(91))) \
        / 230. * np.sin(np.radians(np.arange(91))) + galGasVelMaxLKm             # in km

    if 0:
        plt.plot(230. * np.sin(np.radians(np.arange(91))), 'g.')
        plt.plot(230. * np.sin(np.radians(np.arange(91))) + galGasVelMaxKm, 'b.')
        plt.plot(np.sin(np.radians(np.arange(91))) * galGasVelMaxKm, 'r.')

    if 0:#################################
    
        # GC = Galactic Center
        # l  = gLon = gLongitude (GC at center 0 degrees)
        # RS = Radius of Sun from GC = distance
        # R  = Radius of gas cloud from GC = distance
        # galGasVelMaxUKm = maximum velocity of gas cloud from the Sun, in km/second
        # galGasVelMaxLKm = mimimum velocity of gas cloud from the Sun, in km/second
        #   Maybe galGasVelMaxUKm should be labeled galGasVelMaxKm,
        #   and   galGasVelMaxLKm should be labeled galGasVelMinKm.
        #
        # For 0 <= gLon <= 90 ("quadrant I"),
        #   the gas cloud radius, R, is such that R is tangential from the Sun for a given gLon, l.
        #   Then the galGasVelMaxUKm is the radial velocity from the Sun, of that gas cloud.
        #   And even is the gas cloud velocity around the Galactic Center.
        #   Convenient.
        #
        # But for 90 <= gLon <= 180 ("quadrant II"),
        #   For a given gLon, l. there is no trick to identify the source of the 1420 MHz emission.
        #   It could be any gas cloud along that vector from the Sun, at any R.
        #       Without a known R, the velocity radial from the Sun,
        #       can not be used to calculate the gas cloud velocity around the Galactic Center.
        #
        # For 270 <= gLon <= 360 ("quadrant IV"),
        #   the quadrant I trick, but using galGasVelMaxLKm, did not work.
        #   The professional Velocity-GalacticLongitude plot is not symetrical about the gLon=0 center.
        #   Also, from Colorado, not much data is available for gLon less than 0.


        # as gLon approaches 90 degrees, R approaches RSun, and velGLonUEdge approaches 0,
        #   = galGasRadiusKm
        #   = (Solar radius from Galactic center) * (Sun Galactic rotation speed) * sin(gLon) /
        #       (Sun Galactic rotation speed) * sin(gLon) + velGLonUEdge
        # approaches
        #   = (Solar radius from Galactic center) * (Sun Galactic rotation speed) /
        #       (Sun Galactic rotation speed)
        #   = (Solar radius from Galactic center)

        #galGasRadiusQ2Km = (26000. * 9.46e12) / np.sin(np.radians(np.arange(91, 180)))    # in km
        #galGasRadiusQ2Km = (26000. * 9.46e12) / np.sin(np.radians(np.arange(91, 170)))    # in km
        #galGasRadiusKm = np.concatenate([galGasRadiusKm, galGasRadiusQ2Km])

        #plt.plot(galGasRadiusKm / (26000. * 9.46e12), 'g.')
        plt.plot(galGasRadiusUKm, 'r.')
        plt.plot(galGasRadiusLKm, 'b.')
        # 26000. * 9.46e12 is 2.4596e+17
        
    if 0:
        # Page 54 says for 0 <= gLon <= 90 ("quadrant I"), the Galactic gas radius from Galactic center
        #   = galGasRadiusKm
        #   = (Solar radius from Galactic center) * (Sun Galactic rotation speed) * sin(gLon) /
        #       (Sun Galactic rotation speed) * sin(gLon) + velGLonUEdge[180:180 + 91]
        # https://en.wikipedia.org/wiki/Galactic_Center says (Solar radius from Galactic center) is 26,000 ly
        # https://en.wikipedia.org/wiki/Light-year says light year lt is 9.46e12 km
        #   = (26000 ly * 9.46e12 km/ly)          * (230 km/s)                    * sin(gLon) /
        #       (230 km/s)                    * sin(gLon) + velGLonUEdge[180:180 + 91]
        #################galGasRadiusKm = (26000. * 9.46e12) * 230. * np.sin(np.radians(np.arange(91))) \
        #################    / 230. * np.sin(np.radians(np.arange(91))) + velGLonUEdge[180:180 + 91]             # in km

        #   for 90 <= gLon <= 180 ("quadrant II"), the max Galactic velocity around Galactic center
        #   = galVelMax
        #   = galGasVelMaxKm / sin(gLon) + (Sun Galactic rotation speed) * sin(gLon)
        galGasRadiusKm = (26000. * 9.46e12) * 230. * np.sin(np.radians(np.arange(180))) \
            / 230. * np.sin(np.radians(np.arange(180))) + velGLonUEdge[180:180 + 91]    # in km

        galGasRadiusLy = galGasRadiusKm / 9.46e12                                       # in light years
        print('                         galGasRadiusLy.max() =', galGasRadiusLy.max())

        #plt.plot(galGasRadiusLy, galGasVelMaxKm, 'g.')

    plt.title(titleS)
    plt.grid(ezGalDispGrid)
    plt.xlabel('Gas Radius from Galactic Center (Light Years)  (Sun = 26,000 ly)')
    ##########plt.xlim(0, 26000)        # radius from 0 to Solar radius from Galactic center (=26000 light years)
    ##########plt.xticks([0,   5000.,   10000.,   15000.,   20000.,   25000.],
    ##########           ['0', '5,000', '10,000', '15,000', '20,000', '25,000'])

    ylabelS = 'Gas Max Velocity around Galactic Center (km/s)\n'
    # if ezGalVelGLonEdgeLevel not 0, then ezGalVelGLonEdgeFrac ignored
    #if ezGalVelGLonEdgeLevel:
    #    ylabelS += f'ezGalVelGLonEdgeLevel = {ezGalVelGLonEdgeLevel:0.6f}'
    #else:
    #    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.6f}\n\n'
    #    ylabelS += f'velGLonEdgeLevel = {velGLonEdgeLevel:0.6f}'
    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.4f}'
    plt.ylabel(ylabelS)

    if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
        os.remove(pltNameS)
    plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal560galMass():

    global plotCountdown            # integer
    #global velGLonP180              # float 2d array
    #global velGLonP180Count         # integer array
    #global velGLonP180CountSum      # integer

    global ezGalVelGLonEdgeFrac     # float
    #global ezGalVelGLonEdgeLevel    # float
    global velGLonUEdge             # float array
    #global velGLonLEdge             # float array

    global titleS                   # string
    global ezGalDispGrid            # integer
    global ezGalPlotRangeL          # integer list

    plotCountdown -= 1

    # if not wanted, or nothing in velGLonP180 to save or plot
    if not (ezGalPlotRangeL[0] <= 560 and 560 <= ezGalPlotRangeL[1] and velGLonUEdge.any()):
        return(0)       # plot not needed

    pltNameS = f'ezGal560galMass_{ezGalVelGLonEdgeFrac:0.4f}.png'
    print()
    print('  ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ================================')

    plt.clf()

    # Status: for Galactic plane crossings, velGLonUEdge are max velocities vs Galactic longitude.
    # Page 45 of https://f1ehn.pagesperso-orange.fr/pages_radioastro/Images_Docs/Radioastro_21cm_2012b.pdf
    #   says for 0 <= gLon <= 90 ("quadrant I"), the max Galactic velocity around Galactic center
    #   = galVelMax
    #   = galGasVelMaxKm + (Sun Galactic rotation speed) * sin(gLon)
    # https://en.wikipedia.org/wiki/Galactic_year says (Sun Galactic rotation speed) is 230 km/s
    #   = galGasVelMaxKm + (230 km/s)                      * sin(gLon)
    galGasVelMaxKm = np.add(velGLonUEdge[180:180 + 91], 230 * np.sin(np.radians(np.arange(91))))   # in km/s
    #print('                         velGLonUEdge[180:180 + 91] =', velGLonUEdge[180:180 + 91])
    #print('                         np.sin(np.radians(np.arange(91)) =', np.sin(np.radians(np.arange(91))))
    #print('                         galGasVelMaxKm =', galGasVelMaxKm)

    # Page 54 says for 0 <= gLon <= 90 ("quadrant I"), the Galactic gas radius from Galactic center
    #   = galGasRadiusKm
    #   = (Solar radius from Galactic center)      * (Sun Galactic rotation speed) * sin(gLon) /
    #       (Sun Galactic rotation speed) * sin(gLon) + galGasVelMaxKm
    # https://en.wikipedia.org/wiki/Galactic_Center says (Solar radius from Galactic center) is 26,000 ly
    # https://en.wikipedia.org/wiki/Light-year says light year lt is 9.46e12 km
    #   = (26000 ly * 9.46e12 km/ly)               * (230 km/s)                    * sin(gLon) /
    #       (230 km/s)                    * sin(gLon) + galGasVelMaxKm
    galGasRadiusKm = (26000. * 9.46e12) * 230. * np.sin(np.radians(np.arange(91))) \
        / 230. * np.sin(np.radians(np.arange(91))) + galGasVelMaxKm             # in km
    galGasRadiusLy = galGasRadiusKm / 9.46e12                                   # in light years
    print('                         galGasRadiusLy.max() =', galGasRadiusLy.max())

    # https://phys.libretexts.org/Bookshelves/University_Physics/Book%3A_Physics_(Boundless)/5%3A_Uniform_Circular_Motion_and_Gravitation/5.6%3A_Keplers_Laws
    # equation "(5.6.20)" says G * M / r = v * v
    # M = v * v * r / G
    # with large center mass M, radius r, and gravitational constant G (6.6743e-11 m3 kg-1 s-2)

    # M = v * v * r / G
    # M = (km/s) * (km/s) * (km) / (m3 kg-1 s-2))
    # M = (km/s) * (km/s) * (km) * (m-3 kg s2))
    # M = (k) * (k) * (k) * kg
    galGasVelMaxM = galGasVelMaxKm * 1e3            # km/s to meters/s
    galGasRadiusM = galGasRadiusKm * 1e3            # km   to meters
    galMassKg = np.multiply(np.multiply(galGasVelMaxM, galGasVelMaxM), galGasRadiusM) / 6.6743e-11   # in kg
    print('                         np.nanmax(galMassKg) =', np.nanmax(galMassKg), 'kg')
    print(f'                         np.nanmax(galMassKg) / 1.98e30 = {(np.nanmax(galMassKg)/1.98e30):0.4g} solar masses')
    print('                         solar mass = 1.98e30 kg')
    #print('                         galMassKg =', galMassKg)
    # https://nypost.com/2019/03/11/astronomers-have-figured-out-how-much-the-milky-way-weighs
    # https://en.wikipedia.org/wiki/Milky_Way  says 1.15e12 solar masses
    # https://en.wikipedia.org/wiki/Solar_mass says solar mass is 1.98e30 kg
    # galMassKg prediction = 1.15e12 solarMasses * 1.98e30 kg/solarMasses= 2.277e42 kg
    # lto15hcg data finds np.nanmax(galMassKg) = 2.8552e+41 kg = about a tenth of prediction (missing is dark matter ?)
    #   https://en.wikipedia.org/wiki/Milky_Way says "90% of the mass of the galaxy is dark matter"

    plt.plot(galGasRadiusLy, galMassKg, 'b.')

    plt.title(titleS)
    plt.grid(ezGalDispGrid)
    plt.xlabel('Gas Radius from Galactic Center (Light Years)  (Sun = 26,000 ly)')
    plt.xlim(0, 26000)        # radius from 0 to Solar radius from Galactic center (=26000 light years)
    plt.xticks([0,   5000.,   10000.,   15000.,   20000.,   25000.],
               ['0', '5,000', '10,000', '15,000', '20,000', '25,000'])

    ylabelS = 'Enclosed Mass (kg)\n'
    # if ezGalVelGLonEdgeLevel not 0, then ezGalVelGLonEdgeFrac ignored
    #if ezGalVelGLonEdgeLevel:
    #    ylabelS += f'ezGalVelGLonEdgeLevel = {ezGalVelGLonEdgeLevel:0.6f}'
    #else:
    #    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.6f}\n\n'
    #    ylabelS += f'velGLonEdgeLevel = {velGLonEdgeLevel:0.6f}'
    ylabelS += f'ezGalVelGLonEdgeFrac = {ezGalVelGLonEdgeFrac:0.4f}'
    plt.ylabel(ylabelS)

    if os.path.exists(pltNameS):    # to force plot file date update, if file exists, delete it
        os.remove(pltNameS)
    plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal60XgLonSpectra():

    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer
    global antXTVTName              # string

    global velocitySpanMax          # float
    global velocityBin              # float array

    global plotCountdown            # integer
    global elevation                # float array
    global titleS                   # string
    global ezGalDispGrid            # integer
    #global byFreqBinX               # float array
    global ezGalPlotRangeL          # integer list

    plt.clf()
    pltNameS = 'ezGal60XgLonSpectra.png'

    velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
    print()
    #print(' velGLonP180Count =', velGLonP180Count)
    print(' velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )

    velGLonP180CountNonzeroIndex = np.nonzero(velGLonP180Count)
    #print(' velGLonP180CountNonzeroIndex =', velGLonP180CountNonzeroIndex)
    #print(' velGLonP180CountNonzeroIndex[0] =', velGLonP180CountNonzeroIndex[0])

    #velGLonP180MaxIndex = np.argmax(velGLonP180, axis=0)
    print()
    velGLonP180Max = velGLonP180.max()
    print(' gLon of maximum spectrum value =', np.argmax(np.argmax(velGLonP180 == velGLonP180Max, axis=0)) - 180)

    #yLimMax = 1.05 * velGLonP180Max
    yLimMax = 1.01 * velGLonP180Max
    print(' yLimMax =', yLimMax)

    # same ylim for all ezGal690gLonDegP180_nnnByFreqBinAvg plots
    #yLimMin = 0.95 * velGLonP180.min()
    yLimMin = 0.99 * velGLonP180.min()
    print(' yLimMin =', yLimMin)

    # Galactic quadrants 1 through 4
    for gQuadrant in range(1, 5):

        plotNumber = 600 + gQuadrant        # for this Galactic quadrant

        plotCountdown -= 1

        if ezGalPlotRangeL[0] <= plotNumber and plotNumber <= ezGalPlotRangeL[1] and velGLonP180CountSum:

            #pltNameS = 'ezGal600gLonSpectraQ{gQuadrant}.png'
            pltNameS = f'ezGal{plotNumber}gLonSpectra.png'
            print('    ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ============')

            plt.clf()

            #fig, axs = plt.subplots(6, 10, figsize=(10, 6), layout='constrained')
            fig, axs = plt.subplots(9, 10, figsize=(10, 6), layout='constrained')
            #fig, axs = plt.subplots(6, 10, layout='constrained')
            #print(' axs.flat[0:5] =', axs.flat[0:5])
            #for ax in zip(axs.flat, cases):
            axsFlat = axs.flat

            #plt.title(titleS, transform=plt.transPlot)
            #fig.suptitle('Google (GOOG) daily closing price')
            fig.suptitle(titleS, fontsize=12)

            #plt.ylabel('Average AntXTVT Spectra for Galaxy plane at' \
            #    + f'\n\nGalactic Longitudes of Galactic Quadrant {gQuadrant}', \
            #    rotation=90, verticalalignment='bottom')
            #fig.suptitle(titleS, fontsize=12, rotation=90))
            #fig.suptitle(titleS, fontsize=12, rotation='vertical')
            fig.suptitle(titleS + f'\nAverage {antXTVTName} Spectra for Galaxy plane at' \
                + f' Galactic Longitudes (Galactic Quadrant {gQuadrant})', fontsize=12)

            gLonP180Start = [-1, 180, 270, 0, 90][gQuadrant]

            # 0 through 90 in this quadrant
            for i in range(90):

                gLonP180 = gLonP180Start + i
                #print(' gLonP180 =', gLonP180)

                #print(' i =', i)
                #ax = axs.flat[i]
                ax = axsFlat[i]

                if velGLonP180Count[gLonP180]:
                    #gLonP180 = velGLonP180CountNonzeroIndex[0][gLonP180]

                    #ax.clear()

                    #ax.set_title(f'markevery={markevery}')
                    #ax.set_title(f'mark')
                    #ax.set_title(f'mark{velGLonP180CountNonzeroIndex[0][i]}')
                    #ax.set_title(f'gLon={velGLonP180CountNonzeroIndex[0][gLonP180]-180}')

                    #ax.plot(x, y, 'o', ls='-', ms=4, markevery=markevery)
                    #ax.plot(x, y, 'o', ls='-', ms=4, markevery=0.1)
                    #ax.plot(-byFreqBinX, velGLonP180[:, gLonP180], linewidth=0.5)
                    ax.plot(velocityBin, velGLonP180[:, gLonP180], linewidth=0.5)
                    ax.grid(1)
            
                    #ax.text(fontsize=10)
                        
                    #ax.set_xlim(-dopplerSpanD2, dopplerSpanD2)
                    ax.set_xlim(-velocitySpanMax, velocitySpanMax)
            
                    ax.set_ylim(yLimMin, yLimMax)

                    ax.tick_params('both',labelsize=5) 

                #else:
                    #ax.clear()
                    #ax.set_xticks([], [])
                    #ax.set_yticks([], [])

                ax.set_xticks([], [])
                ax.set_yticks([], [])
                ax.axvline(linewidth=0.5, color='b')

                #ax.set_title(f'gLongitude {gLonDegS}', fontsize=5)
                #ax.text(0.1, 0.9, 'gLon', fontsize=5)
                #ax.text(0.8, 0.8, gLonDegS, fontsize=5)
                #ax.text(0.01, 0.8, 'gLon', fontsize=5, transform=ax.transAxes)
                ax.text(0.02, 0.85, 'gLon', fontsize=5, transform=ax.transAxes)

                # add text with form of '+nnn' or '-nnn' degrees
                #ax.text(0.03, 0.85, 'gLon', fontsize=5, transform=ax.transAxes)
                #ax.text(0.8, 0.8, gLonDegS, fontsize=5, transform=ax.transAxes)
                #ax.text(0.8, 0.8, '-004', fontsize=5, transform=ax.transAxes)
                #ax.text(0.8, 0.8, gLonDegS, fontsize=5, transform=ax.transAxes)
                #ax.text(0.8, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes)
                if gLonP180 < 180:
                    gLonDegS = f'-{180 - gLonP180:03d}'        # '-nnn' with leading zeros
                    #ax.text(0.8, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes)
                else:
                    gLonDegS = f'+{gLonP180 - 180:03d}'        # '+nnn' with leading zeros
                    #ax.text(0.76, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes, horizontalalignment='right')
                    #ax.text(0.99, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes, horizontalalignment='right')
                ax.text(0.99, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes, horizontalalignment='right')

            if os.path.exists(pltNameS): # to force plot file date update, if file exists, delete it
                os.remove(pltNameS)
            plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



    if 0:
        plotCountdown -= 1
        plt.clf()

        # velGLonP180 stores increasing velocity, but X axis is increasing freq, so use -byFreqBinX
        #plt.plot(-byFreqBinX, velGLonP180[:, gLonP180])

        plt.title(titleS)
        plt.grid(ezGalDispGrid)

        #plt.xlabel('Doppler (MHz)')
        #plt.xlim(-dopplerSpanD2, dopplerSpanD2)
        plt.xlabel('Velocity (km/s)')
        #velocitySpanMax = +dopplerSpanD2 * (299792458. / freqCenter) / 1000.  # = 253.273324388 km/s
        plt.xlim(-velocitySpanMax, velocitySpanMax)

        if 0:
            # new ylim for each ezGal690gLonDegP180_nnnByFreqBinAvg plot
            yLimMin = 0.95 * velGLonP180[:, gLonP180].min()
            print(' yLimMin =', yLimMin)

            yLimMax = 1.05 * velGLonP180[:, gLonP180].max()
            print(' yLimMax =', yLimMax)

        plt.ylim(yLimMin, yLimMax)

        # create gLonDegS with form of '+nnn' or '-nnn' degrees
        if gLonP180 < 180:
            gLonDegS = f'-{180 - gLonP180:03d}'        # '-nnn' with leading zeros
        else:
            gLonDegS = f'+{gLonP180 - 180:03d}'        # '+nnn' with leading zeros

        plt.ylabel(f'Average {antXTVTName} Spectrum for Galaxy plane at' \
            + f'\n\nGalactic Longitude = {gLonDegS} degrees', \
            rotation=90, verticalalignment='bottom')

        if os.path.exists(pltNameS): # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal61XgLonSpectraCascade():

    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer
    global antXTVTName              # string

    #global fileFreqBinQty           # integer
    #global freqCenter               # float
    #global dopplerSpanD2            # float
    global velocitySpanMax          # float                 creation
    global velocityBin              # float array           creation

    global ezGal61XGain             # float

    global plotCountdown            # integer
    global elevation                # float array
    global titleS                   # string
    global ezGalDispGrid            # integer
    #global byFreqBinX               # float array
    global ezGalPlotRangeL          # integer list

    plt.clf()
    pltNameS = 'ezGal61XgLonSpectraCascade.png'

    velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
    print()
    #print(' velGLonP180Count =', velGLonP180Count)
    print(' velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )

    velGLonP180CountNonzeroIndex = np.nonzero(velGLonP180Count)
    #print(' velGLonP180CountNonzeroIndex =', velGLonP180CountNonzeroIndex)
    #print(' velGLonP180CountNonzeroIndex[0] =', velGLonP180CountNonzeroIndex[0])

    #velGLonP180MaxIndex = np.argmax(velGLonP180, axis=0)
    print()
    velGLonP180Max = velGLonP180.max()
    print(' gLon of maximum spectrum value =', np.argmax(np.argmax(velGLonP180 == velGLonP180Max, axis=0)) - 180)

    yLimMax = 1.01 * velGLonP180Max
    print(' yLimMax =', yLimMax)

    # same ylim for all ezGal690gLonDegP180_nnnByFreqBinAvg plots
    yLimMin = 0.99 * velGLonP180.min()
    print(' yLimMin =', yLimMin)

    # Galactic quadrants 0 (all) and quadrants 1 through 4
    for gQuadrant in range(0, 5):

        plotNumber = 610 + gQuadrant        # for this Galactic quadrant

        plotCountdown -= 1

        if ezGalPlotRangeL[0] <= plotNumber and plotNumber <= ezGalPlotRangeL[1] and velGLonP180CountSum:

            pltNameS = f'ezGal{plotNumber}gLonSpectraCascade.png'
            print('    ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ============')

            plt.clf()

            gLonP180Start = [180, 180, 270,  0,  90][gQuadrant]
            gLonP180Stop  = [540, 270, 360, 90, 180][gQuadrant]
            gLonP180Qty   = [360,  90,  90, 90,  90][gQuadrant]
            yMax          = [179,  89, 179, -91, -1][gQuadrant]

            # https://stackoverflow.com/questions/29883344/how-can-i-make-waterfall-plots-in-matplotlib-and-python-2-7
            # https://stackoverflow.com/questions/4804005/matplotlib-figure-facecolor-background-color

            #import numpy as np
            #import matplotlib.pyplot as plt

            #######################fig = plt.figure(facecolor='k')
            fig = plt.figure()
            #ax = fig.add_subplot(111, axisbg='k')
            # "The axisbg and axis_bgcolor properties on Axes have been deprecated in favor of facecolor"
            ax = fig.add_subplot(111)
            
            #def fG(x, x0, sigma, A):
            #    """ A simple (un-normalized) Gaussian shape with amplitude A. """
            #    return A * np.exp(-((x-x0)/sigma)**2)

            # Draw ny lines with ng Gaussians each, on an x-axis with nx points
            #nx, ny, ng = 1000, 20, 4
            #ny = 90
            #x = np.linspace(0,1,1000)
            #x = np.linspace(0,1,256)

            gain = ezGal61XGain / velGLonP180Max

            #y = np.zeros((ny, nx))
            #for iy in reversed(range(ny)):
            #for iy in range(gLonP180Start, gLonP180Stop):
            for iy in range(0, gLonP180Qty):
                #print(' iy =', iy)
                #for ig in range(ng):
                #    # Select the amplitude and position of the Gaussians randomly
                #    x0 = np.random.random()
                #    A = np.random.random()*10
                #    sigma = 0.05
                #    y[iy,:] += fG(x, x0, sigma, A)

                # Offset each line by this amount: we want the first lines plotted
                # at the top of the chart and to work our way down
                #offset = (ny-iy)*5
                #print(' gLonP180Stop =', gLonP180Stop)
                offset = gLonP180Stop - iy          # descends from gLonP180Stop down to gLonP180Start
                #print(' offset =', offset)
                # Plot the line and fill under it: increase the z-order each time
                # so that lower lines and their fills are plotted over higher ones
                #ax.plot(x,y[iy]+offset, 'w', lw=2, zorder=(iy+1)*2)
                # ax.plot(-byFreqBinX, velGLonP180[:, gLonP180], linewidth=0.5)
                #print(' gQuadrant =', gQuadrant)
                #if gQuadrant <= 2:
                #    # gQuadrant 1 and 2
                #    #y = velGLonP180[:,gLonP180Stop-iy] * gain + gLonP180Start + offset - gain - 361.
                #    y = velGLonP180[:,offset] * gain - gain + offset - 181.
                #else:
                #    # gQuadrant 3 and 4
                #    #y = velGLonP180[:,gLonP180Stop-iy] * gain + gLonP180Start + offset - gain + 179.
                #    y = velGLonP180[:,offset] * gain - gain + offset - 181.

                ##if offset < 360:
                ##    y = velGLonP180[:,offset] * gain - gain + offset - 181.
                ##else:
                ##    y = velGLonP180[:,offset-360] * gain - gain + offset - 181.

                if gQuadrant:
                    # Galactic quadrants 1 through 4
                    y = velGLonP180[:,offset] * gain - gain + offset - 181.
                else:
                    # Galactic quadrants 0 (all)
                    y = velGLonP180[:,offset-180] * gain - gain + offset - 361.
                #print(' y =', y)

                if 1:
                    # plot unchanging velocity spectra
                    yMax = max(yMax, y.max())
                    #print(' yMax =', yMax)

                    #print(' y =', y)
                    ###################ax.plot(x, y, 'w', zorder=(iy+1)*2, linewidth=0.5)
                    #ax.plot(x, y, 'k', zorder=(iy+1)*2, linewidth=0.5)
                    ax.plot(velocityBin, y, 'k', zorder=(iy+1)*2, linewidth=0.5)
                
                    #ax.fill_between(x, y[iy]+offset, offset, facecolor='k', lw=0, zorder=(iy+1)*2-1)
                    ##############ax.fill_between(x, y, offset, facecolor='k', lw=0, zorder=(iy+1)*2-1)
                    #ax.fill_between(x, y, y-gain, facecolor='w', lw=0, zorder=(iy+1)*2-1)
                    ax.fill_between(velocityBin, y, y-gain, facecolor='w', lw=0, zorder=(iy+1)*2-1)
                else:
                    # do not plot unchanging velocity spectra
                    yMaxThis = y.max()
                    yMinThis = y.min()
                    #yMax = max(yMax, y.max())
                    yMax = max(yMax, yMaxThis)
                    #print(' yMax =', yMax)

                    if yMinThis < yMaxThis:
                        #print(' y =', y)
                        ###################ax.plot(x, y, 'w', zorder=(iy+1)*2, linewidth=0.5)
                        #ax.plot(x, y, 'k', zorder=(iy+1)*2, linewidth=0.5)
                        ax.plot(velocityBin, y, 'k', zorder=(iy+1)*2, linewidth=0.5)
                    
                        #ax.fill_between(x, y[iy]+offset, offset, facecolor='k', lw=0, zorder=(iy+1)*2-1)
                        ##############ax.fill_between(x, y, offset, facecolor='k', lw=0, zorder=(iy+1)*2-1)
                        #ax.fill_between(x, y, y-gain, facecolor='w', lw=0, zorder=(iy+1)*2-1)
                        ax.fill_between(velocityBin, y, y-gain, facecolor='w', lw=0, zorder=(iy+1)*2-1)

            plt.title(titleS)

            plt.xlabel('Velocity (km/s)')
            #velocitySpanMax = +dopplerSpanD2 * (299792458. / freqCenter) / 1000.  # = 253.273324388 km/s
            plt.xlim(-velocitySpanMax, velocitySpanMax)

            if gQuadrant:
                # Galactic quadrants 1 through 4
                plt.ylabel(f'Galactic Quadrant {gQuadrant}')
                #plt.ylim(gLonP180Start-182, gLonP180Stop-181+gain*velGLonP180Max)
                #iy = 0
                #offset = gLonP180Stop - iy          # descends from gLonP180Stop down to gLonP180Start
                #y = velGLonP180[:,offset] * gain - gain + offset - 181.
                #plt.ylim(gLonP180Start-182, y.max()+2)
                plt.ylim(gLonP180Start-182, yMax+2)
            else:
                # Galactic quadrants 0 (all)
                plt.ylabel('Galactic Longitudes   (-180 thru +179 degrees)')
                #plt.ylim(-182, 181+gain*velGLonP180Max)
                #iy = 0
                #offset = gLonP180Stop - iy          # descends from gLonP180Stop down to gLonP180Start
                #y = velGLonP180[:,offset-180] * gain - gain + offset - 361.
                #plt.ylim(-182, y.max()+2)
                plt.ylim(-186, yMax+6)

            if os.path.exists(pltNameS): # to force plot file date update, if file exists, delete it
                os.remove(pltNameS)
            plt.savefig(pltNameS, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), transparent=True)


    if 0:
        # =================================================
        # stacked broken glass, but transparent

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.collections import PolyCollection
        #import matplotlib.pyplot as plt
        #from matplotlib import colors as mcolors
        #import numpy as np





        fig = plt.figure()
        #ax = fig.gca(projection='3d')
        ax = plt.figure().add_subplot(projection='3d')


        xs = np.arange(0, 10, 0.4)
        verts = []
        zs = np.arange(0, 5, 0.2)
        zs = np.arange(0, 5)
        for z in zs:
            r=[int(np.random.normal(5,5)) for i in range(0,10000)]
            ys = np.histogram(r,len(xs))[0]/10000
            print(' ys =', ys)
            print(' ys.shape = ', ys.shape)

            ys[0], ys[-1] = 0, 0
            verts.append(list(zip(xs, ys)))

        poly = PolyCollection(verts,facecolor='white')
        poly.set_edgecolor('black')






        poly.set_alpha(0.7)
        ax.add_collection3d(poly, zs=zs, zdir='y')

        ax.set_xlabel('X')
        ax.set_xlim3d(0, 10)
        ax.set_ylabel('Y')
        ax.set_ylim3d(-1, 4)
        ax.set_zlabel('Z')
        ax.set_zlim3d(0, 1)

        #plt.show()


    if 0:
        if 0:
            xs = np.arange(0, 10, 0.4)
            verts = []
            zs = np.arange(0, 5, 0.2)
            for z in zs:
                r=[int(np.random.normal(5,5)) for i in range(0,10000)]
                ys = np.histogram(r,len(xs))[0]/10000
                ys[0], ys[-1] = 0, 0
                verts.append(list(zip(xs, ys)))

            poly = PolyCollection(verts,facecolor='white')
            poly.set_edgecolor('black')


        if os.path.exists(pltNameS): # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')


        #fig, axs = plt.subplots(6, 10, figsize=(10, 6), layout='constrained')
        fig, axs = plt.subplots(9, 10, figsize=(10, 6), layout='constrained')
        #fig, axs = plt.subplots(6, 10, layout='constrained')
        #print(' axs.flat[0:5] =', axs.flat[0:5])
        #for ax in zip(axs.flat, cases):
        axsFlat = axs.flat

        #plt.title(titleS, transform=plt.transPlot)
        #fig.suptitle('Google (GOOG) daily closing price')
        fig.suptitle(titleS, fontsize=12)

        #plt.ylabel('Average AntXTVT Spectra for Galaxy plane at' \
        #    + f'\n\nGalactic Longitudes of Galactic Quadrant {gQuadrant}', \
        #    rotation=90, verticalalignment='bottom')
        #fig.suptitle(titleS, fontsize=12, rotation=90))
        #fig.suptitle(titleS, fontsize=12, rotation='vertical')
        fig.suptitle(titleS + f'\nAverage {antXTVTName} Spectra for Galaxy plane at' \
            + f' Galactic Longitudes (Galactic Quadrant {gQuadrant})', fontsize=12)

        gLonP180Start = [-1, 180, 270, 0, 90][gQuadrant]

        # 0 through 90 in this quadrant
        for i in range(90):

            gLonP180 = gLonP180Start + i
            #print(' gLonP180 =', gLonP180)

            #print(' i =', i)
            #ax = axs.flat[i]
            ax = axsFlat[i]

            if velGLonP180Count[gLonP180]:
                #gLonP180 = velGLonP180CountNonzeroIndex[0][gLonP180]

                #ax.clear()

                #ax.set_title(f'markevery={markevery}')
                #ax.set_title(f'mark')
                #ax.set_title(f'mark{velGLonP180CountNonzeroIndex[0][i]}')
                #ax.set_title(f'gLon={velGLonP180CountNonzeroIndex[0][gLonP180]-180}')

                #ax.plot(x, y, 'o', ls='-', ms=4, markevery=markevery)
                #ax.plot(x, y, 'o', ls='-', ms=4, markevery=0.1)
                ax.plot(-byFreqBinX, velGLonP180[:, gLonP180], linewidth=0.5)
        
                ax.grid(1)
        
                #ax.text(fontsize=10)
                    
                #ax.set_xlim(-dopplerSpanD2, dopplerSpanD2)
                ax.set_xlim(-velocitySpanMax, velocitySpanMax)
        
                ax.set_ylim(yLimMin, yLimMax)

                ax.tick_params('both',labelsize=5) 

            #else:
                #ax.clear()
                #ax.set_xticks([], [])
                #ax.set_yticks([], [])

            ax.set_xticks([], [])
            ax.set_yticks([], [])
            ax.axvline(linewidth=0.5, color='b')

            #ax.set_title(f'gLongitude {gLonDegS}', fontsize=5)
            #ax.text(0.1, 0.9, 'gLon', fontsize=5)
            #ax.text(0.8, 0.8, gLonDegS, fontsize=5)
            #ax.text(0.01, 0.8, 'gLon', fontsize=5, transform=ax.transAxes)
            ax.text(0.02, 0.85, 'gLon', fontsize=5, transform=ax.transAxes)

            # add text with form of '+nnn' or '-nnn' degrees
            #ax.text(0.03, 0.85, 'gLon', fontsize=5, transform=ax.transAxes)
            #ax.text(0.8, 0.8, gLonDegS, fontsize=5, transform=ax.transAxes)
            #ax.text(0.8, 0.8, '-004', fontsize=5, transform=ax.transAxes)
            #ax.text(0.8, 0.8, gLonDegS, fontsize=5, transform=ax.transAxes)
            #ax.text(0.8, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes)
            if gLonP180 < 180:
                gLonDegS = f'-{180 - gLonP180:03d}'        # '-nnn' with leading zeros
                #ax.text(0.8, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes)
            else:
                gLonDegS = f'+{gLonP180 - 180:03d}'        # '+nnn' with leading zeros
                #ax.text(0.76, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes, horizontalalignment='right')
                #ax.text(0.99, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes, horizontalalignment='right')
            ax.text(0.99, 0.85, gLonDegS, fontsize=5, transform=ax.transAxes, horizontalalignment='right')

        if os.path.exists(pltNameS): # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



    if 0:
        plotCountdown -= 1
        plt.clf()

        # velGLonP180 stores increasing velocity, but X axis is increasing freq, so use -byFreqBinX
        #plt.plot(-byFreqBinX, velGLonP180[:, gLonP180])

        plt.title(titleS)
        plt.grid(ezGalDispGrid)

        #plt.xlabel('Doppler (MHz)')
        #plt.xlim(-dopplerSpanD2, dopplerSpanD2)
        plt.xlabel('Velocity (km/s)')
        velocitySpanMax = +dopplerSpanD2 * (299792458. / freqCenter) / 1000.  # = 253.273324388 km/s
        plt.xlim(-velocitySpanMax, velocitySpanMax)

        if 0:
            # new ylim for each ezGal690gLonDegP180_nnnByFreqBinAvg plot
            yLimMin = 0.95 * velGLonP180[:, gLonP180].min()
            print(' yLimMin =', yLimMin)

            yLimMax = 1.05 * velGLonP180[:, gLonP180].max()
            print(' yLimMax =', yLimMax)

        plt.ylim(yLimMin, yLimMax)

        # create gLonDegS with form of '+nnn' or '-nnn' degrees
        if gLonP180 < 180:
            gLonDegS = f'-{180 - gLonP180:03d}'        # '-nnn' with leading zeros
        else:
            gLonDegS = f'+{gLonP180 - 180:03d}'        # '+nnn' with leading zeros

        plt.ylabel(f'Average {antXTVTName} Spectrum for Galaxy plane at' \
            + f'\n\nGalactic Longitude = {gLonDegS} degrees', \
            rotation=90, verticalalignment='bottom')

        if os.path.exists(pltNameS): # to force plot file date update, if file exists, delete it
            os.remove(pltNameS)
        plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def plotEzGal690gLonDegP180_nnnByFreqBinAvg():

    global velGLonP180              # float 2d array
    global velGLonP180Count         # integer array
    global velGLonP180CountSum      # integer
    global antXTVTName              # string

    #global fileFreqBinQty           # integer
    #global freqCenter               # float
    #global dopplerSpanD2            # float

    global velocitySpanMax          # float
    global velocityBin              # float array

    global plotCountdown            # integer
    global elevation                # float array
    global titleS                   # string
    global ezGalDispGrid            # integer
    #global byFreqBinX               # float array
    global ezGalPlotRangeL          # integer list

    # if anything in velGLonP180 to plot
    if ezGalPlotRangeL[0] <= 690 and 690 <= ezGalPlotRangeL[1] and velGLonP180CountSum:
        velGLonP180CountNonzero = np.count_nonzero(velGLonP180Count)
        print()
        print(' velGLonP180CountNonzero =', velGLonP180CountNonzero, 'of', len(velGLonP180Count) )
        #plotCountdown += np.count_nonzero(velGLonP180Count)
        plotCountdown = velGLonP180CountNonzero

        if 1:
            # same ylim for all ezGal690gLonDegP180_nnnByFreqBinAvg plots
            yLimMin = 0.95 * velGLonP180.min()
            print(' yLimMin =', yLimMin)

            yLimMax = 1.05 * velGLonP180.max()
            print(' yLimMax =', yLimMax)

        for gLonP180 in range(361):                 # for every column, RtoL
            if velGLonP180Count[gLonP180]:      # if column used

                # create pltNameS with form of 'ezGal690gLonDegP180_nnnByFreqBinAvg.png'
                pltNameS = f'ezGal690gLonDegP180_{gLonP180:03d}ByFreqBinAvg.png'
                print()
                print('    ' + str(plotCountdown) + ' plotting ' + pltNameS + ' ============')
                print(' gLonP180 =', gLonP180)
                print(' gLonP180 - 180 =', gLonP180 - 180)
                print(' velGLonP180Count[gLonP180] =', velGLonP180Count[gLonP180])
                plotCountdown -= 1
                plt.clf()

                # velGLonP180 stores increasing velocity
                plt.plot(velocityBin, velGLonP180[:, gLonP180])

                plt.title(titleS)
                plt.grid(ezGalDispGrid)

                #plt.xlabel('Doppler (MHz)')
                #plt.xlim(-dopplerSpanD2, dopplerSpanD2)
                plt.xlabel('Velocity (km/s)')
                plt.xlim(-velocitySpanMax, velocitySpanMax)

                if 0:
                    # new ylim for each ezGal690gLonDegP180_nnnByFreqBinAvg plot
                    yLimMin = 0.95 * velGLonP180[:, gLonP180].min()
                    print(' yLimMin =', yLimMin)

                    yLimMax = 1.05 * velGLonP180[:, gLonP180].max()
                    print(' yLimMax =', yLimMax)

                plt.ylim(yLimMin, yLimMax)

                # create gLonDegS with form of '+nnn' or '-nnn' degrees
                if gLonP180 < 180:
                    gLonDegS = f'-{180 - gLonP180:03d}'        # '-nnn' with leading zeros
                else:
                    gLonDegS = f'+{gLonP180 - 180:03d}'        # '+nnn' with leading zeros

                plt.ylabel(f'{antXTVTName} Average Velocity Spectrum' \
                    + f'\n\nfor Galaxy plane at Galactic Longitude = {gLonDegS} deg', \
                    rotation=90, verticalalignment='bottom')

                if os.path.exists(pltNameS): # to force plot file date update, if file exists, delete it
                    os.remove(pltNameS)
                plt.savefig(pltNameS, dpi=300, bbox_inches='tight')



def printGoodbye(startTime):

    global programRevision          # string
    global commandString            # string

    # print status
    if 0:
        print()
        print('   ezRAObsName      =', ezRAObsName)
        if 0:
            print('   ezGalUseSamplesRawL      =', ezGalUseSamplesRawL)
            print('   ezGalAddAzDeg            =', ezGalAddAzDeg)
            print('   ezGalAddElDeg            =', ezGalAddElDeg)

            print('   ezGalHideFreqBinL        =', ezGalHideFreqBinL)
            print('   ezGalRfiLim              =', ezGalRfiLim)
            print('   ezGalUseSamplesAntL      =', ezGalUseSamplesAntL)
            print('   ezGalDispGrid            =', ezGalDispGrid)
            print('   ezGalDispFreqBin         =', ezGalDispFreqBin)
            #print('   ezGalDetectLevel         =', ezGalDetectLevel)

    stopTime = time.time()
    stopTimeS = time.ctime()
    print()
    print(' That Python command')
    print('  ', commandString)
    print(' took %d seconds = %1.1F minutes' % ((int(stopTime-startTime)),
        (float(int(stopTime-startTime))/60.))) # xxxxxx.x minutes
    print(' Now = %s' % stopTimeS[:-5])

    print()
    print(' programRevision =', programRevision)
    print()
    print()
    print()
    print()
    print()
    print('       The Society of Amateur Radio Astronomers (SARA)')
    print('                    radio-astronomy.org')
    print()
    print()
    print()
    print()
    print()



def main():

    #global programRevision          # string
    #global commandString            # string
    #global cmdDirectoryS            # string

    #global fileFreqMin              # float
    #global fileFreqMax              # float
    #global fileFreqBinQty           # integer

    #global fileNameLast             # string
    ##global fileWriteName            # string
    #global fileWrite                # file handle

    #global freqCenter               # float
    #global freqStep                 # float
    #global dopplerSpanD2            # float
    #global titleS                   # string
    #global plotCountdown            # integer
    #global ezGalDispGrid            # integer

    #global ezGalPlotRangeL          # integer list


    startTime = time.time()

    printHello()
    
    ezGalArguments()

    readDataDir()   # creates fileFreqMin, fileFreqMax, fileFreqBinQty, 
                    #   velGLonP180, velGLonP180Count, galDecP90GLonP180Count,
                    #   galDecP90GLonP180Count, fileNameLast

    plotPrep()      # creates titleS, velocitySpanMax, velocityBin

    # velocity plots
    plotEzGal510velGLon()
    plotEzGal511velGLonCount()          # creates ezGal511velGLonCount.txt
    ################plotEzGal516velGLonAvg()            # spectrum Averages
    ################plotEzGal517velGLonMax()            # spectrum Maximums
    ################plotEzGal518velGLonMin()            # spectrum Minimums

    plotEzGal520velGLonPolar()
    plotEzGal521velGLonPolarCount()

    plotEzGal530galDecGLon()

    findVelGLonEdges()
    plotEzGal540velGLonEdgesB()
    plotEzGal541velGLonEdges()
    plotEzGal550galRot()
    #plotEzGal551galRot2()
    plotEzGal560galMass()

    plotEzGal60XgLonSpectra()
    plotEzGal61XgLonSpectraCascade()

    plotEzGal690gLonDegP180_nnnByFreqBinAvg()

    printGoodbye(startTime)



if __name__== '__main__':
  main()

