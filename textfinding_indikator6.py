# this code is for TEXT FINDING - INDIKATOR 6
# input is txt file from preprocess dokumen lama, nama instansi & judul from dokumen lama & baru

import re
import preprocess_dokbaru as dokbaru
import preprocess_doklama as doklama
from utility import *

def txtreader(filename, lv, keyword):

    file = open(f'cleaned_{filename}.txt', 'r')

    idx = 0
    result = []

    for line in file:

        if (lv == 1):
            reg1 = f'(?:\s?(jaringan intra))'
            reg2 = f'(?:\s?(jaringan lokal))'

            if (re.search(reg1, line.lower(), re.IGNORECASE) or re.search(reg2, line.lower(), re.IGNORECASE)):
                result.append([idx, line])

        if (lv == 2 or lv == 3):
            reg1 = f'(?:\s?(jaringan intra))'
            reg2 = f'(?:\s?(jaringan lokal))'

            if (re.search(reg1, line.lower(), re.IGNORECASE) or re.search(reg2, line.lower(), re.IGNORECASE)):
                for key in keyword:
                    if re.search(key, line.lower(), re.IGNORECASE):
                        result.append([idx, line])

        else:
            reg1 = f'(?:\s?(jaringan intra))'
            reg2 = f'(?:\s?(jaringan lokal))'

            if (re.search(reg1, line.lower(), re.IGNORECASE) or re.search(reg2, line.lower(), re.IGNORECASE)):
                res = [ele for ele in keyword if (ele in line)]
                if (res):
                    result.append([idx, line])

        idx += 1

    file.close()
    return (result)

def ceklvl(filename):
    list_final = []

    lvl1 = []
    res1 = txtreader(filename, 1, lvl1)

    if (not res1):
        return ''

    lvl2 = convert_keywords([
        'organisasi perangkat daerah', 
        'opd', 
        'unit kerja', 
        'pemerintah daerah', 
        'perangkat daerah'])
    res2 = txtreader(filename, 2, lvl2)

    for el in res2:
        if (el[1] not in list_final):
            list_final.append(el[1])
    
    lvl3 = convert_keywords(['setiap opd', 
           'seluruh opd', 
           'setiap unit kerja', 
           'seluruh unit kerja', 
           'setiap pemerintah daerah',
           'seluruh pemerintah daerah',
           'seluruh Perangkat Daerah'])
    res3 = txtreader(filename, 3, lvl3)

    if (not res3):
        return clean_text(list_final)

    for el in res3:
        if (el[1] not in list_final):
            list_final.append(el[1])

    lvl4 = convert_keywords(['hubung', 
            'sambung',
            'integrasi', 
            'berpedoman', 
            'reviu', 
            'diselaraskan', 
            'perubahan', 
            'interkoneksi', 
            'periodik'])
    res4 = txtreader(filename, 4, lvl4)

    for el in res4:
        if (el[1] not in list_final):
            list_final.append(el[1])

    return clean_text(list_final)

filename = 'PhakPhakBarat.pdf'
# filename = 'BatuBara.pdf'
# filename = 'lamongan.pdf'
# filename = 'lamongan-dokumen-lama.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)

teks_final = ceklvl(filename)

# hasil text finding
print("\nTeks:\n", teks_final, "\n")
# print("\nInstansi Baru:\n", instansibaru, "\n")
# print("\nJudul Baru:\n", judulbaru, "\n")
# print("\nInstansi Lama:\n", instansilama, "\n")
# print("\nJudul Lama:\n", judullama, "\n")
