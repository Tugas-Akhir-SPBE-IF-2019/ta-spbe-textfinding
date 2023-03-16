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

        elif (lv == 3):
            # Check primary word first:
            # 1. "Manajemen Data"
            # 2. "Data dan Informasi"
            reg1 = f'(?:(manajemen)\s+(data))'
            reg2 = f'(?:(data)\s+(dan)\s+(informasi))'

            if (re.search(reg1, line, re.IGNORECASE) or re.search(reg2, line, re.IGNORECASE)):
                # Use regex to handle multiple whitespaces
                res = [ele for ele in keyword if (re.search(ele, line, re.IGNORECASE))]
                if (res and not excludewords(line)):
                    result.append([idx, line])

        else:  # lv == 5
            # Check primary word first:
            # 1. Manajemen Data SPBE
            reg = f'(?:(manajemen)\s+(data)\s+(spbe))'
            if (re.search(reg, line, re.IGNORECASE)):
                res = [ele for ele in keyword if (ele in line)]
                if (res):
                    result.append([idx, line])

        idx += 1

    file.close()
    return (result)


# if __name__ == '__main__':
#     pdfparser(sys.argv[1])

def excludewords(line):
    exclude = ["sistem", "domain", "aplikasi"]
    found = False

    for ele in exclude:
        if found:
            break
        if (ele in line.lower()):
            found = True
    return found

def ceklvl(filename):
    list_final = []
    text_final = ''

    # Same keyword for lvl1 and lvl2
    lvl1 = ["manajemen data"]
    res1 = txtreader(filename, 1, lvl1)

    # cek if keyword lvl1 is not found, then return as empty string
    if (not res1):
        return ''

    # Add first line found containing "manajemen data" to list_final for level 2
    list_final.append(res1[0][1])

    # Same keyword for lvl3 and lvl4
    lvl3 = [f"(?:(Arsitektur)\s+(Data))",f"(?:(Data)\s+(Induk))",
            f"(?:(Data)\s+(Referensi))", f"(?:(Basis)\s+(Data))",
            f"(?:(Kualitas)\s+(Data))", f"(?:(Interoperabilitas)\s+(Data)?)"]
    res3 = txtreader(filename, 3, lvl3)

    # Return result for level 2 if no Level 3 Keywords found
    if (not res3):
        text_final = ". ".join(list_final)
        text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
        text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)
        return text_final

    for el in res3:
        if (el[1] not in list_final):
            list_final.append(el[1])

    lvl5 = ["integrasi", "reviu", "diselaraskan", "berpedoman", "pedoman", "perubahan"]
    res5 = txtreader(filename, 5, lvl5)

    for el in res5:
        if (el[1] not in list_final):
            list_final.append(el[1])

    text_final = ". ".join(list_final)

    # clean text
    text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
    text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)

    # return text_final
    return text_final


# filename = 'F2201-287-Indikator_01~+~Indikator1_Perbup_81_tahun_2021.pdf'
# filename = 'Draft Perbup SPBE 2021 Revisi.pdf'
filename = 'PERBUB NO 34 TAHUN 2019 TENTANG RENCANA INDUK SPBE.pdf'

# (instansibaru, judulbaru) = dokbaru.pdfparser(filename)
# (instansilama, judullama) = doklama.pdfparser(filename)
teks_final = ceklvl(filename)

# hasil text finding
# bisa langsung digunakan ke model text similarity

print(teks_final)

# print(instansibaru, judulbaru)
# print(instansilama, judullama)
