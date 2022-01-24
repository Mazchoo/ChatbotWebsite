
let reverseString = function(str) {
    return str.split("").reverse().join("");
}


let replaceExpression = function(str, expression, replacement) {
    return str.replace(expression, () => replacement);
}


let getIndexInArr = function(arr, obj) {
    for(i=0; i<arr.length; i++) {
        if (arr[i] === obj) {
            return i;
        }
    }
    return;
}


let deleteParentDiv = function(obj) {
    if (obj === undefined || obj.parentNode === undefined || obj.parentNode.parentNode === undefined) {return;}
    obj.parentNode.parentNode.removeChild(obj.parentNode);
}


 let removeItem = function(obj) {
    if (obj === undefined || obj.parentNode === undefined) {return;}
    obj.parentNode.removeChild(obj);
}


 let componentFromTemplate = function(template, componentType, className) {
    let obj = document.createElement(componentType);
    obj.innerHTML = template;
    if (className !== undefined) {
        obj.className = className;
    }
    return obj;
}


let changeTooltipTextFromInput = function(e, idTag, suffix) {
    $(idTag)[0].innerHTML = e.target.value + suffix;
}


let reorderOneDivFromAnother = function(sourceTag, targetTag) {
    targetDiv  = $(targetTag)[0];
    sourceObjs = $(sourceTag);

    for (let i = 0; i < sourceObjs.length; i++) {
        targetItem = $(sourceObjs[i].getAttribute('name'))[0];
        targetDiv.appendChild(targetItem);
    }
}


let refreshScrollSpies = function() {
    var dataSpyList = [].slice.call(document.querySelectorAll('[data-bs-spy="scroll"]'))
    dataSpyList.forEach(function (dataSpyEl) {
        bootstrap.ScrollSpy.getInstance(dataSpyEl).refresh()
    })
}
