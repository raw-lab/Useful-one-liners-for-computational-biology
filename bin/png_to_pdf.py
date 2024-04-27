#!/usr/bin/env/python3

#python png_to_pdf.py input.png output.pdf --resolution 600

import argparse
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def png_to_pdf(input_png, output_pdf, resolution=300):
    # Open the PNG image
    img = Image.open(input_png)

    # Set the desired resolution
    img_info = img.info
    img_info['dpi'] = (resolution, resolution)

    # Create a PDF file
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    
    # Set the page size based on the PNG image size
    pdf.setPageSize((img.width, img.height))

    # Draw the PNG image on the PDF canvas
    pdf.drawInlineImage(img, 0, 0, img.width, img.height)

    # Save the PDF file
    pdf.save()

def main():
    parser = argparse.ArgumentParser(description='Convert PNG to high-resolution PDF')
    parser.add_argument('input_png', help='Input PNG file path')
    parser.add_argument('output_pdf', help='Output PDF file path')
    parser.add_argument('--resolution', type=int, default=300, help='Resolution for the PDF (default: 300 dpi)')

    args = parser.parse_args()

    png_to_pdf(args.input_png, args.output_pdf, args.resolution)
    print(f'Conversion completed. PDF saved to {args.output_pdf}')

if __name__ == "__main__":
    main()
