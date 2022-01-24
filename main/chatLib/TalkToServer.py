
from main.globalParams import *
from main.corpusModels.processOutputLine import *
from main.corpusModels.vocabReplacer import *

import pdb


def getAlterationForSentence(sentence_data):
    alterations = None
    if 'vocab_alteration' in sentence_data.keys():
        alterations = sentence_data['vocab_alteration'].alterations

    return alterations


def getProcessedChatbotOutput(alterations, corp_gen, sentence_data):
    if alterations:
        sentence_data['last_sentence'] = replaceVocabInput(
            sentence_data['last_sentence'], alterations
        )

    out_line = corp_gen.predictSentence(**sentence_data)

    if alterations:
        out_line = replaceVocabOutput(out_line, alterations)

    return processOutputLine(out_line)


def getOutputChatLineForRequest(sentence_form, corpus_factory):
    if not sentence_form or not sentence_form.is_valid() or not corpus_factory:
        return ''

    bot_name = sentence_form.cleaned_data['chatbot_name']
    corp_gen = corpus_factory.createPredictor(bot_name)

    if corp_gen is None:
        return ''

    sentence_data = sentence_form.cleaned_data
    alterations = getAlterationForSentence(sentence_data)
    return getProcessedChatbotOutput(alterations, corp_gen, sentence_data)
