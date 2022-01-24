import re
import pdb

seperator = '(\s|^|$|\.|\?|!)'


def replaceVocab(out_line: str, base_word: str, new_word: str):
    def replaceWord(expr_match):
        return expr_match.group(0).replace(base_word, new_word)
    escaped_word = seperator + re.escape(base_word) + seperator

    return re.sub(escaped_word, replaceWord, out_line)


def replaceVocabOutput(out_line: str, vocab_alteration):
    for base_word, new_word in vocab_alteration.items():
        out_line = replaceVocab(out_line, base_word, new_word)

    return out_line


def replaceVocabInput(out_line: str, vocab_alteration):
    for new_word, base_word in vocab_alteration.items():
        out_line = replaceVocab(out_line, base_word, new_word)

    return out_line
