# Test format  'function {name} _ {given} _ {expects} _ test'
from main.testLib.TestCommon import *
from main.htmlCleaner.RemoveHTMLTags import *


def removeAllTags_emptyString_emptyString_test():
    # Act & Assert
    assert(removeAllTags('') == '')


def removeAllTags_htmlTags_removesTags_test():
    # Act & Assert
    assert(removeAllTags('<script>thing</script>') == 'thing')


def removeAllTags_unfinishedTag_noEffect_test():
    # Act & Assert
    assert(removeAllTags('<script') == '<script')


def removeAllTags_nestedHtmlWithScriptTag_scriptTag_test():
    # Act & Assert
    assert(removeAllTags('<script<p>>The') == 'The')


def removeAllTags_nestedHtmlTag_removesInnerTag_test():
    # Act & Assert
    assert(removeAllTags('<p<p>>The') == '<p>The')


def removeScriptTag_emptyString_emptyString_test():
    # Act & Assert
    assert(removeScriptTag('') == '')


def removeScriptTag_scriptTags_removesTag_test():
    # Act & Assert
    assert(removeScriptTag('<script>SillyCode</script>Stuff') == 'Stuff')


def removeScriptTag_embeddedTags_removesTag_test():
    # Act & Assert
    assert(removeScriptTag('<Script<p>>SillyCode</p></scripT>Stuff') == 'Stuff')


def removeScriptTag_incompleteScriptTags_removesCompleteTag_test():
    # Act & Assert
    assert(removeScriptTag('<scrIpt></sCriPt') == '</sCriPt')


def removeSquareBrackets_emptyString_emptyString_test():
    # Act & Assert
    assert(removeSquareBrackets('') == '')


def removeSquareBrackets_squareBrackets_removesBrackets_test():
    # Act & Assert
    assert(removeSquareBrackets('  [The]  ') == 'The')


def removeSquareBrackets_incompleteSquareBrackets_removesBrackets_test():
    # Act & Assert
    assert(removeSquareBrackets('  [The') == 'The')
    assert(removeSquareBrackets('The]  ') == 'The')


def removeHTMLTag_emptyString_emptyString_test():
    # Act & Assert
    assert(removeHTMLTag('') == '')


def removeHTMLTag_htmlTag_removesTag_test():
    # Act & Assert
    assert(removeHTMLTag('<htMl></hTml>') == '')


def getParagraphTypeIndex_emptyString_emptyList_test():
    # Act & Assert
    assert(getParagraphTypeIndex('') == [])


def getParagraphTypeIndex_sillyString_emptyList_test():
    # Act & Assert
    assert(getParagraphTypeIndex('Cheese[]') == [])


def getParagraphTypeIndex_contentString_contentStringAndIndex_test():
    # Act & Assert
    assert(getParagraphTypeIndex('[chapter1]') == [('chapter', '1')])


def checkValidUserWord_emptyString_False_test():
    # Act & Assert
    assert(not checkValidUserWord(''))


def checkValidUserWord_word_True_test():
    # Act & Assert
    assert(checkValidUserWord('Cheese3'))


def checkValidUserWord_punctuation_True_test():
    # Act & Assert
    assert(not checkValidUserWord('::::'))


if __name__ == '__main__':
    runAllTests(locals().copy())
