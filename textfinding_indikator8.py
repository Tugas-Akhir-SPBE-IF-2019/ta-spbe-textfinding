# this code is for TEXT FINDING - INDIKATOR 8
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

    #regex for primary word
    reg = f'(?:(manajemen)\s*(keamanan)\s*(informasi))'
    # read line by line from txt
    for line in file:

        if (lv == 1):
            # check using 
            for key in initial_keys:
                if (key in keyword):
                    if re.search(key, line, re.IGNORECASE):
                        result.append([idx, line])
                        keyword.remove(key)

        elif (lv == 3):
            # Check primary word first:
            if (re.search(reg, line, re.IGNORECASE)):
                for key in initial_keys:
                    if (key in keyword):
                        if (re.search(key, line, re.IGNORECASE)):
                            result.append([idx, line])
                            keyword.remove(key)
        
        else: #lv 4
            # Check primary word first:
            if (re.search(reg, line, re.IGNORECASE)):
                # check if line contains any keyword from list
                for key in initial_keys:
                    if (key in keyword):
                        if (re.search(key, line, re.IGNORECASE)):
                            result.append([idx, line])
                            keyword.remove(key)

        idx += 1

    file.close()
    return (result)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])

def ceklvl(filename):
    list_final = []

    lvl1 = convert_keywords(["manajemen keamanan informasi"])
    res1 = txtreader(filename, 1, lvl1)

    # check if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    # keywords for level 2 and 3 are the same
    lvl2_3 = convert_keywords(['penetapan ruang lingkup', 
              'penetapan penanggung jawab', 
              'perencanaan', 
              'dukungan pengoperasian',
              'evaluasi kinerja',
              'perbaikan berkelanjutan terhadap Keamanan Informasi'])
    res2_3 = txtreader(filename, 3, lvl2_3)

    if not(res2_3):
        list_final.append(res1[0][1])
        return clean_text(list_final)

    for el in res2_3:
        if (el[1] not in list_final):
            list_final.append(el[1])

    # check if there are still any keywords remain (meaning that lvl 3 is not fulfilled)
    # immediately return if any keywords remain
    if (lvl2_3):
        return clean_text(list_final)
    
    lvl4 = convert_keywords(['setiap opd', 
           'seluruh opd', 
           'setiap unit kerja', 
           'seluruh unit kerja', 
           'setiap pemerintah daerah',
           'seluruh pemerintah daerah'])
    res4 = txtreader(filename, 4, lvl4)

    for el in res4:
        if (el[1] not in list_final):
            list_final.append(el[1])

    return clean_text(list_final)


filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
# filename = 'PERBUB NO 34 TAHUN 2019 TENTANG RENCANA INDUK SPBE.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)
teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity
print(teks_final)
print(instansibaru, judulbaru)
print(instansilama, judullama)