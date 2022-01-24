# Test format  'function name _ given _ expects'

from main.testLib.TestCommon import *

from unittest.mock import Mock


class FastAIPredictor(Mock):
    def predict(self, *args, **kwargs):
        return 'Hello'

from main.corpusModels.corpusGenerator import *
generator = CorpusGenerator(FastAIPredictor(), {'Hello': 'Hi'}, 'newb')


def predict_None_EmptyString_test(*args, **kwargs):
    # Act & Assert
    assert(generator.predictSentence(None) == '')


def predict_String_String_test(*args, **kwargs):
    # Act & Assert
    assert(type(generator.predictSentence('What is up?')) == str)


if __name__ == '__main__':
    runAllTests(locals().copy())
