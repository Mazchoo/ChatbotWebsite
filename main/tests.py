
from main.testLib.TestCommon import *
from main.common import *
from main.globalParams import *

# Corpus Models Tests
from main.testLib.main.corpusModels.corpusGenerator_test import *
from main.testLib.main.corpusModels.corpusGeneratorFactory_test import *
from main.testLib.main.corpusModels.processOutputLine_test import *
from main.testLib.main.corpusModels.vocabReplacer_test import *

# Chat Lib Test
from main.testLib.main.chatLib.CheckChatlogSaveContent_test import *
from main.testLib.main.chatLib.TalkToServer_test import *
from main.testLib.main.chatLib.CheckVocabSaveContent_test import *

# HTML Cleaner tests
from main.testLib.main.htmlCleaner.RemoveHTMLTags_test import *

# Urls
from main.testLib.main.urls_test import *

# Forms
from main.testLib.main.forms_test import *

# Views
from main.testLib.main.views_test import *

Logger.setLevel(2)
runAllTests(locals().copy())
