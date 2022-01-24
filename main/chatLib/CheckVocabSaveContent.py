
from enum import Enum
from collections import OrderedDict
import pdb

from main.globalParams import *
from main.forms import VocabTitle, WordAlteration
import main.models


class VocabErrors(Enum):
    no_error         = 'Content Saved Successfully'
    invalid_chatbot  = 'Invalid Chatbot url'
    invalid_word     = 'Alteration made to Unknown Word'
    content_too_long = 'Too many alterations'
    no_title         = 'Invalid Title'
    invalid_title    = 'Invalid Title'
    empty_title      = 'Empty Title'
    empty_exist_ok   = 'No save definition'
    title_not_unique = 'You already have some vocab with this name'
    too_many_vocabs  = 'Maximum number of Vocab Alterations has been reached'
    no_chatbot       = 'No Chatbot'
    unknown_error    = 'Unknown Error'


def verifyTitle(request_post):
    if "title" not in request_post.keys():
        return VocabErrors.no_title, None

    title = request_post["title"]

    if len(title) == 0:
        return VocabErrors.empty_title, None

    vocab_title_form = VocabTitle({'title': title})
    if not vocab_title_form.is_valid():
        return VocabErrors.invalid_title, None

    return VocabErrors.no_error, vocab_title_form.cleaned_data['title']


def titleAlreadyExists(title, user):
    vocab_objects = main.models.VocabAlteration.objects
    alterations = vocab_objects.filter(author=user).filter(name=title)
    if alterations.exists():
        return alterations[0]


def getPreviousAlteration(request_post, title, user):
    if "existsOk" not in request_post.keys():
        return VocabErrors.empty_exist_ok, None

    alteration = titleAlreadyExists(title, user)
    if request_post["existsOk"]:
        return VocabErrors.no_error, titleAlreadyExists(title, user)
    else:
        if alteration:
            return VocabErrors.title_not_unique, None
        else:
            return VocabErrors.no_error, None


def verifyChatbot(request_post):
    if 'chatbot' not in request_post.keys():
        return VocabErrors.no_chatbot, None

    chat_bot_objects = main.models.ChatBot.objects
    chat_bot = chat_bot_objects.get(path=request_post['chatbot'])
    if not chat_bot:
        return VocabErrors.invalid_chatbot, None

    return VocabErrors.no_error, chat_bot


def createVocabOutputContent(request_post, valid_vocab):
    output_content = OrderedDict()

    for key, value in request_post.lists():
        word_form = WordAlteration({'base_word': key, 'new_word': value})

        if word_form.is_valid():
            base_word = word_form.cleaned_data['base_word']
            new_word  = word_form.cleaned_data['new_word']

            if base_word not in valid_vocab:
                return VocabErrors.invalid_word, None

            output_content[base_word] = new_word

    return VocabErrors.no_error, output_content


def verifyVocabAlteration(request_post, user_profile):

    if user_profile.nr_vocabs + 1 > MAX_VOCABS_PER_USER:
        return VocabErrors.too_many_vocabs, None, None, None, None

    if len(request_post) > MAX_VOCAB_CONTENT_LENGTH:
        return VocabErrors.content_too_long, None, None, None, None

    error, title = verifyTitle(request_post)
    if not error == VocabErrors.no_error:
        return error, None, None, None, None

    user = user_profile.user
    error, previous = getPreviousAlteration(request_post, title, user)
    if not error == VocabErrors.no_error:
        return error, None, None, None, None

    error, bot = verifyChatbot(request_post)
    if not error == VocabErrors.no_error:
        return error, None, None, None, None

    error, content = createVocabOutputContent(request_post, bot.public_vocab)
    if not error == VocabErrors.no_error:
        return error, None, None, None, None

    return VocabErrors.no_error, content, title, bot, previous
