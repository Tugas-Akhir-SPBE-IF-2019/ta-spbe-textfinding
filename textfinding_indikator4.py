# this code is for TEXT FINDING - INDIKATOR 4
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

    include = ['aplikasi', 'aplikasi khusus', 'aplikasi umum', 'aplikasi spbe']

    # read line by line from txt
    for line in file:

        if (lv == 1):
            reg = f'(?:(pembangunan)(.*?)(aplikasi)\s+(spbe)?)'
            if (re.search(reg, line, re.IGNORECASE)):
                result.append([idx, line])

        elif (lv == 2):
            for key in keyword:
                if re.search(key, line, re.IGNORECASE):

                    # include words
                    res = [ele for ele in include if (
                        ele in line.lower())]
                    if (res):

                        # exclude words
                        if (not excludewords(line)):
                            result.append([idx, line])
                            keyword.remove(key)

        elif (lv == 3):
            for key in keyword:
                if re.search(key, line, re.IGNORECASE):
                    res = [ele for ele in include if (
                        ele in line.lower())]
                    if (res):
                        result.append([idx, line])
                        keyword.remove(key)

        elif (lv == 4):
            res = [ele for ele in keyword if (ele in line)]
            if (len(res) == len(keyword)):  # if all keyword is found in the same sentence
                res = [ele for ele in include if (
                    ele in line.lower())]
                if (res):
                    if (not excludewords(line)):
                        result.append([idx, line])

        else:
            reg = f'(?:(aplikasi)\s+(spbe))'
            if (re.search(reg, line.lower(), re.IGNORECASE)):
                if (re.search(keyword[0], line.lower(), re.IGNORECASE)):
                    if (not excludewords(line)):
                        result.append([idx, line])

        idx += 1

    file.close()
    return (result, keyword)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])

def excludewords(line):
    # TODO
    # need better lines of code to exclude words

    exclude = ['badan', 'anggaran', 'belanja', 'TIK', 'manajemen', 'fungsi',
               'infrastruktur', 'interoperabilitas', 'rencana induk', 'program', 'pelayanan']
    found = False

    for ele in exclude:
        if found == True:
            break
        if re.search(ele, line, re.IGNORECASE):
            found = True
    return found


def ceklvl(filename):
    list_final = []
    text_final = ''

    res1, keyword = txtreader(filename, 1, [])

    # cek if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return text_final

    lvl2 = ["perencanaan", "analisis", "desain", "implementasi",
            "pemeliharaan"]
    res2, keyword = txtreader(filename, 2, lvl2)

    for el in res2:
        if (el[1] not in list_final):
            list_final.append(el[1])

    # if lvl2 tdk terpenuhi (not all keyword found), end pengecekan lvl
    if (keyword):
        return cleantext(list_final)

    lvl3 = ["konsultasi", "koordinasi"]
    res3, keyword = txtreader(filename, 3, lvl3)

    if (not res3):
        return cleantext(list_final)

    for el in res3:
        if (el[1] not in list_final):
            list_final.append(el[1])

    lvl4 = ["terpadu", "endali"]
    res4, keyword = txtreader(filename, 4, lvl4)

    if (not res4):
        return cleantext(list_final)

    for el in res4:
        if (el[1] not in list_final):
            list_final.append(el[1])

    lvl5 = ["reviu"]
    res5, keyword = txtreader(filename, 5, lvl4)

    for el in res5:
        if (el[1] not in list_final):
            list_final.append(el[1])

    return cleantext(list_final)


def cleantext(list_final):
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
