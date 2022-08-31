This code converts Chirp export file in CSV format to Yaesu's import CSV format. (I only tested this on [FTM-300DR Programming software ADMS-12 (Ver.1.0.0.0) application](https://www.yaesu.com/downloadFile.cfm?FileID=16512&FileCatID=42&FileName=FTM%2D300D%5FADMS%2D12%5FENG.zip&FileContentType=application%2Fx%2Dzip%2Dcompressed))

Use this code at your own discretion. It's not tested on all Yaesu programs.

# HOW

1. Download Chirp and create a station list. 
2. Export this station as a CSV file. (You can name it Chirp-export.csv)
3. Download the chirp2yaesu package from github.com
4. Run it as: python chirp_to_yaesu.py -o Yaesu-import.csv -i Chirp-export.csv
5. Use Yaesu-import.csv file to import the configuration in the Yaesu's own software.

# SCREENSHOTS

Chirp Export

![Chirp Export](http://i.imgur.com/kPHwyOal.png)

# TODO

- So far only Tone and Tone SQL mode are supported, add DTCS, etc...
- Better error handling
 
# SOFAR

- Fixed a problem with enabling Tone SQL mode. (TONE ENC)
- Added basic argument parsing
- Better code commenting
- Add better csv writing
- Added Tone SQL support
- Now retains "holes" in the incoming CSV, retains CSV location numbers
- Will skip any location "0" entries, ie anomolous Chirp CSV export from some radios.
