# this code is for TEXT FINDING - INDIKATOR 9
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
            for key in keyword:
                reg = f'(?:(audit)\s({key}))'
                if (re.search(reg, line, re.IGNORECASE)):
                    result.append([idx, line])

        else:  # lv == 2
            # cek dgn keyword 'audit'
            for key in keyword:

                # manfaatin regex untuk searching yg not only kata keyword
                reg = f'(?:(audit)\s({key}))'
                if (re.search(reg, line, re.IGNORECASE)):
                    result.append([idx, line])
                    # hapus key yg udh ditemuin supaya gausah di search lagi
                    keyword.remove(key)

        idx += 1

    file.close()
    return (result)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])

def ceklvl(filename):
    list_final = []
    text_final = ''

    lvl1 = ["TIK", "Teknologi Informasi dan Komunikasi"]
    res1 = txtreader(filename, 1, lvl1)

    # cek if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    lvl2 = ["Infrastruktur SPBE", "Aplikasi SPBE", "Keamanan SPBE"]
    res2 = txtreader(filename, 2, lvl2)

    for el in res2:
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
