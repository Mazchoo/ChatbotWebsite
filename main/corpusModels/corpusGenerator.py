
from main.globalParams import *


class CorpusGenerator:

    def __init__(self, predictor, vocab: list, name: str):
        self.predictor = predictor  # fastai learner
        self.vocab = vocab
        self.name = name

    def predictSentence(self, last_sentence: str='', temperature: float=0.5, **kwargs):
        if last_sentence is None:
            return ''

        last_sentence += ' #'
        out_str = self.predictor.predict(
            last_sentence, MAX_OUTPUT_SENTENCE_LENGTH, temperature=temperature
        )
        self.predictor.model.reset()
        return out_str

    def __len__(self):
        return len(self.vocab)

    def __str__(self):
        return self.name
