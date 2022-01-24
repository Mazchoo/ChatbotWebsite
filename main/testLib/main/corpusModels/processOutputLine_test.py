# Test format  'function {name} _ {given} _ {expects} _ test'

from main.testLib.TestCommon import *

from main.corpusModels.processOutputLine import *


def processOutputLine_Empty_Empty_test():
    # Act & Assert
    assert(processOutputLine('') == '')


def processOutputLine_String_RemovedTabs_test():
    # Act & Assert
    assert(processOutputLine('\tI like \tcheese.\t') == 'I like cheese.')


def processOutputLine_String_RemovesNewLines_test():
    # Act & Assert
    assert(processOutputLine('\nI like \ncheese.\n') == 'I like cheese.')


def processOutputLine_String_RemovesSpacesBeforePunctuation_test():
    # Arrange
    period_str = 'That , \' " .'
    expected_period_str = 'That,\'".'

    exclaim_str = 'That , \' " !'
    exclaim_period_str = 'That,\'"!'

    question_str = 'That , \' " ?'
    question_period_str = 'That,\'"?'
    # Act & Assert
    assert(processOutputLine(period_str) == expected_period_str)
    assert(processOutputLine(exclaim_str) == exclaim_period_str)
    assert(processOutputLine(question_str) == question_period_str)


def processOutputLine_String_RemovesDividers_test():
    # Act & Assert
    assert(processOutputLine('Hello . # Goodbye ... # Ook! ') == 'Goodbye.')


def processOutputLine_StringWithNoHashes_Unchanged_test():
    # Act & Assert
    assert(processOutputLine('Hello') == 'Hello')


def processOutputLine_String_KeepsFirstSentence_test():
    # Arrange
    period_sentence = 'What. Dare I ask.'
    question_sentence = 'What? Dare I ask.'
    exclamation_sentence = 'What! Dare I ask.'
    # Act & Assert
    assert(processOutputLine(period_sentence) == 'What.')
    assert(processOutputLine(question_sentence) == 'What?')
    assert(processOutputLine(exclamation_sentence) == 'What!')


def processOutputLine_String_removesSpace_test():
    # Act & Assert
    assert(processOutputLine(' Hello.') == 'Hello.')


def processOutputLine_String_capitalizesI_test():
    # Act & Assert
    assert(processOutputLine('i like i think i, i') == 'I like I think I, I')


def processOutputLine_SplitupWord_JoinsWords_test():
    # Arrange
    split_up_sentence = 'I did n\'t gon na got ta'
    expected_sentence = 'I didn\'t gonna gotta'
    # Act & Assert
    assert(processOutputLine(split_up_sentence) == expected_sentence)


def processOutputLine_MultipleSpaces_OneSpace_test():
    # Act & Assert
    assert(processOutputLine('   I  like   owls.  ') == 'I like owls.')


def processOutputLine_SpeechMarks_RemovesSpeechMarks_test():
    single_quote_sentence = 'I \'d say , \' Go away ! \''
    expected_single_quote = 'I\'d say, Go away!'

    double_quote_sentence = 'I \'d say , \" Go away ! \"'
    expected_double_quote = 'I\'d say, Go away!'
    # Act & Assert
    assert(processOutputLine(single_quote_sentence) == expected_single_quote)
    assert(processOutputLine(double_quote_sentence) == expected_double_quote)


def validPublicWord_WordTooShort_False_test():
    # Act & Assert
    assert(not validPublicWord('I'))
    assert(not validPublicWord('No'))


def validPublicWord_SpecialToken_False_test():
    # Act & Assert
    assert(not validPublicWord('xxNo'))
    assert(not validPublicWord('xxx'))


def validPublicWord_InvalidCharacters_False_test():
    # Act & Assert
    assert(not validPublicWord('TheCool#'))
    assert(not validPublicWord('The_Dude'))
    assert(not validPublicWord('Cheese Bomb'))


def validPublicWord_validWord_True_test():
    # Act & Assert
    assert(validPublicWord('1984'))
    assert(validPublicWord('Cheese'))
    assert(validPublicWord('12Cheese'))
    assert(validPublicWord('WooBoo3'))


if __name__ == '__main__':
    runAllTests(locals().copy())
