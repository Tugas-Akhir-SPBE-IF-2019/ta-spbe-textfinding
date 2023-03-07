# this code is for TEXT FINDING - INDIKATOR 1
# input is txt file from preprocess dokumen lama, nama instansi & judul from dokumen lama & baru

import re
import preprocess_dokbaru as dokbaru
import preprocess_doklama as doklama


def txtreader(filename, keyword):
    file = open(f'cleaned_{filename}.txt', 'r')

    idx = 0
    result = []

    lvl2_exclude = ['audit']

    for line in file:
        if (len(keyword) == 1):
            if re.search(keyword[0], line, re.IGNORECASE):
                result.append([idx, line])

        else:
            # check with keyword 'domain'
            for key in keyword:
                reg = f'(?:(domain)\s(arsitektur)?\s({key}))'
                if re.search(reg, line, re.IGNORECASE):
                    result.append([idx, line])

            # TODO
            # check without keyword 'domain'

        idx += 1

    file.close()
    return (result)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])

def ceklvl():
    list_final = []
    text_final = ''

    lvl1 = ["arsitektur SPBE"]
    res1 = txtreader(filename, lvl1)

    # cek if keyword lvl1 is not found
    if (not res1):
        return ''

    lvl2 = ["Proses Bisnis", "Data dan Informasi", "Infrastruktur SPBE",
            "Aplikasi SPBE", "Keamanan SPBE", "Layanan SPBE"]
    res2 = txtreader(filename, lvl2)

    if (not res2):
        return ''

    for el in res2:
        list_final.append(el[1])

    lvl4 = ["integrasi", "reviu"]
    res4 = txtreader(filename, lvl4)

    for el in res4:
        list_final.append(el[1])

    text_final = ". ".join(list_final)

    # clean text
    text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
    text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)

    return text_final


filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
filename2 = 'Draft Perbup SPBE 2021 Revisi.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)

level_final = ceklvl()
