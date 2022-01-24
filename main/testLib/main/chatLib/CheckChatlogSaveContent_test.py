# Test format  'function {name} _ {given} _ {expects} _ test'

from main.testLib.TestCommon import *
from main.globalParams import *

from main.chatLib.CheckChatlogSaveContent import *
from main.models import UserProfileInfo, ChatLog

from main.testLib.CommonMocks import createMockUserProfile, createMockQuery

from collections import OrderedDict


valid_query = {
    'content[title0]': "Valid Title",
    'content[existsOk0]': True,
    'content[chapter1]': "The Old Adventure",
    'content[pgraph2]': "Cheese is good.",
    'content[pgraph3]': "A new paragraph.",
    'csrfmiddlewaretoken': "randomToken",
}


def createExpectedContent():
    output = OrderedDict()
    output['chapter1'] = "'The Old Adventure'"
    output['pgraph2'] = "'Cheese is good.'"
    output['pgraph3'] = "'A new paragraph.'"

    return output


def verifyChatlog_NoTitleContent_Error_test():
    # Arrange
    profile = createMockUserProfile()
    log = createMockQuery(valid_query)
    del log['content[title0]']
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.no_title_found)


def verifyChatlog_TitleTooLong_Error_test():
    # Arrange
    long_title = '#' * (MAX_TITLE_LENGTH + 1)
    log = createMockQuery(valid_query, {'content[title0]': long_title})
    profile = createMockUserProfile()
    # Act

    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.title_too_long)


def verifyChatlog_NoExistsOkayContent_Error_test():
    # Arrange
    profile = createMockUserProfile()
    log = createMockQuery(valid_query)
    del log['content[existsOk0]']
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.no_exists_okay)


def verifyChatlog_ContentTooLong_Error_test():
    # Arrange
    profile = createMockUserProfile()
    long_log = {str(i):i for i in range(MAX_NR_CONTENT_ITEMS + 1)}
    log = createMockQuery(valid_query, long_log)
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.too_many_items)


def verifyChatlog_TooManyStoriesPerUser_Error_test():
    # Arrange
    profile = createMockUserProfile({'nr_stories': MAX_STORIES_PER_USER})
    log = createMockQuery(valid_query)
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.too_many_stories)


@patch('main.models')
def verifyChatlog_NotExistsOkay_Error_test(*args):
    # Arrange
    profile = createMockUserProfile()
    log = createMockQuery(valid_query, {'content[existsOk0]': False})
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.already_exists)


@patch('main.models')
def verifyChatlog_ParagraphIsTooLong_Error_test(*args):
    # Arrange
    profile = createMockUserProfile()
    long_string = 'e' * (MAX_PARAGRAPH_LENGTH + PARAGRAPH_LENGTH_LEYWAY + 1)
    log = createMockQuery(valid_query, {'content[pgraph2]': long_string})
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.invalid_paragraph)


@patch('main.models')
def verifyChatlog_ChapterIsTooLong_Error_test(*args):
    # Arrange
    profile = createMockUserProfile()
    long_string = 'e' * (CHAPTER_MAX_LENGTH + 1)
    log = createMockQuery(valid_query, {'content[chapter1]': long_string})
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.invalid_chapter)


@patch('main.models')
def verifyChatlog_TotalContentIsTooLong_Error_test(*args):
    # Arrange
    profile = createMockUserProfile()
    long_string = 'e' * MAX_PARAGRAPH_LENGTH

    long_paragraphs = {}
    for i in range(2, MAX_NR_PARAGRAPHS + 2):
        long_paragraphs[f'content[pgraph{i}]'] = long_string
    log = createMockQuery(valid_query, long_paragraphs)
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    # test assumes maximum length has been beached
    assert(MAX_PARAGRAPH_LENGTH * MAX_NR_PARAGRAPHS > MAX_CHATLOG_LENGTH)
    assert(error == ChatLogErrors.content_too_long)


@patch('main.models')
def verifyChatlog_TooManyContentItems_Error_test(*args):
    # Arrange
    profile = createMockUserProfile()
    too_many_items = {}
    for i in range(2, MAX_NR_CONTENT_ITEMS + 2):
        too_many_items[f'content[pgraph{i}]'] = 'spam'
    log = createMockQuery(valid_query, too_many_items)
    # Act
    error, content, title, prev_log = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.too_many_items)


@patch('main.models')
def verifyChatlog_ValidChatlog_ValidOutput_test(*args):
    # Arrange
    profile = createMockUserProfile()
    log = createMockQuery(valid_query)
    expected_content = createExpectedContent()
    # Act
    error, content, title, _ = verifyChatlog(log, profile)
    # Assert
    assert(error == ChatLogErrors.no_error)
    assert(title == 'Valid Title')
    assert(content == expected_content)


if __name__ == '__main__':
    runAllTests(locals().copy())
