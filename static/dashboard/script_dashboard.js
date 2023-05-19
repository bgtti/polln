// Hiding/unhiding elements in modal add project
function hideUnhideIfChecked(el_id) {
    let theElement = document.querySelector(`#${el_id}`);
    let theCheckbox = event.target;
    if (theCheckbox.checked){
        theElement.classList.remove("BASE-hide");
    } else {
        theElement.classList.add("BASE-hide");
    }
}

// Checking question type in modal add question
function checkedQuestionType(el_id) {
    //theElement is the parent container
    let theElement = document.querySelector(`#${el_id}`);
    let theCheckbox = event.target;
    //Remove styling from other 'checked' containers
    all_containers = document.querySelectorAll('.DASHBOARD-question-choice-container');
    all_containers.forEach(container => {
        if (container.classList.contains('DASHBOARD-question-choice-container-checked')){
            container.classList.remove('DASHBOARD-question-choice-container-checked');
        }
    });
    //Mark all other checkboxes as unchecked
    all_checkboxes = document.querySelectorAll('.DASHBOARD-question-checkbox');
    all_checkboxes.forEach(box => {
        box.checked = false;
    })
    //Mark this checkbox as checked and give styling to parent container
    theCheckbox.checked = true;
    theElement.classList.add("DASHBOARD-question-choice-container-checked");
    //Display correct form elements according to question type
    qAndA = document.querySelector("#DASHBOARD-question-type-qanda-container");
    multipleChoice = document.querySelector("#DASHBOARD-question-type-multiple-choice-container");
    if (el_id === "DASHBOARD-choice-2"){
        qAndA.classList.remove("BASE-hide");
        multipleChoice.classList.add("BASE-hide");
    } else if (el_id === "DASHBOARD-choice-3") {
        qAndA.classList.add("BASE-hide");
        multipleChoice.classList.remove("BASE-hide");
    } else{
        qAndA.classList.add("BASE-hide");
        multipleChoice.classList.add("BASE-hide");
    }
}

// displaying elements accordingly for multi-choice type in modal add question
function displayMultiChoices(event){
    let nrChoice = event.target.value
    let allChoices = document.querySelectorAll('[data-multiChoice]');
    if (nrChoice == 2){
        allChoices.forEach(choice => choice.classList.add('BASE-hide'));
    } else if (nrChoice == 3){
        allChoices.forEach(choice => {
            choice.getAttribute("data-multiChoice") === "3" ? choice.classList.remove('BASE-hide') : choice.classList.add('BASE-hide');
        })
    } else if (nrChoice == 4){
        allChoices.forEach(choice => {
            if (choice.getAttribute("data-multiChoice") === "3" || choice.getAttribute("data-multiChoice") === "4") {
                choice.classList.remove('BASE-hide');
            } else {
                choice.classList.add('BASE-hide');
            }
        })
    } else {
        allChoices.forEach(choice => choice.classList.remove('BASE-hide'));
    }
}

//Adding event listeners to projects.html where questions can be dragged into position
//This was written with the help of Web Dev Simplified's video available at: https://www.youtube.com/watch?v=jfYWwQrtzzY&t=655s
const questionContainer = document.querySelector('#DASHBOARD-project-question-container')
const questionElements = document.querySelectorAll('.DASHBOARD-project-question-item')

function moveElements(event){
    event.target.classList.add('DASHBOARD-project-question-item-dragging');
}
function stopMoveElement(event) {
    event.target.classList.remove('DASHBOARD-project-question-item-dragging');
}
function elementPosition(container, y){
    //getting all draggable elements
    const draggableEls = [...container.querySelectorAll('.DASHBOARD-project-question-item:not(.DASHBOARD-project-question-item-dragging)')];
    //define which element comes after the cursor's position when dragging an element
    return draggableEls.reduce((elBellowCursor, draggableEl)=>{
        //get size of element and its position relative to viewport
        const box = draggableEl.getBoundingClientRect();
        //get center of box
        const offset = y - box.top - box.height/2;
        //negative offsets means the cursor is hovering above an element
        //and the closest element bellow the cursor will have an offset closest to 0
        if (offset < 0 && offset > elBellowCursor.offset){
            return { offset: offset, element: draggableEl }
        } else {
            return elBellowCursor
        }
        //the default offset is a number infinitely lower than any other possible offset
    },{offset: Number.NEGATIVE_INFINITY}).element
}
function positionInContainer(event){
    event.preventDefault();
    //get the element which is bellow the element we want to insert
    const afterEl = elementPosition(event.target, event.clientY)
    //get the element we are currently dragging
    const theEl = document.querySelector('.DASHBOARD-project-question-item-dragging');
    //if element being dragged has no element above it, it goes to the bottom, else, it goes above an element
    if (afterEl == null){
        questionContainer.append(theEl);
    } else {
        questionContainer.insertBefore(theEl, afterEl)
    }
}
questionElements.forEach(el => {
    el.addEventListener('dragstart', moveElements)
    el.addEventListener('dragend', stopMoveElement)
})
//add event listener to container (in template): questionContainer.addEventListener('dragover', positionInContainer(event))

//after an element is dragged, show the option to save the current order of the questions.

//DONT FORGET TO ADD A data-pk dataset to each question of template!!!!!
//Get button 'Save Order' to appear after a dragend event happens
//Send this array to the backend
function getOrderOfQuestions(){
    let questionsAndPositions = [];
    let allQuestions = [...questionContainer.children];
    allQuestions.forEach(child => {
        let el = [parseInt(child.getAttribute['data-pk']), allQuestions.indexOf(child)]
        questionsAndPositions.append(el)
    })
}