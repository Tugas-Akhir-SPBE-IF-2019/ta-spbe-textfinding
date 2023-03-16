# this code is for TEXT FINDING - INDIKATOR 5
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

        if (lv == 2):
            # check using 
            reg = f'(?:\s?(jaringan intra))'
            if re.search(reg, line, re.IGNORECASE):
                result.append([idx, line])

        if (lv == 3):
            # check using 
            for key in keyword:

                reg = f'{key}'
                if re.search(reg, line, re.IGNORECASE):
                    result.append([idx, line])
        
        else:  # lv == 4

            # TODO 
            # this still doesn't feel right to me; subject for later change
            reg = f'(?:\s?(jaringan intra))'

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


# for indicator 7, ceklvl will only check against lvl2 keywords only
# because the rest are related to lvl2 and will be checked in the next step (text similarity)
def ceklvl(filename):
    list_final = []
    text_final = ''

    # empty keywords; the check will use built in regex in txtreader function
    lvl2 = []
    res2 = txtreader(filename, 2, lvl2)

    # check if keyword lvl2 is not found, then return as empty string
    if (not res2):
        return ''

    for el in res2:
        list_final.append(el[1])
    
    # TODO
    # this can be optimized by using regex
    lvl3 = ['setiap opd', 
           'seluruh opd', 
           'setiap unit kerja', 
           'seluruh unit kerja', 
           'setiap pemerintah daerah',
           'seluruh pemerintah daerah']
    res3 = txtreader(filename, 3, lvl3)

    for el in res3:
        list_final.append(el[1])

    lvl4 = ['keterhubungan', 
            'hubung', 
            'integrasi', 
            'berpedoman', 
            'reviu', 
            'diselaraskan', 
            'perubahan']
    res4 = txtreader(filename, 4, lvl4)

    for el in res4:
        list_final.append(el[1])

    text_final = ". ".join(list_final)

    # clean text
    text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
    text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)

    return text_final


filename = 'PhakPhakBarat.pdf'
# filename = 'BatuBara.pdf'

(instansibaru, judulbaru) = dokbaru.pdfparser(filename)
(instansilama, judullama) = doklama.pdfparser(filename)

teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity
print("\nTeks:\n", teks_final, "\n")
# print(instansibaru, judulbaru)
# print(instansilama, judullama)