# Test format  'function {name} _ {given} _ {expects} _ test'
from main.testLib.TestCommon import *
from main.forms import *
from main.globalParams import *


valid_user_id  = User.objects.all()[0].id
valid_bot_id   = ChatBot.objects.all()[0].id
valid_bot_path = ChatBot.objects.all()[0].path
valid_vocab_id = VocabAlteration.objects.all()[0].id
valid_story_id = ChatLog.objects.all()[0].id


def ChatBotLogEditor_validData_isValid_test():
    # Arrange
    data = {
        'author': valid_user_id,
        'text_content': {"chapter1": "Dude", "pgraph2": "<p>Hello.</p>"},
        'name': 'The Story'
    }
    # Act
    form = ChatBotLogEditor(data)
    # Assert
    assert(form.is_valid())


def ChatBotLogEditor_titleTooLong_isNotValid_test():
    # Arrange
    data = {
        'author': valid_user_id,
        'text_content': {"chapter1": "Dude", "pgraph2": "<p>Hello.</p>"},
        'name': '#' * (MAX_TITLE_LENGTH + 1)
    }
    # Act
    form = ChatBotLogEditor(data)
    # Assert
    assert(not form.is_valid())


def ChatBotLogEditor_titleTooShort_isNotValid_test():
    # Arrange
    data = {
        'author': valid_user_id,
        'text_content': {"chapter1": "Dude", "pgraph2": "<p>Hello.</p>"},
        'name': ''
    }
    # Act
    form = ChatBotLogEditor(data)
    # Assert
    assert(not form.is_valid())


def VocabAlteration_validData_isValid_test():
    # Arrange
    data = {
        'author': valid_user_id,
        'name': 'The Alteration',
        'bot': valid_bot_id,
        'alterations': {'Oui': 'Yes'}
    }
    # Act
    form = VocabAlterationForm(data)
    # Assert
    assert(form.is_valid())


def VocabAlteration_titleTooLong_isNotValid_test():
    # Arrange
    data = {
        'author': valid_user_id,
        'name': '#' * (MAX_TITLE_LENGTH + 1),
        'bot': valid_bot_id,
        'alterations': {'Oui': 'Yes'}
    }
    # Act
    form = VocabAlterationForm(data)
    # Assert
    assert(not form.is_valid())


def VocabAlteration_titleTooShort_isNotValid_test():
    # Arrange
    data = {
        'author': valid_user_id,
        'name': '',
        'bot': valid_bot_id,
        'alterations': {'Oui': 'Yes'}
    }
    # Act
    form = VocabAlterationForm(data)
    # Assert
    assert(not form.is_valid())


def ChatInput_validData_isValid_test():
    # Arrange
    data = {
        'last_sentence': 'I like cheese.',
        'chatbot_name': valid_bot_path,
        'temperature': '100',
        'vocab_id': valid_vocab_id,
        'user_id': valid_user_id
    }
    # Act
    form = ChatInput(data)
    # Assert
    assert(form.is_valid())


def ChatInput_temperatureTooHigh_isNotValid_test():
    # Arrange
    data = {
        'last_sentence': 'I like cheese.',
        'chatbot_name': valid_bot_path,
        'temperature': '999',
        'vocab_id': valid_vocab_id,
        'user_id': valid_user_id
    }
    # Act
    form = ChatInput(data)
    # Assert
    assert(not form.is_valid())


def ChatInput_temperatureTooLow_isNotValid_test():
    # Arrange
    data = {
        'last_sentence': 'I like cheese.',
        'chatbot_name': valid_bot_path,
        'temperature': '-10',
        'vocab_id': valid_vocab_id,
        'user_id': valid_user_id
    }
    # Act
    form = ChatInput(data)
    # Assert
    assert(not form.is_valid())


def ChatParagraph_validData_isValid_test():
    # Arrange
    data = {'text_content': ' [<p>I like cheese</p>] '}
    # Act
    form = ChatParagraph(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['text_content'] == '<p>I like cheese</p>')


def ChatParagraph_scriptTag_removesScript_test():
    # Arrange
    data = {'text_content': ' [<script>I like cheese</script>] '}
    # Act
    form = ChatParagraph(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['text_content'] == '')


def ChatChapter_alidData_isValid_test():
    # Arrange
    data = {'text_content': ' [<p>I like cheese</p>] '}
    # Act
    form = ChatChapter(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['text_content'] == '<p>I like cheese</p>')


def ChatChapter_scriptTag_removesScript_test():
    # Arrange
    data = {'text_content': ' [<script>I like cheese</script>] '}
    # Act
    form = ChatChapter(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['text_content'] == '')


def ChatTitle_validData_isValid_test():
    # Arrange
    data = {'title': ' [I like cheese] '}
    # Act
    form = ChatTitle(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['title'] == 'I like cheese')


def ChatTitle_emptyString_isNotValid_test():
    # Arrange
    data = {'title': ''}
    # Act
    form = ChatTitle(data)
    # Assert
    assert(not form.is_valid())


def ChatTitle_scriptTags_removesTags_test():
    # Arrange
    data = {'title': '[<script>The</script> Thing]'}
    # Act
    form = ChatTitle(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['title'] == 'The Thing')


def ChatTitle_emptyAfterScriptRemoval_isNotValid_test():
    # Arrange
    data = {'title': '[<script></script>]'}
    # Act
    form = ChatTitle(data)
    # Assert
    assert(not form.is_valid())


def ChatTitle_emptyAfterScriptRemoval_isNotValid_test():
    # Arrange
    data = {'title': '[<script></script>]'}
    # Act
    form = ChatTitle(data)
    # Assert
    assert(not form.is_valid())


def ChatExists_FalseString_isValid_test():
    # Arrange
    data = {'text_content': 'false'}
    # Act
    form = ChatExists(data)
    # Assert
    assert(form.is_valid())


def ChatExists_TrueString_isValid_test():
    # Arrange
    data = {'text_content': 'true'}
    # Act
    form = ChatExists(data)
    # Assert
    assert(form.is_valid())


def ChatExists_InvalidString_isNotValid_test():
    # Arrange
    data = {'text_content': 'form'}
    # Act
    form = ChatExists(data)
    # Assert
    assert(not form.is_valid())


def VocabTitle_validData_isValid_test():
    # Arrange
    data = {'title': 'I like cheese'}
    # Act
    form = VocabTitle(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['title'] == 'I like cheese')


def VocabTitle_emptyString_isNotValid_test():
    # Arrange
    data = {'title': ''}
    # Act
    form = VocabTitle(data)
    # Assert
    assert(not form.is_valid())


def VocabTitle_scriptTags_removesTags_test():
    # Arrange
    data = {'title': '<script>The</script> Thing'}
    # Act
    form = VocabTitle(data)
    # Assert
    assert(form.is_valid())
    assert(form.cleaned_data['title'] == 'The Thing')


def VocabTitle_emptyAfterScriptRemoval_isNotValid_test():
    # Arrange
    data = {'title': '<script></script>'}
    # Act
    form = VocabTitle(data)
    # Assert
    assert(not form.is_valid())


def ChatSaveContent_validContentType_isValid_test():
    # Arrange
    data = [{'name': f'[{c}100]'} for c in Content.__members__]
    # Act
    results = [ChatSaveContent(d) for d in data]
    # Arrange
    for form in results:
        assert(form.is_valid())


def ChatSaveContent_invalidContentType_isNotValid_test():
    # Arrange
    data = {'name': f'[varyBadContentType100]'}
    # Act
    form = ChatSaveContent(data)
    # Arrange
    assert(not form.is_valid())


def WordAlteration_ValidWords_isValid_test():
    # Arrange
    data = {
        'base_word': 'content[A]',
        'new_word': '_[B]_'
    }
    # Act
    form = WordAlteration(data)
    # Arrange
    assert(form.is_valid())


def WordAlteration_invalidBaseWord_isNotValid_test():
    # Arrange
    data = {
        'base_word': 'content[#]',
        'new_word': '_[B]_'
    }
    # Act
    form = WordAlteration(data)
    # Arrange
    assert(not form.is_valid())


def WordAlteration_invalidNewWord_isNotValid_test():
    # Arrange
    data = {
        'base_word': 'content[A]',
        'new_word': '_[#]_'
    }
    # Act
    form = WordAlteration(data)
    # Arrange
    assert(not form.is_valid())


def WordAlteration_BaseWordNewWordSame_isNotValid_test():
    # Arrange
    data = {
        'base_word': 'content[Same]',
        'new_word': '_[Same]_'
    }
    # Act
    form = WordAlteration(data)
    # Arrange
    assert(not form.is_valid())


def SavedStory_validStoryId_isValid_test():
    # Arrange
    data = {'story_id': valid_story_id}
    # Act
    form = SavedStory(data)
    # Arrange
    assert(form.is_valid())


def SavedStory_invalidStoryId_isNotValid_test():
    # Arrange
    data = {'story_id': -1}
    # Act
    form = SavedStory(data)
    # Arrange
    assert(not form.is_valid())


def SavedVocab_validVocabId_isValid_test():
    # Arrange
    data = {'vocab_id': valid_vocab_id}
    # Act
    form = SavedVocab(data)
    # Arrange
    assert(form.is_valid())


def SavedVocab_invalidVocabId_isNotValid_test():
    # Arrange
    data = {'vocab_id': -1}
    # Act
    form = SavedVocab(data)
    # Arrange
    assert(not form.is_valid())


if __name__ == '__main__':
    runAllTests(locals().copy())
