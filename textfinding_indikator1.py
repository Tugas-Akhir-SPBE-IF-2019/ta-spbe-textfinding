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

    # TODO
    # exclude some words
    lvl2_exclude = ['audit']

    # read line by line from txt
    for line in file:

        if (lv == 1):
            if re.search(keyword[0], line, re.IGNORECASE):
                result.append([idx, line])

        elif (lv == 2):
            # cek dgn keyword 'domain'. cont: domain arsitektur proses bisnis, domain data dan informasi, domain arsitektur keamanan, dll
            for key in keyword:

                # manfaatin regex untuk searching yg not only kata keyword
                reg = f'(?:(domain)\s(arsitektur)?\s?({key}))'
                if re.search(reg, line, re.IGNORECASE):
                    result.append([idx, line])

        elif (lv == 3):
            # masih pengecekan keyword yg sama dgn level 2, tapi tanpa 'domain'
            for key in keyword:

                # gausah regex krn searching nya langsung kata keyword tanpa ada embel embel 'domain'
                if re.search(reg, line, re.IGNORECASE):
                    result.append([idx, line])

                    # hapus key yg udh ditemuin supaya gausah di search lagi
                    keyword.remove(key)

        else:  # lv == 4
            # cek dulu keyword utama level 4 which is arsitektur spbe nasional
            word = "Arsitektur SPBE Nasional"

            # kalau ketemu, lanjut cek keyword [integrasi, reviu, dll]
            if (re.search(word, line, re.IGNORECASE)):
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

    lvl1 = ["arsitektur SPBE"]
    res1 = txtreader(filename, 1, lvl1)

    # cek if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    lvl2 = ["Proses Bisnis", "Data dan Informasi", "Infrastruktur SPBE",
            "Aplikasi SPBE", "Keamanan SPBE", "Layanan SPBE"]
    res2 = txtreader(filename, 2, lvl2)

    if (not res2):
        res2 = txtreader(filename, 3, lvl2)

    for el in res2:
        list_final.append(el[1])

    lvl4 = ["integrasi", "reviu", "diselaraskan", "berpedoman", "perubahan"]
    res4 = txtreader(filename, 4, lvl4)

    for el in res4:
        list_final.append(el[1])

    text_final = ". ".join(list_final)

    # clean text
    text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
    text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)

    return text_final


filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
# filename2 = 'Draft Perbup SPBE 2021 Revisi.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)
teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity
print(teks_final)
print(instansibaru, judulbaru)
print(instansilama, judullama)
