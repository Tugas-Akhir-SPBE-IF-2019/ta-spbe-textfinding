import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import re


def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    page_no_title = 0
    page_no_start = 0
    startingPoint = None
    startfound = False
    fulltext = ''

    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        interpreter.process_page(page)
        data = retstr.getvalue()
        retstr.truncate(0)
        # retstr.seek(0)

        # print(page)
        # print(data)
        # print(pageNumber)

        if (startfound == False):
            if (pageNumber == page_no_title):
                # get nama instansi
                instansi = re.split('(?i)peraturan', data)[0]
                # print(instansi)

                # get starting point for judul
                peraturan = re.split('(?i)(peraturan)', data)[1]
                data = re.split('(?i)(peraturan)', data)[2]
                # print(data)

                # get judul
                judul = peraturan + re.split('(?i)(dengan rahmat)', data)[0]
                judul = " ".join(judul.split())
                # print(judul)

            # get starting point for isi dokumen bukti
            startingPoint = re.search('(?i)(bab I)', data)

            # if starting point found in current page
            if (startingPoint != None):
                startfound = True
                page_no_start = pageNumber

                # get isi dokumen bukti
                startingPoint = re.split('(?i)(bab I)', data)[1]
                fulltext += startingPoint + re.split('(?i)(bab I)', data)[2]
        else:
            fulltext += data

    # print(fulltext)

    return (fulltext)

# if __name__ == '__main__':
#     pdfparser(sys.argv[1])


def datacleaner(data, filename):
    codec = 'utf-8'

    # clean whitespace and undefined texts
    data = re.sub(r'\x00+', '\n', data)
    data = re.sub(r'\n{3,}', '\n' * 2, data)
    data = re.sub(r'\n{2,3}', '\n', data)
    data = re.sub(r'(\n\s+)+\n', '\n' * 2, data, flags=re.MULTILINE)

    data = re.sub(r'(\n)+', '', data, flags=re.MULTILINE)

    with open(f'cleaned_{filename}.txt', 'w') as file:
        file.write(data)

    data = re.split(r'(?:[?!\n]|(?<!\d)\.(?!\d))', data)
    # TODO
    # exclude alphabet numbering from split
    # '[.]\s{1}'
    # (?:[?!:;\n]|(?<!\d|(\n[a-z])|(\n[A-Z]))\.(?!\d[0-9]))

    with open(f'cleaned_{filename}2.txt', 'w') as file:
        for el in data:
            print(el)
            print('\n')

            # check if not 'empty' line
            if (re.fullmatch('^(?:\s*(atau|dan)?\s?([0-9]+|[a-z]{1,2}))', el) is None):
                # remove leading whitespace and add newline
                # write line to txt
                file.write(f"{el.lstrip()}\n")

    # datasplitter(filename)


def datasplitter(filename):

    txtfile = open(f'cleaned_{filename}.txt', 'r')
    lines = txtfile.readlines()

    for idx, line in enumerate(lines):
        # print("Line{}: {}".format(idx, line.strip()))

        # line is not judul bab, dll
        if (not line.isupper() and not isnumbering(line)):
            print("Line{}: {}".format(idx, line.strip()))

            pos = re.search('(\.\s[^\S\r\n]*\w)', line)
            # if line contains more than one sentence
            if (pos != None):
                print(lines[idx])
                l = line[:pos.start() + 1]
                r = line[pos.start() + 1:].lstrip()

                print(l)
                print(r)
                lines[idx] = line[:pos.start()]

            # sample_str.endswith('t')


def isnumbering(str):
    res = re.match(('^([0-9]|[a-z]|[A-Z]){1}\.\s*'), str)

    if (res != None):
        return True
    return False


file = 'PERBUB NO 34 TAHUN 2019 TENTANG RENCANA INDUK SPBE.pdf'
file2 = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'

text = pdfparser(file2)
datacleaner(text, file2)
