# Image Investigation Tool

This Python script provides a versatile tool for image analysis, focusing on extracting GPS data from images and searching for embedded PGP public keys within image files. It leverages the PIL library to handle images and extract EXIF metadata, including GPS information, and uses basic OS operations to search for text patterns indicative of PGP keys.

## Features

- **GPS Data Extraction**: Extract and display GPS coordinates embedded in the image's EXIF metadata. It converts the coordinates to decimal degrees and generates a Google Maps URL for easy location viewing.
- **PGP Public Key Search**: Search for PGP public keys embedded within the image file by scanning the text output of the `strings` command.

## Requirements

- Python 3
- PIL (Pillow)
- chardet

## Installation

Ensure you have Python 3 installed on your system. Then, install the required Python packages:

```bash
pip install Pillow chardet
```

## Usage

The tool provides two main functionalities: extracting GPS data and searching for PGP public keys.

### Extracting GPS Data

To extract GPS data from an image and convert it to a readable format, use:
```bash
$> python3 image.py -map image.jpeg
GPS Info:
#Latitude: 37.774929
#Longitude: -122.419416
#Google Maps URL: https://www.google.com/maps/place/37.774929,-122.419416
```
This command prints the latitude and longitude in both DMS (Degrees, Minutes, Seconds) and decimal degrees format, along with a direct Google Maps URL.

### Searching for PGP Public Keys

To search for PGP public keys within an image file, use:
```bash
$> python3 image.py -steg image.jpeg
#-----BEGIN PGP PUBLIC KEY BLOCK-----
#Version: 01
#
#lorem ipsum dolor sit amet, consectetur adipiscing elit.
#
#-----END PGP PUBLIC KEY BLOCK-----
```
If a PGP public key block is found, it is printed to the console.

