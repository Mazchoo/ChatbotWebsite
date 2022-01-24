# Test format  'function {name} _ {given} _ {expects} _ test'
from main.testLib.TestCommon import *
from main.chatLib.TalkToServer import *

from unittest.mock import Mock


class MockStaticGenerator(Mock):
    def __init__(self, output_line):
        super().__init__()
        self.output_line = output_line

    def predictSentence(self, *args, **kwargs):
        return self.output_line


class MockRemoveSpacesGenerator(Mock):
    def __init__(self):
        super().__init__()

    def predictSentence(self, last_sentence, *args, **kwargs):
        return last_sentence.replace(' ', '')


class MockCorpusFactory(Mock):
    def __init__(self, generator):
        super().__init__()
        self.generator = generator

    def createPredictor(self, *args, **kwargs):
        return self.generator


class MockSentenceData(Mock):
    def __init__(self, _is_valid, fields={}):
        super().__init__()
        self.cleaned_data = {
            'last_sentence': 'I like bread.',
            'chatbot_name': 'Valid Chatbot',
        }
        self.cleaned_data.update(fields)
        self._is_valid = _is_valid

    def is_valid(self):
        return self._is_valid


class MockAlterations(Mock):
    def __init__(self, alterations):
        super().__init__()
        self.alterations = alterations


def getOutputChatLineForRequest_None_EmptyString_test():
    # Arrange
    corpus_factory = MockCorpusFactory(MockRemoveSpacesGenerator())
    valid_sentence_data  = MockSentenceData(True)
    invalid_sentence_data  = MockSentenceData(False)
    # Act
    res1 = getOutputChatLineForRequest(None, corpus_factory)
    res2 = getOutputChatLineForRequest(valid_sentence_data, None)
    res3 = getOutputChatLineForRequest(invalid_sentence_data, corpus_factory)
    # Assert
    assert(res1 == '')
    assert(res2 == '')
    assert(res3 == '')


def getOutputChatLineForRequest_ValidInputLine_ExpectedOutLine_test():
    # Arrange
    expected_output = 'I like bread.'
    corpus_factory = MockCorpusFactory(MockStaticGenerator(expected_output))
    sentence_data  = MockSentenceData(True)
    # Act
    out_line = getOutputChatLineForRequest(sentence_data, corpus_factory)
    # Assert
    assert(out_line == expected_output)


def getOutputChatLineForRequest_AlterationOnOutput_AltersOutput_test():
    # Arrange
    corpus_factory = MockCorpusFactory(MockStaticGenerator('I like bread.'))
    fields = {'vocab_alteration' : MockAlterations({
        'I': 'You', 'like': 'love', 'bread': 'cheese'
    })}
    sentence_data  = MockSentenceData(True, fields)
    # Act
    result = getOutputChatLineForRequest(sentence_data, corpus_factory)
    # Assert
    assert(result == 'You love cheese.')


def getOutputChatLineForRequest_AlterationOnInput_AltersInput_test():
    # Arrange
    corpus_factory = MockCorpusFactory(MockRemoveSpacesGenerator())
    fields = {'vocab_alteration' : MockAlterations({
        'You': 'I', 'love': 'like', 'cheese': 'bread'
    })}
    sentence_data = MockSentenceData(True, fields)
    # Act
    result = getOutputChatLineForRequest(sentence_data, corpus_factory)
    # Assert
    assert(result == 'Youlovecheese.')


if __name__ == '__main__':
    runAllTests(locals().copy())
