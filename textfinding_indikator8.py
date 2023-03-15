# this code is for TEXT FINDING - INDIKATOR 8
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
            # check using 
            for key in keyword:

                reg = f'{key}'
                if re.search(reg, line, re.IGNORECASE):
                    result.append([idx, line])
        
        else: #lv 2,3, and 4 should follow the same pattern
            # TODO 
            # this still doesn't feel right to me; subject for later change
            reg = f'manajemen keamanan informasi'

            if (re.search(reg, line, re.IGNORECASE)):
                # check if line contains any keyword from list
                res = [ele for ele in keyword if (ele in line)]
                if (res):
                    result.append([idx, line])

        idx += 1

    file.close()
    return (result)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])


# for indicator 8, ceklvl will only check against lvl2 keywords only
# because the rest are related to lvl2 and will be checked in the next step (text similarity)
def ceklvl(filename):
    list_final = []
    text_final = ''

    lvl1 = ["manajemen keamanan informasi"]
    res1 = txtreader(filename, 1, lvl1)

    # check if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    for el in res1:
        list_final.append(el[1])

    # keywords for level 2 and 3 are the same
    lvl2_3 = ['penetapan ruang lingkup', 
              'penetapan penanggung jawab', 
              'perencanaan', 
              'dukungan pengoperasian',
              'evaluasi kinerja',
              'perbaikan berkelanjutan terhadap Keamanan Informasi']
    res2_3 = txtreader(filename, 2, lvl2_3)

    for el in res2_3:
        if (el[1] not in list_final):
            list_final.append(el[1])
    
    lvl4 = ['setiap opd', 
           'seluruh opd', 
           'setiap unit kerja', 
           'seluruh unit kerja', 
           'setiap pemerintah daerah',
           'seluruh pemerintah daerah']
    res4 = txtreader(filename, 4, lvl4)

    for el in res4:
        if (el[1] not in list_final):
            list_final.append(el[1])

    text_final = ". ".join(list_final)

    # clean text
    text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
    text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)

    return text_final


filename = 'F2201-287-Indikator_01_+_Indikator1_Perbup_81_tahun_2021.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)

teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity
print(teks_final)
