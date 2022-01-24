import re
import pdb

def removeDividers(text: str):
    text = text[text.find('#') + 1:]
    if sentence_end := re.search(r'#', text):
        text = text[:sentence_end.end() - 1]
    return text


def removeLineBreaks(text: str):
    text = re.sub("\t", "", text)
    return re.sub("\n", "", text)


def keepOnlyOneSentence(text: str):
    if sentence_end := re.search(r'[\.\?!]', text):
        text = text[:sentence_end.end()]
    return text


def removeSpacesBeforePunctuation(text: str):
    return re.sub(r'\s([\?\.!,"\'])', r'\1', text)


def correctBadPhrases(text: str):
    text = re.sub(" n't", "n't", text)
    text = re.sub("gon na", "gonna", text)
    text = re.sub("got ta", "gotta", text)
    return text


def removeQuotationMarks(text: str):
    return re.sub('[\'"][\s$]', ' ', text)


def capitalizeI(text: str):
    text = re.sub(r"i(\s|$)", r"I\1", text)
    return re.sub(r"\si(\.|\?|!|,)", r" I\1", text)


def removeExcessSpaces(text: str):
    return re.sub("\s{1,}", " ", text)


def processOutputLine(text: str):
    text = removeDividers(text)
    text = removeLineBreaks(text)
    text = keepOnlyOneSentence(text)
    text = removeSpacesBeforePunctuation(text)
    text = correctBadPhrases(text)
    text = removeQuotationMarks(text)
    text = capitalizeI(text)
    text = removeExcessSpaces(text)
    text = text.strip()
    return text


def validPublicWord(word: str):
    if len(word) < 3:
        return False
    elif word[:2] == 'xx':
        return False
    elif not re.match('^[a-zA-Z0-9\-]+$', word):
        return False
    else:
        return True


if __name__ == '__main__':
    input_line = "No . # \"What 's the matter ?\" # Nothing ... We."
    print(processOutputLine(input_line))
