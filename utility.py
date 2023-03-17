# Convert array of keywords to its regex version
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
