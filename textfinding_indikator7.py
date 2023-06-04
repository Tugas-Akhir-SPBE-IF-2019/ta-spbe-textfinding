# this code is for TEXT FINDING - INDIKATOR 7
# input is txt file from preprocess dokumen lama, nama instansi & judul from dokumen lama & baru

import re
import preprocess_dokbaru as dokbaru
import preprocess_doklama as doklama
from utility import *


def txtreader(filename, lv, keyword):
    # func to search keyword in txt file

    # open txt file
    file = open(f'cleaned_{filename}.txt', 'r')

    idx = 0
    result = []
    initial_keys = list(keyword)

    # read line by line from txt
    for line in file:

        if (lv == 2):
            # check using 
            for key in initial_keys:
                if (key in keyword):
                    reg = f'{key}'
                    if re.search(reg, line, re.IGNORECASE):
                        result.append([idx, line])
                        keyword.remove(key)
        
        # lv 3 and 4 have the same logic to check for found text
        elif (lv == 3 or lv == 4):
            # check using main keyword first
            reg = f'(?:(sistem)\s*(penghubung)\s*(layanan))'
            if (re.search(reg, line, re.IGNORECASE)):
                for key in initial_keys:
                    if (key in keyword):
                        if re.search(key, line, re.IGNORECASE):
                            result.append([idx, line])
                            keyword.remove(key)

        idx += 1

    file.close()
    return (result)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])


# for indicator 7, ceklvl will only check against lvl2 keywords only
# because the rest are related to lvl2 and will be checked in the next step (text similarity)
def ceklvl(filename):
    list_final = []
    text_final = ''

    lvl2 = convert_keywords(['sistem penghubung layanan'])
    res2 = txtreader(filename, 2, lvl2)

    # check if keyword lvl2 is not found, then return as empty string
    if (not res2):
        return text_final

    for el in res2:
        list_final.append(el[1])
    
    lvl3 = convert_keywords([
        'seluruh opd', 
        'setiap opd'
        'seluruh unit kerja', 
        'setiap unit kerja'
        'seluruh pemerintah daerah',
        'setiap pemerintah daerah'])
    res3 = txtreader(filename, 3, lvl3)

    #immediately return if no result is found for lvl3
    if (not res3):
        return clean_text(list_final)

    for el in res3:
        if (el[1] not in list_final):
            list_final.append(el[1])

    lvl4 = convert_keywords(['keterhubungan', 
            'hubung', 
            'integrasi', 
            'berpedoman', 
            'reviu', 
            'diselaraskan', 
            'perubahan'])
    res4 = txtreader(filename, 4, lvl4)

    for el in res4:
        if (el[1] not in list_final):
            list_final.append(el[1])

    text_final = ". ".join(list_final)

    return clean_text(list_final)


filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
# filename = 'PERBUB NO 34 TAHUN 2019 TENTANG RENCANA INDUK SPBE.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)
teks_final = ceklvl(filename)

# hasil text finding
print(teks_final)
print(instansibaru, judulbaru)
print(instansilama, judullama)
