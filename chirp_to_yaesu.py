#!/usr/bin/env python

import csv
import argparse

def addEmptyLine(foo, lineNumber):
    templine = str(lineNumber) + ",,,,,,,,,,,,,,0,,0"
    foo.append(templine.split(","))
    return foo

# Adding the command line flags
parser = argparse.ArgumentParser(description="This tool converts a chirp csv file to a Yaesu importable csv file.")
parser.add_argument('--input', '-i', required = True)
parser.add_argument('--output', '-o', default="Yaesu-import.csv")
args = parser.parse_args()

ftline = []
chirpFile = []
numlines = 0
inputFile = args.input
outputFile = args.output

# Open the Chirp file and create the Yaesu formatted array
with open(inputFile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Tone"] == "Tone":
            numlines += 1
            ftline.append(str(numlines))
            ftline.append(row['Frequency'])
            ftline.append('')
            ftline.append(row['Offset'])
            ftline.append(row['Duplex'] + "RPT")
            ftline.append(row['Mode'])
            ftline.append(row['Name'])
            ftline.append("TONE ENC")
            ftline.append(row['rToneFreq'] + " Hz")
            ftline.append(row['DtcsCode'])
            ftline.append("1500 Hz")
            ftline.append("HIGH")
            ftline.append("OFF")
            ftline.append("25.0KHz")
            ftline.append("0")
            ftline.append(row['Comment'])
            ftline.append("0")

            chirpFile.append(ftline)
            ftline = []
        else:
            # If it's not Tone, Don't do anything now, just add an empty line
            # This will have to handle DCS stuff one day.
            numlines += 1
            chirpFile = addEmptyLine(chirpFile, numlines)

# For some reason Yaesu import CSV file expects 500 lines,
# filling the rest with empty lines here

for line in range(numlines+1, 501):
    chirpFile = addEmptyLine(chirpFile, line)

# Writing the file to Yaesu importable CSV file.
with open(outputFile, "w") as csvWriter:
    writer = csv.writer(csvWriter, delimiter=",")
    for line in chirpFile:
        writer.writerow(line)
