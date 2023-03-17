# this code is for TEXT FINDING - INDIKATOR 2
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

    # read line by line from txt
    for line in file:

        if (lv == 1):
            if re.search(keyword[0], line, re.IGNORECASE):
                result.append([idx, line])

        elif (lv == 2):
            # Check primary words first:
            # 1. "Peta Rencana SPBE"
            # 2. "Rencana Strategis"
            reg1 = f'(?:(peta)\s+(rencana)\s+(spbe))'
            reg2 = f'(?:(rencana)\s+(strategis))'

            if (re.search(reg1, line, re.IGNORECASE) or re.search(reg2, line, re.IGNORECASE)):
                # Use regex to handle multiple whitespaces
                res = [ele for ele in keyword if (re.search(ele, line, re.IGNORECASE))]
                if (res):
                    result.append([idx, line])

        else:  # lv == 4
            # Check primary words first:
            # 1. "Peta Rencana SPBE Nasional"
            # 2. "Rencana Induk SPBE Nasional"
            reg1 = f'(?:(peta)\s+(rencana)\s+(spbe)\s+(nasional))'
            reg2 = f'(?:(rencana)\s+(induk)\s+(spbe)\s+(nasional))'

            if (re.search(reg1, line, re.IGNORECASE) or re.search(reg2, line, re.IGNORECASE)):
                res = [ele for ele in keyword if (ele in line)]
                if (res):
                    result.append([idx, line])

        idx += 1

    file.close()
    return (result)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])

def ceklvl(filename):
    list_final = []
    text_final = ''

    lvl1 = convert_keywords(["Peta Rencana SPBE"])
    res1 = txtreader(filename, 1, lvl1)

    # cek if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    # Regex keywords to handle multiple whitespaces
    lvl2 = convert_keywords([
        "Tata Kelola SPBE", "Manajemen SPBE",
        "Layanan SPBE", "Infrastruktur SPBE",
        "Aplikasi SPBE", "Keamanan SPBE",
        "Audit Teknologi Informasi dan Komunikasi",
        "Audit TIK"
    ])
    res2 = txtreader(filename, 2, lvl2)

    # Terminate immediately if no Level 2 Keywords found
    if (not res2):
        return ''

    for el in res2:
        if (el[1] not in list_final):
            list_final.append(el[1])

    lvl4 = ["integrasi", "reviu", "diselaraskan", "berpedoman", "perubahan"]
    res4 = txtreader(filename, 4, lvl4)

    for el in res4:
        list_final.append(el[1])

    return clean_text(list_final)


# filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
# filename = 'Draft Perbup SPBE 2021 Revisi.pdf'
filename = 'PERBUB NO 34 TAHUN 2019 TENTANG RENCANA INDUK SPBE.pdf'

# (instansibaru, judulbaru) = dokbaru.pdfparser(filename)
# (instansilama, judullama) = doklama.pdfparser(filename)
teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity
print(teks_final)
