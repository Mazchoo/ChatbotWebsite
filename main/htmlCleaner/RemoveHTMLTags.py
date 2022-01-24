
import re


def removeScriptTag(text):
    return re.sub('</?script.*>', '', text, flags=re.IGNORECASE)


def removeSquareBrackets(text):
    text = re.sub('^.*\[', '', text)
    return re.sub('\].*$', '', text)


def removeHTMLTag(text):
    return re.sub('</?html.*>', '', text, flags=re.IGNORECASE)


def getParagraphTypeIndex(nameText):
    match = re.findall('\[([a-zA-Z]+)(\d+)\]', nameText)
    return match


def checkValidUserWord(word):
    return re.match('^[a-zA-Z0-9\-]+$', word)


def removeAllTags(text):
    return removeScriptTag(re.sub('<[^<]+?>', '', text))
