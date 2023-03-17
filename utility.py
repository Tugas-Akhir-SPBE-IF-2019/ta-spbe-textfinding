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

# Check if a word exist in a line
# Input: Array of Excluded Keywords, Line
# Output: Found/Not Found
def exclude_words(exclude_keywords, line):
    found = False

    for ele in exclude_keywords:
        if found:
            break
        if (ele in line.lower()):
            found = True
    return found
