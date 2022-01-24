import json
import pdb
import re

import main.forms as forms
import main.models as models
import django.contrib as contrib # for mocking messages
import django.contrib.auth as auth

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from main.common.viewHelperFunctions import *
from main.chatLib import *
import main.corpusModels.corpusGeneratorFactory as cf
BOT_FACTORY = cf.CorpusGeneratorFactory(CHATBOT_MODEL_FILES)


def homePage(request):
    context = {
        "max_input_length": MAX_INPUT_SENTENCE_LENGTH,
        "bot_name": "movie_dialog",
    }
    return render(
        request=request,
        template_name='home.html',
        context=context
    )


def register(request):
    if request.method == "POST":
        form = forms.CreateNewUser(request.POST)
        profile_form = forms.ChangeProfileInfo(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES.keys():
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            contrib.messages.success(request, "Account created for " + username)
            auth.login(request, user)
            return redirect('/')
    else:
        form = forms.CreateNewUser()
        profile_form = forms.ChangeProfileInfo()

    context = {'register_form': form, 'profile_form': profile_form}
    return render(
        request=request,
        template_name='register.html',
        context=context
    )


def logInUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            contrib.messages.info(request, "Invalid username/password combination")

    return render(
        request=request,
        template_name='login.html',
        context={}
    )


def logOutUser(request):
    auth.logout(request)
    return redirect('/')


def generateStoryContext(user):
    context = {
        "max_input_sentence_length": MAX_INPUT_SENTENCE_LENGTH,
        "max_nr_chapters": MAX_NR_CHAPTERS,
        "max_nr_paragraphs": MAX_NR_PARAGRAPHS,
        "max_paragraph_length": MAX_PARAGRAPH_LENGTH,
        "max_title_length": MAX_TITLE_LENGTH,
        "paragraph_leyway": PARAGRAPH_LENGTH_LEYWAY,
        "max_total_length": MAX_CHATLOG_LENGTH,
        "max_chapter_length": CHAPTER_MAX_LENGTH,
        "chapter_tag": forms.Content.chapter._value_,
        "paragraph_tag": forms.Content.pgraph._value_,
        "title_tag": forms.Content.title._value_,
        "chatbots": models.ChatBot.objects.all(),
        "vocabs":  models.VocabAlteration.objects.filter(author=user),
        "log_form": forms.TinyMCEComponent(),
        "loaded_story": None
    }
    return context


@login_required(login_url='/login')
def writeStory(request):
    context = generateStoryContext(request.user)

    return render(
        request=request,
        template_name='editWithChatbot.html',
        context=context
    )


@login_required(login_url='/login')
def loadSavedStory(request):
    context = generateStoryContext(request.user)

    story_form = forms.SavedStory(request.POST)
    if story_form.is_valid():
        context['loaded_story'] = story_form.cleaned_data['story']

    return render(
        request=request,
        template_name='editWithChatbot.html',
        context=context
    )


def addExtraFieldsToVocabContext(context: dict):
    extra_fields = {
        "max_title_length": MAX_TITLE_LENGTH,
        "max_vocab_length": MAX_VOCAB_LENGTH,
        "title_tag": Content.title._value_,
        "max_word_size": MAX_WORD_SIZE,
    }
    context.update(extra_fields)


@login_required(login_url='/login')
def loadSavedVocab(request):
    vocab_form = forms.SavedVocab(request.POST)

    if vocab_form.is_valid():
        vocab = vocab_form.cleaned_data['vocab']
        context = {"chat_bot": vocab.bot}
        addExtraFieldsToVocabContext(context)
        context['loaded_vocab'] = vocab

        return render(
            request=request,
            template_name='alterVocabulary.html',
            context=context
        )
    return redirect('/vocab')


@login_required(login_url='/login')
def selectVocabToAlter(request):
    context = {'chatbots': models.ChatBot.objects.all()}
    return render(
        request=request,
        template_name='selectChatbot.html',
        context=context
    )


@login_required(login_url='/login')
def alterVocab(request, bot_path):
    matching_chatbots = models.ChatBot.objects.all().filter(path=bot_path)

    if matching_chatbots.exists():
        context = {"chat_bot": matching_chatbots[0]}
        addExtraFieldsToVocabContext(context)

        return render(request=request,
                      template_name='alterVocabulary.html',
                      context=context)
    return redirect('/vocab')


@login_required(login_url='/login')
def savedStories(request):
    context = {
        "stories": models.ChatLog.objects.filter(author=request.user),
        "vocabs": models.VocabAlteration.objects.filter(author=request.user),
    }
    return render(
        request=request,
        template_name='savedStories.html',
        context=context
    )


@ajaxRequest
@checkPost
@login_required(login_url='/login')
def saveStory(request):
    user_profile = models.UserProfileInfo.objects.get(user_id=request.user.id)
    error, output_content, title, prev_chatlog = verifyChatlog(
        request.POST, user_profile
    )

    if error == ChatLogErrors.no_error:
        if prev_chatlog is None:
            log_form = forms.ChatBotLogEditor({
                'author': request.user,
                'text_content': output_content,
                'name': title,
            })

            if log_form.is_valid():
                log_form.save(commit=True)
                user_profile.nr_stories += 1
                user_profile.save()
            else:
                error = ChatLogErrors.unknown_error
        else:
            prev_chatlog.text_content = output_content
            prev_chatlog.save()

    return HttpResponse(error._value_, content_type='text/plain')


@ajaxRequest
@checkPost
@login_required(login_url='/login')
def saveVocabAlteration(request):
    user_profile = models.UserProfileInfo.objects.get(user_id=request.user)
    error, output_content, title, chat_bot, prev_alteration = verifyVocabAlteration(
        request.POST, user_profile
    )

    if error == VocabErrors.no_error:
        if prev_alteration is None:
            alteration_form = forms.CreateNewVocab({
                'author': request.user,
                'name': title,
                'bot': chat_bot,
                'alterations': output_content
            })

            if alteration_form.is_valid():
                alteration_form.save(commit=True)
                user_profile.nr_vocabs += 1
                user_profile.save()
            else:
                error = VocabErrors.unknown_error
        else:
            prev_alteration.alterations = output_content
            prev_alteration.save()

    return HttpResponse(error._value_, content_type='text/plain')


@ajaxRequest
@checkPost
def talkToServer(request):
    user_chat_data = request.POST.copy()
    user_chat_data['user_id'] = request.user.id
    sentence_form = forms.ChatInput(user_chat_data)

    out_line = getOutputChatLineForRequest(sentence_form, BOT_FACTORY)
    json_response = json.dumps(out_line)
    return HttpResponse(json_response, content_type="application/json")
