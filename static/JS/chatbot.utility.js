const sentenceEnd = new RegExp('[\.\?!]');

let getLastSentence = function(str) {
    let reversedStr = reverseString(str);

    let lastEnd = sentenceEnd.exec(reversedStr);
    if (lastEnd === null) {
      return str;
    }

    reversedStr = reversedStr.substring(lastEnd.index + 1, str.length);
    let penultimateEnd = sentenceEnd.exec(reversedStr);
    if (penultimateEnd === null) {
        return str;
    } else {
        let lastSentenceStart = str.length - penultimateEnd.index - lastEnd.index;
        return str.substring(lastSentenceStart, str.length);
    }
}


let scrollToBottom = function() {
    $('.scrollable-stuff').stop().animate({
        scrollTop: $('.scrollable-stuff')[0].scrollHeight
    }, 800);
}


let scrollToTop = function() {
    $('.scrollable-stuff').stop().animate({
        scrollTop: 0
    }, 800);
}


let verifyInput = function(str) {
    let errorMessage = "NoError";
    let validInput = true;

    if (typeof(str) !== 'string') {
        validInput = false;
        errorMessage = "Unrecognised content entered in the paragraph.";
    } else if (str.trim().length === 0) {
        validInput = false;
        errorMessage = "You must enter a non-empty last sentence in the paragraph before the AI can generate more.";
    } else if (str.length > maxSentenceLength) {
        validInput = false;
        errorMessage = 'A single paragraph is limited to '.concat(String(maxSentenceLength), ' characters.');
    }

    if (validInput === false) {
        $(".talk").addClass('shakey');
    }
    return [validInput, errorMessage];
}


let submitChatbotRequest = function(inputLine, botName, temperature, callback, url, vocabId) {
    if (botName == null || inputLine === null || url === null) {return;}

    $('.loading-spinner').removeClass('invisible');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: 'POST',
        url: url,
        data: {'last_sentence': inputLine,
               'chatbot_name': botName,
               'temperature' : temperature,
               'csrfmiddlewaretoken': csrftoken,
               'vocab_id': vocabId,
        },
        success: callback,
        complete: function(response) {
            $('.loading-spinner').addClass('invisible');
        }
    })
}