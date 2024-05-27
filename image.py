#!/usr/bin/python3

import time
import os
import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import chardet


def dms_to_dd(dms, direction):
    degrees, minutes, seconds = dms
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if direction in ["S", "W"]:
        dd *= -1
    return dd


def GPS_convert(value):
    print("\033[92m[+] GPS Info\033[0m")
    # same in green
    url = "https://maps.google.com/?q={lat},{lng}"
    for key in value:
        if key in [1, 3]:  # Latitude or Longitude Direction
            print(
                f"\t\033[92m[-] {'Latitude' if key == 1 else 'Longitude'} Direction: {value[key]}\033[0m"
            )
        elif key in [2, 4]:  # Latitude or Longitude Ref
            dms = value[key]
            direction = value[key - 1]
            dd = dms_to_dd(dms, direction)
            print(
                f"\t\033[92m[-] {'Latitude' if key == 2 else 'Longitude'} in Decimal Degrees: {dd}\033[0m"
            )
            if key == 2:
                lat = dd
            else:
                lng = dd
    print(f"\t\033[92m[-] Google Maps URL: {url.format(lat=lat, lng=lng)}\033[0m")


# Need to be upgraded (if encoding is not detected)
def detect_encoding(data):
    # print("\033[92m[+] Detecting encoding...\033[0m")
    result = chardet.detect(data)
    encoding = result["encoding"]
    confidence = result["confidence"]
    print(
        f"\033[92m[+] Detected encoding: {encoding} with {confidence*100:.2f}% confidence\033[0m"
    )
    return encoding


def safe_decode(data):
    encoding = detect_encoding(data)
    try:
        return data.decode(encoding)
    except Exception as e:
        return "\033[91mError decoding data\033[0m"


def location(image):
    try:
        img = Image.open(image)
        exif_data = img._getexif()
        if exif_data is not None:
            for tag_id in exif_data:
                tag = TAGS.get(tag_id, tag_id)
                data = exif_data.get(tag_id)
                # Gérer spécifiquement les données binaires ou autres données non-textuelles
                if isinstance(data, bytes):
                    data = safe_decode(data)
                if tag == "GPSInfo":
                    print(data)
                    GPS_convert(data)
                else:
                    print(f"[-] {tag}: {data}")
        else:
            print("Aucune donnée EXIF trouvée.")
    except Exception as e:
        print(f"[-] {e}")


def search_steg(image_path):
    # we use strings to search for PGP public key
    os.system(f"strings {image_path} > strings.txt")
    time.sleep(1)  # wait for the file to be created (not the best way to do it)
    # the best way is to check if the file exists
    with open("strings.txt", "r") as f:
        for line in f:
            if "-----BEGIN PGP PUBLIC KEY BLOCK-----" in line:
                print("\033[92m[+] PGP PUBLIC KEY found\033[0m")
                print(line)
                for line in f:
                    #print line but don't jump a line after each print
                    print(line, end="")
                    if "-----END PGP PUBLIC KEY BLOCK-----" in line:
                        break
                break
            else:
                print(line)
        else:
            print("\033[91m[-] PGP PUBLIC KEY not found\033[0m")


def main():

    parser = argparse.ArgumentParser(description="Image Investigation Tool")
    parser.add_argument(
        "-map",
        "--map",
        metavar="",
        type=str,
        help="Search where the image was taken",
    )
    parser.add_argument(
        "-steg", "--steg", metavar="", type=str, help="Search for PGP PUBLIC KEY"
    )

    # Gestion manuelle de l'option d'aide
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Logique de traitement des arguments ici
    if args.map:
        location(args.map)
    elif args.steg:
        search_steg(args.steg)


if __name__ == "__main__":
    main()
