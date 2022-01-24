# Test format  'function {name} _ {given} _ {expects} _ test'
from main.testLib.TestCommon import *
from main.globalParams import *

from unittest.mock import MagicMock


def homePageUrl():
    # Act & Assert
    assert(CLIENT.get('/').status_code == 200)


def loginUrl():
    # Act & Assert
    assert(CLIENT.get('/login').status_code == 200)


def logoutUrl_Redirects():
    # Act
    response = CLIENT.get('/logout')
    # Assert
    assert(response.status_code == 302)
    assert(response.url == '/')


def registerUrl():
    # Act & Assert
    assert(CLIENT.get('/register').status_code == 200)


def writeUrl():
    # Act & Assert
    assert(CLIENT.get('/write').status_code == 200)


def writeUrl():
    # Act & Assert
    assert(CLIENT.get('/write').status_code == 200)


def vocabUrl():
    # Act & Assert
    assert(CLIENT.get('/vocab').status_code == 200)


def vocabWithModelUrl():
    # Act & Assert
    for model in CHATBOT_MODEL_FILES.keys():
        assert(CLIENT.get(f'/vocab/{model}/').status_code == 200)


def savedUrl():
    # Act & Assert
    assert(CLIENT.get('/saved').status_code == 200)


@patch('main.forms')
def loadStoryUrl(*args):
    # Act & Assert
    assert(CLIENT.get('/loadStory').status_code == 200)


@patch('main.forms.SavedVocab')
def loadVocabUrl_MockVocabData(*args):
    # Act & Assert
    assert(CLIENT.get('/loadVocab').status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def urls_test(*args):
    loginUrl()
    loginClient()

    writeUrl()
    homePageUrl()
    registerUrl()
    vocabUrl()
    vocabWithModelUrl()
    savedUrl()
    loadStoryUrl()

    loadVocabUrl_MockVocabData()
    logoutUrl_Redirects()


if __name__ == '__main__':
    runAllTests(locals().copy())
