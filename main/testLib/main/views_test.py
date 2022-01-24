# Test format  'function {name} _ {given} _ {expects} _ test'
from main.testLib.TestCommon import *
from main.globalParams import *
from main.models import User, ChatBot

from unittest.mock import MagicMock
from django.http import Http404

valid_user = User.objects.all()[0]
valid_bot_path = ChatBot.objects.all()[0].path


@patch('main.corpusModels.corpusGeneratorFactory')
def homePage_BlankInput_ValidPage_test(*args):
    # Arrange
    from main.views import homePage
    request  = REQ_FACTORY.get('home')
    # Act
    response = homePage(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def register_BlankInput_ValidPage_test(*args):
    # Arrange
    from main.views import register
    request  = REQ_FACTORY.get('register')
    # Act
    response = register(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.forms.CreateNewUser')
@patch('main.forms.ChangeProfileInfo')
@patch('django.contrib.messages')
@patch('django.contrib.auth.login')
@patch('main.corpusModels.corpusGeneratorFactory')
def register_MockProfileData_RedirectsAndUserLoggedIn_test(*args):
    # Arrange
    from main.views import register
    from django.contrib.auth import login
    request  = REQ_FACTORY.post('register')
    # Act
    response = register(request)
    # Assert
    assert(response.status_code == 302)
    assert(login.call_count == 1)


@patch('main.corpusModels.corpusGeneratorFactory')
def register_InvalidForm_validPage_test(*args):
    # Arrange
    from main.views import register
    request  = REQ_FACTORY.post('register', {})
    # Act
    response = register(request)
    # Assert
    assert(response.status_code == 200)


@patch('django.contrib.auth.login')
@patch('main.corpusModels.corpusGeneratorFactory')
def logInUser_BlankInput_ValidPageNoLogIn_test(*args):
    # Arrange
    from main.views import logInUser
    from django.contrib.auth import login
    request  = REQ_FACTORY.get('logIn')
    # Act
    response = logInUser(request)
    # Assert
    assert(response.status_code == 200)
    assert(login.call_count == 0)


@patch('django.contrib.auth.authenticate')
@patch('django.contrib.auth.login')
@patch('django.contrib.messages')
@patch('main.corpusModels.corpusGeneratorFactory')
def logInUser_MockUser_UserLoggedIn_test(*args):
    # Arrange
    from main.views import logInUser
    from django.contrib.auth import authenticate, login
    request  = REQ_FACTORY.post('logIn')
    # Act
    response = logInUser(request)
    # Assert
    assert(response.status_code == 302)
    assert(authenticate.call_count == 1)
    assert(login.call_count == 1)


@patch('django.contrib.auth.login')
@patch('django.contrib.messages')
@patch('main.corpusModels.corpusGeneratorFactory')
def logInUser_InvalidUser_ValidPageNoLogIn_test(*args):
    # Arrange
    from main.views import logInUser
    from django.contrib.auth import login
    request  = REQ_FACTORY.post('logIn')
    # Act
    response = logInUser(request)
    # Assert
    assert(response.status_code == 200)
    assert(login.call_count == 0)


@patch('django.contrib.auth.logout')
@patch('main.corpusModels.corpusGeneratorFactory')
def logOutUser_BlankInput_RedirectsCallsLogout_test(*args):
    # Arrange
    from main.views import logOutUser
    from django.contrib.auth import logout
    request  = REQ_FACTORY.post('logOut')
    # Act
    response = logOutUser(request)
    # Assert
    assert(response.status_code == 302)
    assert(logout.call_count == 1)


@patch('main.corpusModels.corpusGeneratorFactory')
def writeStory_ValidUser_ValidPage_test(*args):
    # Arrange
    from main.views import writeStory
    request  = REQ_FACTORY.get('writeStory')
    request.user = valid_user
    # Act
    response = writeStory(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def loadSavedStory_ValidUser_ValidPage_test(*args):
    # Arrange
    from main.views import loadSavedStory
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = loadSavedStory(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.forms.SavedStory')
@patch('main.corpusModels.corpusGeneratorFactory')
def loadSavedStory_ValidUserMockStory_ValidPage_test(*args):
    # Arrange
    from main.views import loadSavedStory
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = loadSavedStory(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def loadSavedVocab_ValidUserNoVocab_Redirects_test(*args):
    # Arrange
    from main.views import loadSavedVocab
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = loadSavedVocab(request)
    # Assert
    assert(response.status_code == 302)


@patch('main.forms.SavedVocab')
@patch('main.corpusModels.corpusGeneratorFactory')
def loadSavedVocab_ValidUserMockVocab_ValidPage_test(*args):
    # Arrange
    from main.views import loadSavedVocab
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = loadSavedVocab(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def selectVocabToAlter_ValidUser_ValidPage_test(*args):
    # Arrange
    from main.views import selectVocabToAlter
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = selectVocabToAlter(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def alterVocab_InvalidChatBot_Redirects_test(*args):
    # Arrange
    from main.views import alterVocab
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = alterVocab(request, '')
    # Assert
    assert(response.status_code == 302)


@patch('main.corpusModels.corpusGeneratorFactory')
def alterVocab_ValidChatBot_ValidPage_test(*args):
    # Arrange
    from main.views import alterVocab
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = alterVocab(request, valid_bot_path)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def savedStories_ValidUser_ValidPage_test(*args):
    # Arrange
    from main.views import savedStories
    request  = REQ_FACTORY.get('loadSavedStory')
    request.user = valid_user
    # Act
    response = savedStories(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def saveStory_ValidUserNoAjax_RasiesHttp404_test(*args):
    # Arrange
    from main.views import saveStory
    request  = REQ_FACTORY.post('saveStory')
    request.user = valid_user
    # Act & Assert
    assertRaises(saveStory, Http404, request)


@patch('main.corpusModels.corpusGeneratorFactory')
def saveStory_ValidUserAjaxAndPost_ValidPage_test(*args):
    # Arrange
    from main.views import saveStory
    request  = REQ_FACTORY.post('saveStory')
    request.user = valid_user
    request.is_ajax = lambda: True
    request.POST = {'data': True}
    # Act
    response = saveStory(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def saveVocabAlteration_ValidUserNoAjax_RasiesHttp404_test(*args):
    # Arrange
    from main.views import saveVocabAlteration
    request  = REQ_FACTORY.post('saveVocabAlteration')
    request.user = valid_user
    # Act & Assert
    assertRaises(saveVocabAlteration, Http404, request)


@patch('main.corpusModels.corpusGeneratorFactory')
def saveVocabAlteration_ValidUserAjaxAndPost_ValidPage_test(*args):
    # Arrange
    from main.views import saveVocabAlteration
    request  = REQ_FACTORY.post('saveVocabAlteration')
    request.user = valid_user
    request.is_ajax = lambda: True
    request.POST = {'data': True}
    # Act
    response = saveVocabAlteration(request)
    # Assert
    assert(response.status_code == 200)


@patch('main.corpusModels.corpusGeneratorFactory')
def talkToServer_ValidUserNoAjax_RasiesHttp404_test(*args):
    # Arrange
    from main.views import talkToServer
    request  = REQ_FACTORY.post('talkToServer')
    request.user = valid_user
    # Act & Assert
    assertRaises(talkToServer, Http404, request)


@patch('main.corpusModels.corpusGeneratorFactory')
def talkToServer_ValidUserAjaxAndPost_ValidPage_test(*args):
    # Arrange
    from main.views import talkToServer
    request  = REQ_FACTORY.post('talkToServer')
    request.user = valid_user
    request.is_ajax = lambda: True
    request.POST = {'data': True}
    # Act
    response = talkToServer(request)
    # Assert
    assert(response.status_code == 200)


if __name__ == '__main__':
    runAllTests(locals().copy())
