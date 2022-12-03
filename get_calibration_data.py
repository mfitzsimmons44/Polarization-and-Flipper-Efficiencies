#
# get_calibration_data.py
# version 1
#
# Code to read in ROI and background data intended for calculating efficiencies
# of the polarizers and flippers.
# 
# The data are expected in 8 files: 4 of ROI data and 4 of background.
# The data should already have been normalized to constant exposure and integrate
# over the same number of pixels.
#
# The data format is: wavelength, time of flight, signal and standard deviation on signal.
# The prefaces of the 4 files of each type are expected to be the same and all are expected
# to end with "On_On.txt" etc.
# This routine removes the background data.
#
import math
import getopt
import sys
import numpy as np
import os

DefaultDir=os.getcwd() + r'/'

# usage() is a way to communicate to an unknowing victim what arguments are expected--namely this routine allows 
# access to any named file and output file name.  the first file is the background, the second the data, the output
# is the net.
#
def usage():
	print("Options:\n \t--help \n \t--back=BACKFILE \n \t--input=INPUTFILE \n \t--output=OUTPUTFILE")
	print("	Example:")
	print(" net_data.py --back=BackFileofData --input=FileNameofInputData --output=FileNameofOutputData")
	print("    Note: The default read directory is %s"%(DefaultDir))
	print("    Note: The suffix On_On.txt and so forth will be appended by the code; do not include.")
	print("    Note: The prefixes of each file type, back or ROI, are the same to the file type.")
	print("    Note: The files are assumed to have the same number of rows, wavelengths and tofs.")
	
def main():
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "back=", "input=", "output="])
	except getopt.GetoptError as err:
		print(str(err))  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	OutputFile = None
	BackFile = None
	InputFile = None

	verbose = False
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-i", "--back"):
			BackFile = a
		elif o in ("-i", "--input"):
			InputFile = a
		elif o in ("-o", "--output"):
			OutputFile = a
		else:
			assert False, "unhandled option"

	if BackFile == None:
		usage()
		sys.exit()
	else:
		print(DefaultDir+BackFile+"On_On.txt")
		file = open(DefaultDir+BackFile+"On_On.txt","r")
		back_data_OnOn = file.readlines()
		file.close
		print(DefaultDir+BackFile+"Off_Off.txt")
		file = open(DefaultDir+BackFile+"Off_Off.txt","r")
		back_data_OffOff = file.readlines()
		file.close
		print(DefaultDir+BackFile+"Off_On.txt")
		file = open(DefaultDir+BackFile+"Off_On.txt","r")
		back_data_OffOn = file.readlines()
		file.close
		print(DefaultDir+BackFile+"On_Off.txt")
		file = open(DefaultDir+BackFile+"On_Off.txt","r")
		back_data_OnOff = file.readlines()
		file.close
	if InputFile == None:
		usage()
		sys.exit()
	else:
		print(DefaultDir+InputFile+"On_On.txt")
		file = open(DefaultDir+InputFile+"On_On.txt","r")
		roi_data_OnOn = file.readlines()
		file.close
		print(DefaultDir+InputFile+"Off_Off.txt")
		file = open(DefaultDir+InputFile+"Off_Off.txt","r")
		roi_data_OffOff = file.readlines()
		file.close
		print(DefaultDir+InputFile+"Off_On.txt")
		file = open(DefaultDir+InputFile+"Off_On.txt","r")
		roi_data_OffOn = file.readlines()
		file.close
		print(DefaultDir+InputFile+"On_Off.txt")
		file = open(DefaultDir+InputFile+"On_Off.txt","r")
		roi_data_OnOff = file.readlines()
		file.close

#
# the assumption not checked! is that the files are equal length
# remove newlines
#
	n = len(back_data_OnOn)
	Lambda = np.zeros(n, dtype=np.float32)
	Tof = np.zeros(n, dtype=np.float32)
	OnOn = np.zeros(n, dtype=np.float32)
	sOnOn =  np.zeros(n, dtype=np.float32)
	OffOff = np.zeros(n, dtype=np.float32)
	sOffOff =  np.zeros(n, dtype=np.float32)
	OffOn = np.zeros(n, dtype=np.float32)
	sOffOn =  np.zeros(n, dtype=np.float32)
	OnOff = np.zeros(n, dtype=np.float32)
	sOnOff =  np.zeros(n, dtype=np.float32)
	for i in range(n):
		back_data_OnOn[i]=back_data_OnOn[i].replace('\n','')
		x = back_data_OnOn[i].split()
		roi_data_OnOn[i]=roi_data_OnOn[i].replace('\n','')
		y = roi_data_OnOn[i].split()
		OnOn[i] = float(y[2]) - float(x[2])
		sOnOn[i] = math.sqrt(float(y[3])**2 + float(x[3])**2)
#
		back_data_OffOff[i]=back_data_OffOff[i].replace('\n','')
		x = back_data_OffOff[i].split()
		roi_data_OffOff[i]=roi_data_OffOff[i].replace('\n','')
		y = roi_data_OffOff[i].split()
		OffOff[i] = float(y[2]) - float(x[2])
		sOffOff[i] = math.sqrt(float(y[3])**2 + float(x[3])**2)
#
		back_data_OffOff[i]=back_data_OffOn[i].replace('\n','')
		x = back_data_OffOn[i].split()
		roi_data_OffOn[i]=roi_data_OffOn[i].replace('\n','')
		y = roi_data_OffOn[i].split()
		OffOn[i] = float(y[2]) - float(x[2])
		sOffOn[i] = math.sqrt(float(y[3])**2 + float(x[3])**2)
#
		back_data_OnOff[i]=back_data_OnOff[i].replace('\n','')
		x = back_data_OffOff[i].split()
		roi_data_OnOff[i]=roi_data_OnOff[i].replace('\n','')
		y = roi_data_OnOff[i].split()
		OnOff[i] = float(y[2]) - float(x[2])
		sOnOff[i] = math.sqrt(float(y[3])**2 + float(x[3])**2)
#
		Lambda[i] = float(x[0])
		Tof[i] = float(x[1])
#


	return Lambda,Tof,OnOn,sOnOn,OffOff,sOffOff,OffOn,sOffOn,OnOff,sOnOff

if __name__ == "__main__":
    Lambda, Tof, OnOn, sOnOn, OffOff, sOffOff, OffOn, sOffOn, OnOff, sOnOff = main()
	
