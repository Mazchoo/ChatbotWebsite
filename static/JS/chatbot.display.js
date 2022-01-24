
let resetMCE = function(div) {
     // MCE bugs out after divs get moved around
     let divName = div.children[0].getAttribute('name');
     if (divName === 'chapter-heading') {return;}
     tinymce.get(divName).remove();
     tinymce.init({selector:'#' + divName});
}


let getContentType = function(key) {
     let contentType = key.match(/([a-zA-Z]+)/g);
     return contentType[0]
}


function downloadFile(filename, text) {
     var element = document.createElement('a');
     element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
     element.setAttribute('download', filename);

     element.style.display = 'none';
     document.body.appendChild(element);

     element.click();

     document.body.removeChild(element);
}


let changeTemperatureTooltip = function(e) {
     changeTooltipTextFromInput(e, "#temperature-tooltip", "%");
}


let addNewChapterToContents = function(contentInd) {
     let classTemplate = replaceExpression(
          'list-group-item list-group-item-action remove-action-item chapter-region-%{contentInd}', 
          /%{contentInd}/g, contentInd
     )
     let link = componentFromTemplate('New Chapter', 'a', classTemplate);
     link.href = '#' + chapterType + String(contentInd);
     link.id = 'contents' + String(contentInd);
     $('#contents-chapters')[0].appendChild(link);
}


let generateParagraphTemplate = function(contentInd) {
     return replaceExpression(paragraphTemplate, /%{contentInd}/g, contentInd);
}


let generateChapterTemplate = function(contentInd) {
     return replaceExpression(chapterTemplate, /%{contentInd}/g, contentInd);
}


let moveItemUp = function(e) {
     let parentDiv = $(e.target.getAttribute('name'))[0];
     if  (parentDiv === undefined) {return;}
     parentDiv = parentDiv.parentNode;
     let editAreaList = $('#edit-area')[0];
     let objInd = getIndexInArr(editAreaList.children, parentDiv)

     if (objInd === undefined || objInd == 0) {return;}

     editAreaList.insertBefore(parentDiv, editAreaList.children[objInd-1]);
     resetMCE(parentDiv);
     resetMCE(editAreaList.children[objInd]);
}


let moveItemDown = function(e) {
     let parentDiv = $(e.target.getAttribute('name'))[0];
     if  (parentDiv === undefined) {return;}
     parentDiv = parentDiv.parentNode;
     let editAreaList = $('#edit-area')[0];
     let objInd = getIndexInArr(editAreaList.children, parentDiv)

     if (objInd === undefined || objInd == editAreaList.children.length-1) {return;}

     editAreaList.insertBefore(editAreaList.children[objInd+1], parentDiv);
     resetMCE(parentDiv);
     resetMCE(editAreaList.children[objInd]);
}


let talkToBot = function(e) {
    let paragraph = $(e.target.getAttribute('name'))[0];
    if (paragraph === undefined) { return; }
    paragraph = paragraph.contentDocument.body;

     if (paragraph.innerHTML.trim().length > maxParagraphLength) {
          showMessageSimpleModal('Paragraph Too Long', 
          `The contents of a paragraph (including styling) should not be more than ${maxParagraphLength}.`);
     }

    let inputLine = paragraph.innerText;
    inputLine = getLastSentence(inputLine);

    let chatbotName = $('#model-select')[0].value;
    let vocabId = $('#vocab-select')[0].value;
    let temperature = $('#temperature-slider')[0].value;

    let successCallback = function(response) {
          paragraph.innerHTML += (' <p>' + response + '</p>');
    }

    const [lineIsValid, errorMessage] = verifyInput(inputLine);
     if (lineIsValid) {
          submitChatbotRequest(inputLine, chatbotName, temperature, successCallback, talkUrl, vocabId);
     } else {
          showMessageSimpleModal("Invalid Paragraph", errorMessage);
     }
}


let deleteParagraph = function(e) {
     let paragraphDivs = $(e.target.getAttribute('name'));
     let deleteParagraphs = function() {
          deleteParentDiv(paragraphDivs[0]);
          nrParagraphs -= 1;
     }

    let paragraphText = paragraphDivs.find(".tox-edit-area__iframe")[0];
     if (paragraphText !== undefined) {
          paragraphContent = paragraphText.contentDocument.body;
          if (paragraphContent.innerText.trim().length === 0) {
               deleteParagraphs();
               return;
          }
     }

     showCallbackModal(
          'Are you sure?', 
          'Are you sure you want to delete this non-empty paragraph? There is no way to undo this.',
          'Confirm', 
          deleteParagraphs
     )
}


let deleteChapter = function(e) {
     let chapterDivs = $(e.target.getAttribute('name'));
     let chapterParent = chapterDivs[chapterDivs.length - 1].parentNode;

     for (let i = 0; i < chapterDivs.length; i++) {
          removeItem(chapterDivs[i]);
     }
     removeItem(chapterParent);

     nrChapters -= 1;
     if (nrChapters === 0) {
          $('#contents-chapters').addClass('d-none');
     }
}


let checkNrParagraphs = function() {
    if (nrParagraphs >= maxNrParagraphs) {
          showMessageSimpleModal(`Too Many Paragraphs!`,
              `The maximum number of paragraphs is capped ${maxNrParagraphs}. 
              Delete some paragraphs in order to continue adding them.`);
          return false;
    }

    contentInd += 1;
    nrParagraphs += 1;

    return true;
}


let checkNrChapters = function() {
     if (nrChapters >= maxNrChapters) {
          showMessageSimpleModal(`Too Many Chapters!`,
               `The maximum number of chapters is capped ${maxNrChapters}. 
               Delete some chapters in order to continue adding them.`);
          return false;
     }

     contentInd += 1;
     nrChapters += 1;

     if (nrChapters > 0) {
          $('#contents-chapters').removeClass('d-none');
     }
     return true;
}


let createNewParagraph = function() {
     if (!checkNrParagraphs()) {return;}
     return componentFromTemplate(generateParagraphTemplate(contentInd), 'div', 'row mt-3');
}


let insertNewObjectIntoEditArea = function(e, newFunc, initFunc) {
     let parentDiv = $(e.target.getAttribute('name'))[0];
     if (parentDiv === undefined) {return;}
     let div = newFunc();
     if (div === undefined) {return;}
     parentDiv = parentDiv.parentNode;

     $('#edit-area')[0].insertBefore(div, parentDiv)
     initFunc(String(contentInd));
     return div;
}


let initializeNewParagraph = function(lastestId) {
     tinymce.init({selector:'#' + paragraphType + lastestId});
     $('#generate-content' + lastestId).click(talkToBot);
     $('#delete-content' + lastestId).click(deleteParagraph);
     $('#insert-paragraph' + lastestId).click(insertNewParagraph);
     $('#insert-chapter' + lastestId).click(insertNewChapter);
     $('#move-content-up' + lastestId).click(moveItemUp);
     $('#move-content-down' + lastestId).click(moveItemDown);
}


let insertNewParagraph = function(e) {
     return insertNewObjectIntoEditArea(e, createNewParagraph, initializeNewParagraph);
}


let appendParagraphToList = function(textContent) {
     let div = createNewParagraph();
     if (div === undefined) {return;}

     $('#edit-area')[0].appendChild(div);
     tinymce.init({selector:'#' + paragraphType + String(contentInd), mode : "none"});
     initializeNewParagraph(String(contentInd));

     return div;
}


let editParagraphContent = function(updateInd, textContent) {
     if (updateInd === undefined || textContent === undefined) { return false; }
     let contentDiv = $('#' + paragraphType + String(updateInd) + '_ifr')[0];
     let success = false;

     if (contentDiv !== undefined) {
          contentDiv.contentDocument.body.innerHTML = textContent;
          success = true;
     }
     return success;
}


let editParagraphWhenInitialised = function(updateInd, textContent, counter) {
     if (counter <= 0 || updateInd === undefined || textContent === undefined) { return false; }

     if (!editParagraphContent(updateInd, textContent)) {
          counter--;
          setTimeout(editParagraphWhenInitialised, 1000, updateInd, textContent, counter);
     }
}


let editChapterContent = function(updateInd, textContent) {
     if (updateInd === undefined || textContent === undefined) { return false; }

     let chapterDiv = $('#' + chapterType + String(updateInd))[0];
     if (chapterDiv !== undefined) {
          chapterDiv.innerHTML = textContent;
     }

     let contentDiv = $('#contents' + String(updateInd))[0];
     if (contentDiv !== undefined) {
          contentDiv.innerHTML = textContent;
     }
}


let createNewChapter = function() {
     if (!checkNrChapters()) {return;}
     return componentFromTemplate(generateChapterTemplate(contentInd), 'div', 'row mt-3');     
}


let changeChapterName = function(e) {
     let chapterName = e.target.innerText;
     if (chapterName.length > maxChapterLength) {
          showMessageSimpleModal('Chapter Name Too Long', 
          `Chapter has length that is too long. It must be below ${maxChapterLength} characters. It cannot be saved like this!`);
     }
     let chapterTag = e.target.getAttribute('name');
     $(chapterTag)[0].innerText = chapterName;
}


let initializeNewChapter = function(latestId) {
     $('#delete-content' + latestId).click(deleteChapter);
     addNewChapterToContents(contentInd);
     $('#' + chapterType + latestId).blur(changeChapterName);
     refreshScrollSpies();
}


let insertNewChapter = function(e) {
     let chapter = insertNewObjectIntoEditArea(e, createNewChapter, initializeNewChapter);
     reorderOneDivFromAnother('.chapter-name', '#contents-chapters');
     return chapter;
}


let appendChapterToList = function() {
     let div = createNewChapter();
     if (div === undefined) {return;}

     $('#edit-area')[0].appendChild(div);
     initializeNewChapter(String(contentInd));

     return div;
}


let checkParagraphLength = function(textContent, maxParagraphLength, currentLength, maxTotalLength) {
     if (textContent.length > maxParagraphLength) {
          let contentIndex = contentId.match(/\d+/)[0];
          $(".paragraph-region-" + String(contentIndex) + " form button").css("color", "red");

          showMessageSimpleModal('Paragraph Too Long', 
          `Paragraph has contents that is too long to save. The Invalid paragraph has been highlighted red.`);
          return false;
     }

     if (currentLength + textContent.length > maxTotalLength) {
          showMessageSimpleModal('Total Content Too Long', 
          `Total story including chapters, paragraphs and styling is limited to ${maxTotalLength} characters.`);
          return false;
     }

     return true;
}


let checkChapterLength = function(textContent, maxChapterLength, currentLength, maxTotalLength, contentId) {
     if (textContent.length > maxChapterLength) {
          let contentIndex = contentId.match(/\d+/)[0];
          $(".chapter-region-" + String(contentIndex) + " h4").css("color", "red");

          showMessageSimpleModal('Chapter Too Long', 
          `Chapter has contents that is too long to save. The Invalid chapter has been highlighted red.`);
          return false;
     }
     
     if (currentLength + textContent.length > maxTotalLength) {
          showMessageSimpleModal('Total Content Too Long', 
          `Total story including chapters, paragraphs and styling is limited to ${maxTotalLength} characters.`);
          return false;
     }

     return true;
}


let generateSaveChatlog = function(saveContent, title) {
     if (saveContent === null || title === null) {return;}
     let currentLength = 0;
     let saveData = {};
     saveData[titleTag + "0"] = title;

     for (let i = 0; i < saveContent.length; i++) {
          let content = saveContent[i];
          let contentId = content.id;

          if (content.classList.contains("talk")) {
               let textContent = $('#' + contentId + '_ifr')[0].contentDocument.body.innerHTML;

               if (checkParagraphLength(textContent, maxFinalParagraphLen, currentLength, maxTotalLength, contentId)) {
                    saveData[contentId] = textContent;
                    currentLength += textContent.length;
               } else {
                    return;
               }
          } else if (content.classList.contains("chapter-name")) {
               let textContent = content.innerText;

               if (checkChapterLength(textContent, maxChapterLength, currentLength, maxTotalLength, contentId)) {
                    saveData[contentId] = textContent;
                    currentLength += textContent.length;
               } else {
                    return;
               }
          } else {
               console.log("Unrecognised save content");
               return;
          }
     }

     return saveData;
} 


let saveChatlogToDatabase = function(saveData) {
     if (saveData === null || saveData[titleTag + "0"] === undefined) {return;}
     let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

     $.ajax({
          type: 'POST',
          url: saveUrl,
          data: {"content" : saveData, "csrfmiddlewaretoken": csrftoken},
          success: function(response) {
               showMessageSimpleModal('Story Save Status', response);
               $('.save-story').removeClass('disabled');
               storyName = saveData[titleTag + "0"];
          },
          error: function(_jqXhr, _textStatus, _errorThrown){
               showMessageSimpleModal('Unknown Error', 'Content could not be saved.');
          }
     })
}


let getSaveData = function(title) {
     let saveContent = $('.save-content');
     return generateSaveChatlog(saveContent, title);
}


let generateSaveDataNewStory = function(title) {
     let saveData = getSaveData(title);
     saveData['existsOk0'] = 'False';
     saveChatlogToDatabase(saveData);
}


let generateSaveDataNamedStory = function(title) {
     let saveData = getSaveData(title);
     saveData['existsOk0'] = 'True';
     saveChatlogToDatabase(saveData);
}


let insertNewLinesAndHeaders = function(saveData) {
     output = ["<style> body {margin-right: 10%; margin-left: 10%;} </style>"];
     for (var key in saveData) {
          let contentType = getContentType(key);
          if (contentType == titleTag) {
               output.push("<br><h1>" + saveData[key] + "</h1><br>");
          } else if (contentType == chapterType) {
               output.push("<h2>" + saveData[key] + "</h2><br>");
          } else if (contentType == paragraphType) {
               output.push(saveData[key] + "<br>");
          }
     }
     return output.join(" ");
}


let generateSaveDataForDownload = function(title) {
     if (title === null) {return;}
     let saveData = getSaveData(title);
     let downloadString = insertNewLinesAndHeaders(saveData);
     downloadFile(title + ".html", downloadString);
}


let downloadStory = function() {
     showInputModal('Download Story', 'What is the name of your story?', generateSaveDataForDownload);
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
          generateSaveDataNewStory(title);
     }
}


let saveChatLog = function() {
     showInputModal('Save Story', 'What is the title of your story?', addTitleCallback);
}


let createBlankStory = function() {
     appendChapterToList();
     appendParagraphToList();
}


let loadChapterContent = function(textContent) {
     appendChapterToList();
     editChapterContent(contentInd, textContent);
}


let loadParagraphContent = function(textContent) {
     appendParagraphToList();
     editParagraphWhenInitialised(contentInd, textContent, maximumChangeAttempts);
}


let parseLoadedStoryContent = function(key, textContent) {
     let contentType = getContentType(key);

     if (contentType !== undefined) {
          if (contentType === chapterType) {
               loadChapterContent(textContent);

          } else if (contentType === paragraphType) {
               loadParagraphContent(textContent);

          }
     }
}

let intializeStoryContent = function(loadedContent) {
     if (loadedContent === null) {
          createBlankStory();
          $('.save-story').addClass('disabled');
     } else {
          for([key, textContent] of Object.entries(loadedContent)) {
               parseLoadedStoryContent(key, textContent);
          }
     }
}


let saveNamedChatlog = function() {
     if (storyName === null || storyName === undefined) { return;}
     generateSaveDataNamedStory(storyName);
}


let updateVocabOptions = function() {
     let botOptions = $('#model-select')[0].options;
     let botSelection = botOptions[botOptions.selectedIndex];
     let botId = botSelection.getAttribute('name');

     let vocabOptions = $('#vocab-select')[0].options;
     for (i = 1; i < vocabOptions.length; ++i) {
          let option = vocabOptions[i];
          let vocabBot = option.getAttribute('name');
          if (vocabBot == botId) {
               $('#' + option.id).show();
          } else {
               $('#' + option.id).hide();
          }
     }
     $('#vocab-select').val(-1);
}
