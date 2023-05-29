# this code is for DOKUMEN BUKTI LAMA
# the code below will get the title

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

    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        interpreter.process_page(page)
        data = retstr.getvalue()
        retstr.truncate(0)
        # retstr.seek(0)

        if (pageNumber == page_no_title):
            # get perihal dokumen
            try:
                perihal = re.split('(?i)perihal', data)
                perihal = perihal[1]
            except Exception as e:
                print("The error is: ", e)
                perihal = ''
            else:
                perihal = stringcleaner(perihal)

            # if perihal is generalized
            if (perihal.lower() in ['undangan', 'notulensi', 'notulen']):
                try:
                    perihal = re.split('(?i)keperluan', data)
                    perihal = perihal[1]
                except Exception as e:
                    print("The error is: ", e)
                    perihal = ''
                else:
                    perihal = stringcleaner(perihal)

        break

    return (perihal)


def stringcleaner(data):
    codec = 'utf-8'

    # clean leading whitespace
    data = re.split('\n+', data)[1]
    print(data)

    # split on new line
    data = re.split('\n+', data)[0]

    return data.strip()


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])

filename = 'Nota Dinas.pdf'
filename2 = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
filename3 = 'karawang.pdf'
filename4 = 'Palangkaraya.pdf'
filename5 = 'salatiga.pdf'
filename6 = 'TANGGAMUS.pdf'

perihal = pdfparser(filename4)
print(perihal)
