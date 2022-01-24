# Test format  'function {name} _ {given} _ {expects} _ test'

from main.testLib.TestCommon import *

from main.corpusModels.corpusGeneratorFactory import *


@patchModelLoading
def init_GlobalFileTable_CreatesLearners_test(*args, **kwargs):
    # Act
    generator_factory = CorpusGeneratorFactory(CHATBOT_MODEL_FILES)
    # Assert
    assert(len(generator_factory) == len(CHATBOT_MODEL_FILES))
    for key, _ in generator_factory:
        assert(key in CHATBOT_MODEL_FILES.keys())


@patchModelLoading
def init_EmptyDict_CreatesEmptyDict_test(*args, **kwargs):
    # Act & Assert
    assert(len(CorpusGeneratorFactory({})) == 0)


@patchModelLoading
def init_BadDict_GeneratorWithNone_test(*args, **kwargs):
    # Arrange
    bad_file_paths = {'spam': 'spam.spam'}
    # Act
    corpus_generators = CorpusGeneratorFactory(bad_file_paths)
    # Assert
    assert(len(corpus_generators) == len(bad_file_paths))
    for key, val in corpus_generators:
        assert(key == 'spam')
        assert(val is None)


if __name__ == '__main__':
    runAllTests(locals().copy())
