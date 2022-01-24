
let deleteAlteration = function(e) {
    let obj = $(e.target.getAttribute('name'))[0];
    if (obj === undefined) {return;}
    removeItem(obj);
    vocabLength -= 1;
}


let checkNewWord = function(baseWord, newWord) {
    if (newWord.length > maxWordSize) {
         showMessageSimpleModal('Word Too Long', `New words cannot be more than ${maxWordSize} in length.`);
         return false;
    } else if (vocabLength + 1 > maxVocabLength) {
         showMessageSimpleModal('Vocab Too Long', `Vocab cannot be more than ${maxVocabLength} words.`);
         return false;
    } else if (newWord == baseWord) {
         showMessageSimpleModal('Invalid Word', 'New word should be different to old word.');
         return false;
    } else if (newWord.length == 0) {
         showMessageSimpleModal('Invalid Word', 'New word should be non-empty.');
         return false;
    } else if (newWord.match('^[a-zA-Z0-9\-]+$') === null) {
         showMessageSimpleModal('Invalid Word', 'New words should not contain spaces or punctuation (apart from dashes).');
         return false;
    } else if ($('#' + baseWord + '_' + newWord).length > 0) {
         showMessageSimpleModal('Invalid Word', 'This alteration already exists.');
         return false;
    }
    return true;
}


let addAlteration = function(baseWord, newWord) {
    if (!checkNewWord(baseWord, newWord)) { return; }

    let alterationHTML = alterationTemplate.slice();
    alterationHTML = replaceExpression(alterationHTML, /%{baseWord}/g, baseWord);
    alterationHTML = replaceExpression(alterationHTML, /%{changedWord}/g, newWord);

    obj = componentFromTemplate(alterationHTML, "li");
    if (obj === undefined) {return;}
    if (obj.children[0] === undefined) {return;}
    
    obj = obj.children[0];
    $('#vocab-alterations')[0].appendChild(obj);
    $('#' + baseWord + '-' + newWord + '-btn').click(deleteAlteration);
    vocabLength += 1;
}


let chooseAlteration = function(e) {
    showAlterationModal(e.target.innerText.trim(), addAlteration);
}


let generateVocabAlterations = function(saveContent) {
    if (saveContent === null) {return;}
    let saveData = {};

    for (i = 0; i < saveContent.length; ++i) {
         let saveString = saveContent[i].id;
         let saveWords = saveString.split("_");

         if (saveWords.length > 1) {
              saveData[saveWords[0]] = saveWords[1];
         }
    }

    return saveData;
}


let saveAlterationContent = function(saveData, title, existsOk) {
    if (saveData === null || title === null || existsOk === null) {return;}

    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
         type: 'POST',
         url: saveUrl,
         data: {"content": saveData, 
                "csrfmiddlewaretoken": csrftoken, 
                "chatbot": chatbotName,
                "existsOk": existsOk, 
                "title": title
         },
         success: function(response) {
               $('#save-alterations').removeClass('disabled');
               vocabName = title;
               showMessageSimpleModal('Vocabulary Save Status', response);
         },
         error: function(jqXhr, textStatus, errorThrown){
              showMessageSimpleModal('Unknown Error', 'Vocab Alteration could not be saved.');
         }
    })
}


let addVocabContentToSaveData = function(title, existsOk) {
    let saveContent = $('#vocab-alterations')[0].children;
    let saveData = generateVocabAlterations(saveContent);
    saveAlterationContent(saveData, title, existsOk);
}


let addTitleCallback = function(title) {
    if (title === null) {return;}
    
    if (title.length > maxTitleLength) {
          showMessageSimpleModal(
              'Title Too Long', 
              `The title cannot be more than ${maxTitleLength} characters.`
          );
    } else if (title.length == 0) {
          showMessageSimpleModal(
          'Title is Empty', 
              'Title should be atleast one character in length.'
          );
    } else {
         addVocabContentToSaveData(title, false);
    }
}


let saveAlteration = function() {
    showInputModal('Save Vocab', 'Give a name to the alterations', addTitleCallback);
}


let intializeVocabContent = function(loadedContent) {
     if (loadedContent === null) { 
          $('#save-alterations').addClass('disabled');
          return;
     }

     for([baseWord, newWord] of Object.entries(loadedContent)) {
          addAlteration(baseWord, newWord);
     }
}


let saveExistingVocabContent = function() {
     if (vocabName === null || vocabName === undefined) { return; }
     addVocabContentToSaveData(vocabName, true);
}
