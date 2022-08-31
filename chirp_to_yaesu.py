#!/usr/bin/env python

# Updated for FTM-300D ADMS-12 Version 1.0.0.0

import csv
import argparse

def addEmptyLine(foo, lineNumber):
    templine = str(lineNumber) + ",,,,,,,,,,,,,,,,,,,,,0"
    foo.append(templine.split(","))
    return foo

# Adding the command line flags
parser = argparse.ArgumentParser(description="This tool converts a chirp csv file to a Yaesu importable csv file.")
parser.add_argument('--input', '-i', required = True)
parser.add_argument('--output', '-o', default="Yaesu-import.csv")
parser.add_argument('--band', '-b', default='A', choices = ['A', 'B'], help='Specify the A or B band')
args = parser.parse_args()

ftline = []
chirpFile = []
numlines = 0
inputFile = args.input
outputFile = args.output
if args.band == 'A':
    band = "0"
else :
    band = "1"

# Open the Chirp file and create the Yaesu formatted array
with open(inputFile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #if row["Location"] == "0":  # TD skip bad chirp CSV export defaults
        #    continue
        while numlines  != int(row["Location"]): # TD skip missing lines in input, preserve holes!
            numlines += 1
            chirpFile = addEmptyLine(chirpFile, numlines)
        if row["Tone"] in ("Tone", "TSQL", "DTCS") or (row['Frequency'] != None and row["Tone"] == ''):
            numlines += 1
            ftline.append(str(numlines))                # Channel No
            rxfreq = '%3.5f' % float( row['Frequency'] )# RX Frequency
            ftline.append(rxfreq)
            if row['Offset'] == "OFF":
                ftline.append(rxfreq)
            else :
                freq = float( row['Frequency'] )
                if row['Duplex'] == "-" :
                    freq = freq - float( row['Offset'] )
                elif row['Duplex'] == "+":
                    freq = freq + float( row['Offset'] )
                ftline.append('%3.5f' % freq)           # TX frequency
            #ftline.append('%0.5f' % float(row['Offset']))
            ftline.append('0.00000')                    # Offset frequency (default to 0.00000, TX and RX frequencies have the actual)
            if row['Duplex'] in [ '+', '-' ] :
                ftline.append("-/+") #row['Duplex'] + "RPT")
            else :
                ftline.append( "OFF" )                  # Offset direction
            ftline.append(row['Mode'])                  # Operating Mode
            ftline.append(row['Mode'])                  # DIG/ANALOG
            ftline.append(row['Name'][0:6] + ' ' +row['Comment'].split(',')[0].split('[')[0].strip('"[')[0:9])             # Name (Callsign + First word of comment stripped of ,[" characters)
            if row["Tone"] == "Tone" :                  # Tone Mode
                ftline.append("TONE")
            elif row["Tone"] == "TSQL" :
                ftline.append("TONE SQL")
            elif row["Tone"] == "DTCS" :
                ftline.append("DCS")
            else :
                ftline.append("OFF")
            ftline.append('%.1f' % float(row['rToneFreq']) + " Hz")     # CTCSS Frequency e.g. 100.0 Hz
            ftline.append(row['DtcsCode'])              # DCS Code
            ftline.append("1500 Hz")                    # User CTCSS
            ftline.append("RX 00")                      # RX DG-ID
            ftline.append("TX 00")                      # TX DG-ID
            ftline.append("LOW")                        # Tx Power, Default to Low
            ftline.append("OFF")                        # M-GRP
            ftline.append("NO")                         # Scan, default to No. Modify in ADMS
            ftline.append("12.5KHz")                    # Step
            if row['Mode'] == "NFM":                    # Narrow (ON/OFF)
                ftline.append("ON")
            else :
                ftline.append("OFF")
            ftline.append("OFF")                        # Clock shift (ON/OFF)
            ftline.append(row['Comment'])               # Comment
            ftline.append("0")                          # Add mysterious 0 at end

            chirpFile.append(ftline)
            ftline = []
        else:
            # Unhandled Tones, Don't do anything now, just add an empty line
            # This will have to handle DCS stuff one day.
            numlines += 1
            chirpFile = addEmptyLine(chirpFile, numlines)

# For some reason Yaesu import CSV file expects 1000 lines,
# filling the rest with empty lines here

for line in range(numlines+1, 1000):
    chirpFile = addEmptyLine(chirpFile, line)

# Writing the file to Yaesu importable CSV file.
with open(outputFile, "wb") as csvWriter:
    writer = csv.writer(csvWriter, delimiter=",")
    for line in chirpFile:
        writer.writerow(line)
