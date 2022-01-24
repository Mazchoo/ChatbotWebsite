# Test format  'function {name} _ {given} _ {expects} _ test'

from main.testLib.TestCommon import *

from main.corpusModels.vocabReplacer import *


def replaceVocabOutput_Sentence_replacesWord_test():
    # Act
    output = replaceVocabOutput('Sausage Bacon', {'Sausage': 'Bacon'})
    # Assert
    assert(output == 'Bacon Bacon')


def replaceVocabOutput_SentenceWithPunctuation_replacesWord_test():
    # Act
    output = replaceVocabOutput('Sausage! Sausage?', {'Sausage': 'Bacon'})
    # Assert
    assert(output == 'Bacon! Bacon?')


def replaceVocabInput_Sentence_replacesWord_test():
    # Act
    output = replaceVocabInput('Sausage Bacon', {'Sausage': 'Bacon'})
    # Assert
    assert(output == 'Sausage Sausage')


def replaceVocabInput_SentenceWithPunctuation_replacesWord_test():
    # Act
    output = replaceVocabInput('Bacon! Bacon?', {'Sausage': 'Bacon'})
    # Assert
    assert(output == 'Sausage! Sausage?')


if __name__ == '__main__':
    runAllTests(locals().copy())
