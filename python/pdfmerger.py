import os
from glob import glob
import PyPDF4 as pdf

def merge(pdf_list):
    writer = pdf.PdfFileWriter()
    for path in pdf_list:
        reader = pdf.PdfFileReader(path)
        writer.addPage(reader.getPage(0))
    return writer

def merge_dir(dir, outfile):
    writer = merge(sorted(glob(f'{dir}/*.pdf'), key=os.path.getmtime))
    with open(outfile, 'wb') as out:
        writer.write(out)

if __name__ == '__main__':
    import sys
    merge_dir(sys.argv[1], sys.argv[2])

