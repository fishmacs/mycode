import os
import tempfile
from glob import glob
from PIL import Image
import PyPDF4 as pdf

separator_height = 40

def merge(img_list):
    w = max([img.width for img in img_list])
    h = sum([img.height for img in img_list])
    h += separator_height * (len(img_list) - 1)
    dst = Image.new('RGB', (w, h), 'WHITE')
    last = img_list[0]
    dst.paste(last, (0, 0))
    for img in img_list[1:]:
        dst.paste(img, (0, last.height + separator_height))
    return dst

def merge_dir(dir, ext, outfile):
    img_list = [Image.open(f) for f in glob(f'{dir}/*.{ext}')]
    dst = merge(img_list)
    dst.save(outfile)

def img_to_pdf(filename):
    img = Image.open(filename)
    name = f'{os.path.splitext(filename)[0]}.pdf'
    img.save(name)

def convert_dir(dir, outfile, extnames, resize=False, reverse=False):
    files = glob(f'{dir}/*.' + extnames[0])
    for ext in extnames[1:]:
        files.extend(glob(f'{dir}/*.' + ext))
    files.sort(reverse=reverse)
    writer = pdf.PdfFileWriter()
    for f in files:
        if f.endswith('.pdf'):
            reader = pdf.PdfFileReader(f)
        else:
            img = Image.open(f)
            if resize:
                img = resize_first_page(img)
            with tempfile.NamedTemporaryFile('wb', suffix='.pdf') as tmpfile:
                img.save(tmpfile.name)
                reader = pdf.PdfFileReader(tmpfile.name)
        writer.addPage(reader.getPage(0))
    with open(outfile, 'wb') as out:
        writer.write(out)

def resize_first_page(img):
    w, h = img.size
    if w < 1000:
        # img = img.crop((0, 500, w, h - 500))
        img = img.resize((1280, 1802), Image.ANTIALIAS)
        # print(w, h, img.size)
    if img.mode == 'RGBA':
        rgb = Image.new('RGB', img.size, (255, 255, 255))
        rgb.paste(img, mask=img.split()[3])
        img = rgb
    return img


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('-r', '--reverse', type=int)
    parser.add_argument('-e', '--extname', type=str)
    parser.add_argument('-s', '--resize', type=int)
    args = parser.parse_args()
    extnames = ['jpg']
    extname = args.extname or ''
    if 'n' in extname:
        extnames.append('png')
    if 'p' in extname:
        extnames.append('pdf')
    resize = args.resize and True or False
    reverse = args.reverse and True or False
    # ext = sys.argv[3] or 'jpg' if len(sys.argv)>3 else 'jpg'
    # merge_dir(sys.argv[1], ext, sys.argv[2])
    convert_dir(args.input, args.output, extnames, resize, reverse)
