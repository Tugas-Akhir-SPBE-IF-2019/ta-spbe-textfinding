# this code is for TEXT FINDING - INDIKATOR 2
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
            for key in keyword:

                if re.search(key, line, re.IGNORECASE):
                    result.append([idx, line])

        else:  # lv == 4
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

    lvl1 = ["Peta Rencana SPBE"]
    res1 = txtreader(filename, 1, lvl1)

    # cek if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    lvl2 = ["Tata Kelola SPBE", "Manajemen SPBE", "Layanan SPBE", "Infrastruktur SPBE", "Aplikasi SPBE", "Keamanan SPBE", "Audit Teknologi Informasi dan Komunikasi", "Audit TIK"]
    res2 = txtreader(filename, 2, lvl2)

    if (not res2):
        return ''

    for el in res2:
        if (el[1] not in list_final):
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


# filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
# filename = 'Draft Perbup SPBE 2021 Revisi.pdf'
filename = 'PERBUB NO 34 TAHUN 2019 TENTANG RENCANA INDUK SPBE.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)
teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity
print(teks_final)
