import fastai.text.learner
import fastai.text.models.awdlstm

from main.corpusModels.corpusGenerator import *
from main.common import *
from main.corpusModels.processOutputLine import validPublicWord
from main.globalParams import *

import dill
from os.path import exists
from os import getcwd
import pdb


class CorpusGeneratorFactory:
    def __init__(self, model_files):
        self.corpus_generators = {}
        self.compileModels(model_files)

    def compileModels(self, model_files: dict):
        cwd = getcwd() + '/main/corpusModels/models/'

        for learn_path, vocab_path in model_files.items():

            if exists(cwd + learn_path + '.pth') and exists(cwd + vocab_path):
                corpus = dill.load(open(cwd + vocab_path, 'rb'))
                mutable_vocab = [w for w in corpus.vocab if validPublicWord(w)]

                learn = fastai.text.learner.language_model_learner(
                    corpus, fastai.text.models.awdlstm.AWD_LSTM
                )

                learn.load(cwd + learn_path)
                learn.model = learn.model.eval()
                line = learn.predict('Hello #', 2, temperature=0.5)
                Logger.info(learn, 'loaded correctly =>', line)

                generator = CorpusGenerator(learn, mutable_vocab, learn_path)
            else:
                Logger.warn('Learner files do not exist.')
                generator = None

            self.corpus_generators[learn_path] = generator

    def createPredictor(self, learn_name: str):
        if learn_name in self.corpus_generators.keys():
            return self.corpus_generators[learn_name]

    def __iter__(self):
        for key, val in self.corpus_generators.items():
            yield key, val

    def __len__(self):
        return len(self.corpus_generators)


if __name__ == '__main__':
    model_files = {
        'movie_dialog': 'movie_dialog_dlm.pickle',
        'lord_of_ring': 'lord_of_ring_dlm.pickle',
    }
    corpus_factory = CorpusGeneratorFactory(model_files)
    corp_gen = corpus_factory.createPredictor('movie_dialog')
    out_str = corp_gen.predictSentence('He will not get out of here alive.')
    print(out_str)
