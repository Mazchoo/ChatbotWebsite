# Test format  'function {name} _ {given} _ {expects} _ test'
from main.testLib.TestCommon import *
from main.chatLib.CheckVocabSaveContent import *

from collections import OrderedDict

from main.testLib.CommonMocks import createMockUserProfile, createMockQuery

save_content = {
    'title': "French",
    'existsOk': True,
    'chatbot': "valid_chatbot",
    'content[green]': "vert",
    'content[cheese]': "fromage",
    'csrfmiddlewaretoken': "randomToken",
}


def createExpectedOutput():
    out_dict = OrderedDict()
    out_dict['green'] = 'vert'
    out_dict['cheese'] = 'fromage'

    return out_dict


def verifyVocabAlteration_UserHasTooManyVocabs_Error_test():
    # Arrange
    profile = createMockUserProfile({'nr_vocabs': MAX_VOCABS_PER_USER})
    vocab = createMockQuery(save_content)
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.too_many_vocabs)


def verifyVocabAlteration_VocabAlterationTooLong_Error_test():
    # Arrange
    profile = createMockUserProfile()
    extra_words = {}
    for i in range(1, MAX_VOCAB_LENGTH + 2):
        extra_words[f'content[word{i}]'] = f'new_word{i}'
    vocab = createMockQuery(save_content, extra_words)
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.content_too_long)


def verifyVocabAlteration_NoTitle_Error_test():
    # Arrange
    profile = createMockUserProfile()
    vocab = createMockQuery(save_content)
    del vocab['title']
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.no_title)


def verifyVocabAlteration_TooShortTitle_Error_test():
    # Arrange
    profile = createMockUserProfile()
    vocab = createMockQuery(save_content, {'title': ''})
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.empty_title)


def verifyVocabAlteration_TooLongTitle_Error_test():
    # Arrange
    profile = createMockUserProfile()
    long_title = 'e' * (MAX_TITLE_LENGTH + 1)
    vocab = createMockQuery(save_content, {'title': long_title})
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.invalid_title)


def verifyVocabAlteration_NoExistsOkay_Error_test():
    # Arrange
    profile = createMockUserProfile()
    vocab = createMockQuery(save_content)
    del vocab['existsOk']
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.empty_exist_ok)


@patch('main.models')
def verifyVocabAlteration_TitleNotUnique_Error_test(*args):
    # Arrange
    profile = createMockUserProfile()
    vocab = createMockQuery(save_content, {'existsOk': False})
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.title_not_unique)


@patch('main.models')
def verifyVocabAlteration_NoChatbot_Error_test(*args):
    # Arrange
    profile = createMockUserProfile()
    vocab = createMockQuery(save_content)
    del vocab['chatbot']
    # Act
    error, content, title, bot, previous = verifyVocabAlteration(vocab, profile)
    # Assert
    assert(error == VocabErrors.no_chatbot)


@patch('main.models')
def createVocabOutputContent_ValidInput_ValidOutput_test(*args):
    # Arrange
    vocab = createMockQuery(save_content)
    valid_words = ['he', 'is', 'green', 'cheese']
    # Act
    error, content = createVocabOutputContent(vocab, valid_words)
    # Assert
    assert(error == VocabErrors.no_error)
    assert(content == createExpectedOutput())


@patch('main.models')
def createVocabOutputContent_InvalidWord_Error_test(*args):
    # Arrange
    vocab = createMockQuery(save_content)
    valid_words = ['unused-word']
    # Act
    error, content = createVocabOutputContent(vocab, valid_words)
    # Assert
    assert(error == VocabErrors.invalid_word)


if __name__ == '__main__':
    runAllTests(locals().copy())
