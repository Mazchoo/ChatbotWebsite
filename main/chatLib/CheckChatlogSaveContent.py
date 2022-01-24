
from enum import Enum
from collections import OrderedDict
import pdb

from main.globalParams import *
from main.forms import (Content, ChatSaveContent, ChatParagraph,
                        ChatChapter, ChatTitle, ChatExists)
import main.models


class ChatLogErrors(Enum):
    no_error             = 'Content Saved Successfully'
    too_many_items       = 'Chatlog exceeds total number of items'
    no_title_found       = 'Chatlog has no title.'
    no_exists_okay       = 'Unknown Error'
    cannot_parse_exists  = 'Unknown Error'
    invalid_chapter      = 'Chapter title has invalid length'
    invalid_paragraph    = 'ParagraphText has invalid length'
    already_exists       = 'Chatlog already exists'
    title_too_long       = 'Chatlog title is too long or invalid'
    too_many_stories     = 'Maximum number of stories for one user reached'
    content_too_long     = 'Content exceeds maximum number of characters'
    title_not_unique     = 'You already have a story with this name'
    unknown_error        = 'Unknown Error'


def verifyTitle(request_post):
    if 'content[title0]' not in request_post.keys():
        return None, ChatLogErrors.no_title_found
    title = request_post['content[title0]']

    content_form = ChatTitle({'title': title})
    if content_form.is_valid():
        cleaned_content = content_form.cleaned_data['title']
        return cleaned_content, ChatLogErrors.no_error

    return None, ChatLogErrors.title_too_long


def verifyExistsOk(request_post):
    if 'content[existsOk0]' not in request_post.keys():
        return ChatLogErrors.no_exists_okay, None

    existsOk = request_post['content[existsOk0]']
    content_form = ChatExists({'text_content': existsOk})
    if not content_form.is_valid():
        return ChatLogErrors.cannot_parse_exists, None

    return ChatLogErrors.no_error, content_form.cleaned_data['exists_okay']


def verifStoryContent(content, content_type):
    if content_type == Content.chapter._value_:
        content_form = ChatChapter({'text_content': content})

        if content_form.is_valid():
            text = content_form.cleaned_data['text_content']
            return ChatLogErrors.no_error, text
        else:
            return ChatLogErrors.invalid_chapter, None

    elif content_type == Content.pgraph._value_:
        content_form = ChatParagraph({'text_content': content})

        if content_form.is_valid():
            text = content_form.cleaned_data['text_content']
            return ChatLogErrors.no_error, text
        else:
            return ChatLogErrors.invalid_paragraph, None

    else:
        return ChatLogErrors.no_error, None


def getPreviousChatlog(request_post, title, user):
    error, existsOk = verifyExistsOk(request_post)
    if not error == ChatLogErrors.no_error:
        return error, None

    log_objects = main.models.ChatLog.objects
    logs_same_name = log_objects.filter(author=user).filter(name=title)
    chatlog = None
    if logs_same_name.exists():
        if not existsOk:
            return ChatLogErrors.already_exists, None
        chatlog = logs_same_name[0]

    return ChatLogErrors.no_error, chatlog


def verifyChatlog(request_post, user_profile):

    if len(request_post) > MAX_NR_CONTENT_ITEMS:
        return ChatLogErrors.too_many_items, None, None, None

    if user_profile.nr_stories + 1 > MAX_STORIES_PER_USER:
        return ChatLogErrors.too_many_stories, None, None, None

    title, error = verifyTitle(request_post)
    if not error == ChatLogErrors.no_error:
        return error, None, None, None

    user = user_profile.user
    error, prev_log = getPreviousChatlog(request_post, title, user)
    if not error == ChatLogErrors.no_error:
        return error, None, None, None

    output_content = OrderedDict()
    content_ind = 0
    total_content_len = 0
    for key, value in request_post.lists():
        content_type_form = ChatSaveContent({'name': key})

        if not content_type_form.is_valid():
            continue
        content_type = content_type_form.cleaned_data['content_type']

        error, content = verifStoryContent(value, content_type)
        if not error == ChatLogErrors.no_error:
            return error, None, None, None

        if content is None:
            continue

        content_ind += 1
        total_content_len += len(content)

        if total_content_len > MAX_CHATLOG_LENGTH:
            return ChatLogErrors.content_too_long, None, None, None

        output_content[content_type + str(content_ind)] = content

    return ChatLogErrors.no_error, output_content, title, prev_log
