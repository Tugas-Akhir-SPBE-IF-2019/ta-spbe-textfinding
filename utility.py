import re

# Convert array of keywords to its regex version
# Input: Array of Keywords
# Output: Regex version of Keywords
def convert_keywords(keywords):
    result = []

    for keyword in keywords:
        regex_keyword = f""

        for word in keyword.split():
            # Current word is the first word in keyword
            if (not regex_keyword):
                regex_keyword += f"(?:({word})"
            else:
                regex_keyword += f"\s+({word})"

        regex_keyword += ")"
        result.append(regex_keyword)

    return result

# Clean collected lines and merge into a single paragraph
# Input: Array of Lines
# Output: String
def clean_text(list_final):
    text_final = ". ".join(list_final)

    # clean text
    text_final = re.sub(r'(\n)+', '', text_final, flags=re.MULTILINE)
    text_final = re.sub(r'(;)+', ',', text_final, flags=re.MULTILINE)

    return text_final