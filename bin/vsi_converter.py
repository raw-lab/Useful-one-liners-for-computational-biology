#!/usr/bin/python3

import argparse
import os
from PIL import Image
import imageio
import numpy 

#Example command line (single file)
#python vsi_converter.py input_file.vsi -o output_file.jpg -f jpeg

#Example command line (many files)
#python vsi_converter.py input_folder -f tif -d

# Define the supported output formats
SUPPORTED_FORMATS = ['jpeg', 'tiff', 'png']

# Parse command line arguments
parser = argparse.ArgumentParser(description='Convert VSI file or folder to JPEG, TIFF, or PNG format.')
parser.add_argument('input', type=str, help='Input VSI file or folder path')
parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Output file path')
parser.add_argument('-f', '--format', type=str, choices=SUPPORTED_FORMATS, default='jpeg', help='Output file format')
parser.add_argument('-d', '--directory', action='store_true', help='Process a whole directory of files while maintaining the original file name')
args = parser.parse_args()

# Check if the input file or folder exists
if not os.path.exists(args.input):
    print(f"Error: Input {args.input} not found.")
    exit(1)

# If input is a file, process it directly
if not args.directory:
    # Set the output file path
    if args.output:
        output_file = args.output.name
    else:
        # If output path is not provided, use the same name as the input file with the chosen output format extension
        output_file = os.path.splitext(args.input)[0] + '.' + args.format

    # Check if the output file already exists
    if os.path.exists(output_file):
        print(f"Error: Output file {output_file} already exists.")
        exit(1)

    # Open VSI file using imageio
    image = imageio.imread(args.input)

    # Convert to PIL Image object
    pil_image = Image.fromarray(image)

    # Save as the chosen output format
    pil_image.save(output_file, format=args.format)

else:
    # If input is a directory, process all files in the directory
    for file_name in os.listdir(args.input):
        # Check if the file is a VSI file
        if file_name.endswith('.vsi') or file_name.endswith('.VSI'):
            # Set the output file path
            output_file = os.path.join(args.input, os.path.splitext(file_name)[0] + '.' + args.format)

            # Check if the output file already exists
            if os.path.exists(output_file):
                print(f"Error: Output file {output_file} already exists.")
                exit(1)

            # Open VSI file using imageio
            with Image.open(os.path.join(args.input, file_name)) as pil_image:

            # Convert PIL image to numpy array
                image = numpy.array(pil_image)

            # Save as the chosen output format
            pil_image.save(output_file, format=args.format)

            print('Conversion complete.')

