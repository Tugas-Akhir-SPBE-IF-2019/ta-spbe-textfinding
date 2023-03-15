# this code is for TEXT FINDING - INDIKATOR 1
# input is txt file from preprocess dokumen lama, nama instansi & judul from dokumen lama & baru

import re
import preprocess_dokbaru as dokbaru
import preprocess_doklama as doklama


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
            # cek dgn keyword 'domain'. cont: domain arsitektur proses bisnis, domain data dan informasi, domain arsitektur keamanan, dll
            for key in keyword:

                if re.search(key, line, re.IGNORECASE):
                    result.append([idx, line])

        else:  # lv == 5
            # check if line contains any keyword from list
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

    # Same keyword for lvl1 and lvl2

    lvl1 = ["manajemen data"]
    res1 = txtreader(filename, 1, lvl1)

    # cek if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    # Same keyword for lvl3 and lvl4

    lvl3 = ["arsitektur data","data induk", "data referensi",
    "basis data", "kualitas data", "interoperabilitas data"]
    res3 = txtreader(filename, 3, lvl3)

    if (not res3):
        res3 = txtreader(filename, 3, lvl3)

    for el in res3:
        if (el[1] not in list_final):
            list_final.append(el[1])

    lvl5 = ["integrasi", "reviu", "diselaraskan", "berpedoman", "perubahan"]
    res5 = txtreader(filename, 5, lvl5)

    for el in res5:
        if (el[1] not in list_final):
            list_final.append(el[1])

    # text_final = ". ".join(list_final)

    # clean text
    # text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
    # text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)

    # return text_final
    return list_final


filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
# filename2 = 'Draft Perbup SPBE 2021 Revisi.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)
teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity

# print(teks_final)
for line in teks_final:
    print(line)

# print(instansibaru, judulbaru)
# print(instansilama, judullama)
