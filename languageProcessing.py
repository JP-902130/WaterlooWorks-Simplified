import re


def getMatchingIndex(string):

    string = string.lower()

    keyword = ["react", "node", "mongodb",
               "express", "rest", "javascript", "api"]
    banned = ["C#", ".net", "Java", "spring"]
    count = 0
    for each in keyword:
        count += string.count(each.lower())
    for each in banned:
        count -= string.count(each.lower())
    return count


def getIDFromString(string):

    # Sample string
    text = string

    # Use regular expression to extract the 6-digit number
    match = re.search(r"\d{6}", text)

    # Extract the matched substring
    if match:
        six_digit_number = match.group(0)

    # Print the result
    return(six_digit_number)
