// *****************MULTIPLE***************************
// Hiding/unhiding elements in modals add project and add question
// Accepts two parameters: the first is the id of the element that should be hidden/unhidden
// the second is an optional parameter: the targeted checkbox. If none is given, the event target will be used
function hideUnhideIfChecked(el_id, theCheckbox = event.target) {
    let theElement = document.querySelector(`#${el_id}`);
    // let theCheckbox = event.target;
    if (theCheckbox.checked){
        theElement.classList.remove("BASE-hide");
    } else {
        theElement.classList.add("BASE-hide");
    }
}
//function to reload the page, used upon closing add_question to reset changes done while edditing question
function reloadPage() {
    location.reload()
}

//function that opens and closes poll
// function accepts two parameters: the project id and either the string 'open' or 'close'
function openOrClosePoll(projectId, openOrClose){
    // event.preventDefault()
    fetch(`/dashboard/${openOrClose}_poll/${projectId}`)
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            reloadPage();
        })
        .catch (error => console.error(error));
}

//function that checks whether a browser tab's visibility changed
//if user goes to another tab, than returns to the project, the page should be reloaded
//purpose is to detect poll status, since user is re-directed when presenting
// This function was written by Andrea Viviani and is available at: https://stackoverflow.com/questions/64659511/refresh-page-when-active-tab
document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
        console.log("Browser tab is hidden")
    } else {
        console.log("Browser tab is visible")
        location.reload();
    }
});

// *****************MODAL ADD PROJECT***************************
// editing projects
function editProjectData(projectId) {
    event.preventDefault()
    // change modal title and form action
    document.querySelector('#DASHBOARD-P-modal-title').textContent = "Edit Project"
    document.querySelector('#DASHBOARD-P-edit-form').action = `/dashboard/edit_project/${projectId}`
    // get the data information
    fetch(`/dashboard/edit_project/${projectId}`)
        .then(response => response.json())
        .then(data => {
            let projectData = JSON.parse(data.project);
            // console.log(projectData)
            // use the data information to populate the modal:
            document.querySelector('[name="projectname"]').value = projectData[0].fields.name;
            if (projectData[0].fields.username_requirement === true) {
                // here I changed the switch altogether because .checked = true would not
                // visually turn the switch on, and changing the attibute did not work either
                let theSwitchParentU = document.querySelector('#DASHBOARD-P-SwitchParentUsername')
                theSwitchParentU.removeChild(theSwitchParentU.lastElementChild)
                let newSwitchU = document.createElement('div')
                newSwitchU.innerHTML = `<input class="form-check-input" type="checkbox" id="flexSwitchUsername" name="usernamenabled" checked>
                        <label class="form-check-label" for="flexSwitchUsername" class="BASE-modal-label">Set username</label>`;
                theSwitchParentU.replaceChild(newSwitchU, theSwitchParentU.lastElementChild)
            }
            if (projectData[0].fields.pw_requirement === true) {
                // here I changed the switch altogether because .checked = true would not
                // visually turn the switch on, and changing the attibute did not work either
                let theSwitchParent = document.querySelector('#DASHBOARD-P-SwitchParent')
                theSwitchParent.removeChild(theSwitchParent.lastElementChild)
                let newSwitch = document.createElement('div')
                newSwitch.innerHTML = `<input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" name="pwenabled" onclick="hideUnhideIfChecked('setProjectPasswordContainer')" checked>
                        <label class="form-check-label" for="flexSwitchCheckDefault" class="BASE-modal-label">Set password</label>`;
                theSwitchParent.replaceChild(newSwitch, theSwitchParent.lastElementChild)
                hideUnhideIfChecked('setProjectPasswordContainer', newSwitch.firstChild)
                document.querySelector('[name="projectpw"]').value = projectData[0].fields.pw
            }
            if (projectData[0].fields.show_answers === true){
                let theSwitchParentU = document.querySelector('#DASHBOARD-P-SwitchParentAnswer')
                theSwitchParentU.removeChild(theSwitchParentU.lastElementChild)
                let newSwitchU = document.createElement('div')
                newSwitchU.innerHTML = `<input class="form-check-input" type="checkbox" id="flexSwitchAnswer" name="answernabled" checked>
                        <label class="form-check-label" for="flexSwitchAnswer" class="BASE-modal-label">Show answer</label>`;
                theSwitchParentU.replaceChild(newSwitchU, theSwitchParentU.lastElementChild)
            }
            // when a project is editted, close the poll
            document.querySelector('#DASHBOARD-save-edit-prj-btn').addEventListener("click", () => { openOrClosePoll(projectId, 'close') })
            //open the modal
            document.querySelector('#modal_add_project').classList.remove('BASE-hide')
        })
        .catch(error => console.error(error));
}


// *****************MODAL ADD QUESTION***************************
// Checking question type in modal add question
// Accepts two parameters: the first is the selected element's id
// the second is an optional parameter: the targeted checkbox. If none is given, the event target will be used
function checkedQuestionType(el_id, theCheckbox = event.target) {
    //theElement is the parent container
    let theElement = document.querySelector(`#${el_id}`);
    // let theCheckbox = event.target;
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
    // Display correct form elements according to question type
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
// And define options in select answer
function displayMultiChoices(nrChoice = event.target.value){
    let allChoices = document.querySelectorAll('[data-multiChoice]');
    let selectChoiceContainer = document.querySelector("#rightChoice");
    let options = [...selectChoiceContainer.children]
    if (nrChoice == 2) {
        allChoices.forEach(choice => choice.classList.add('BASE-hide'));
        options[2].classList.add('BASE-hide');
        options[3].classList.add('BASE-hide');
        options[4].classList.add('BASE-hide');
    } else if (nrChoice == 3) {
        allChoices.forEach(choice => {
            choice.getAttribute("data-multiChoice") === "3" ? choice.classList.remove('BASE-hide') : choice.classList.add('BASE-hide');
        })
        options[2].classList.remove('BASE-hide');
        options[3].classList.add('BASE-hide');
        options[4].classList.add('BASE-hide');
    } else if (nrChoice == 4) {
        allChoices.forEach(choice => {
            if (choice.getAttribute("data-multiChoice") === "3" || choice.getAttribute("data-multiChoice") === "4") {
                choice.classList.remove('BASE-hide');
            } else {
                choice.classList.add('BASE-hide');
            }
        })
        options[2].classList.remove('BASE-hide');
        options[3].classList.remove('BASE-hide');
        options[4].classList.add('BASE-hide');
    } else {
        allChoices.forEach(choice => choice.classList.remove('BASE-hide'));
        options.forEach(option => option.classList.remove('BASE-hide'))
    }
}

//getting data from the edit_question function for modal add question (adapted to edit question)
function editQuestionData(questionId) {
    event.preventDefault()
    // change modal title and form action
    document.querySelector('#DASHBOARD-Q-modal-title').textContent = "Edit Question";
    document.querySelector('#DASHBOARD-Q-edit-form').action = `/dashboard/edit_question/${questionId}`;
    let theDeleteBtn = document.querySelector('#DASHBOARD-Q-delete');
    theDeleteBtn.href = `/dashboard/delete_question/${questionId}`;
    theDeleteBtn.classList.remove('BASE-hide');
    // get the data information
    fetch(`/dashboard/edit_question/${questionId}`)
        .then(response => response.json())
        .then(data => {
            let questionData = JSON.parse(data.question);
            // use the data information to populate the modal:
            document.querySelector('[name="thequestion"]').value = questionData[0].fields.question;
            let questionType = questionData[0].fields.question_type;
            if (questionType != "Open-ended Question") {
                if (questionType === "Question and Answer") {
                    checkedQuestionType('DASHBOARD-choice-2', document.querySelector('#qanda'));
                    document.querySelector('[name="theanswer"]').value = questionData[0].fields.answer;
                } else {
                    checkedQuestionType('DASHBOARD-choice-3', document.querySelector('#multiplechoice'))
                    document.querySelector('#nrchoices').value = questionData[0].fields.nr_choices;
                    displayMultiChoices(questionData[0].fields.nr_choices)

                    for (let i = 1; i < 6; i++) {
                        document.querySelector(`[name = 'choice${i}']`).value = questionData[0].fields[`option${i}`]
                    }
                    if (questionData[0].fields.correctOptionEnabled === true) {
                        // here I changed the switch altogether because .checked = true would not
                        // visually turn the switch on, and changing the attibute did not work either
                        let theSwitchParent = document.querySelector('#DASHBOARD-Q-SwitchParent')
                        theSwitchParent.removeChild(theSwitchParent.lastElementChild)
                        let newSwitch = document.createElement('div')
                        newSwitch.innerHTML = `<input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" name="choiceAnswerEnabled"
                                role="switch" onclick="hideUnhideIfChecked('choiceAnswer')" checked>
                                <label class="form-check-label" for="flexSwitchCheckDefault" class="BASE-modal-label">Show correct answer</label>`;
                        theSwitchParent.replaceChild(newSwitch, theSwitchParent.lastElementChild)
                        hideUnhideIfChecked('choiceAnswer', newSwitch.firstChild)
                        document.querySelector('#rightChoice').value = questionData[0].fields.correctOption
                    }
                }
            }
            //open the modal
            document.querySelector('#modal_add_question').classList.remove('BASE-hide')
        })
        .catch(error => console.error(error));
}

// *****************DRAG AND DROP QUESTIONS***************************
//Adding event listeners to projects.html where questions can be dragged into position
//This was written with the help of Web Dev Simplified's video available at: https://www.youtube.com/watch?v=jfYWwQrtzzY&t=655s
const questionContainer = document.querySelector('#DASHBOARD-project-question-container')
const questionElements = document.querySelectorAll('.DASHBOARD-project-question-item')

function moveElements(event){
    event.target.classList.add('DASHBOARD-project-question-item-dragging');
}
function stopMoveElement(event) {
    event.target.classList.remove('DASHBOARD-project-question-item-dragging');
    // Show button to save new question order
    const orderBtn = document.querySelector('#BtnSaveQorder');
    orderBtn.classList.remove('BASE-hide')
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
        questionContainer.insertBefore(theEl, afterEl);
    }
}
questionElements.forEach(el => {
    el.addEventListener('dragstart', moveElements)
    el.addEventListener('dragend', stopMoveElement)
})

// After a dragend event the user can save the new question order.
// This function returns an array of arrays for each question, where the first number represents the 
// pk of the question, and the second number represents the new position of the question. 
function getOrderOfQuestions(projectId){
    event.preventDefault()
    let questionsAndPositions = [];
    let allQuestions = [...questionContainer.children];
    allQuestions.forEach(child => {
        let el = [parseInt(child.dataset.questionpk), allQuestions.indexOf(child)]
        questionsAndPositions.push(el)
    })
    fetch(`/dashboard/question_order`, {
        method:'POST',
        body: JSON.stringify({
            body: questionsAndPositions,
        })
    })
    .then(response => {
        console.log(response);
        return response.json();
    })
    .then(result => console.log(result))
    //make sure poll is closed when changes are made
    //when debugging, comment out the next line
    .then(
        openOrClosePoll(projectId, 'close')
    )
}

//*****************DOWNLOAD EXCEL TABLE***************************
//how to convert html table to excel from https://phppot.com/javascript/convert-html-table-excel-javascript/

//in function used for onclick events in project_answers.html
function downloadTableExcel(table_id) {
    event.preventDefault();
    const table = document.getElementById(table_id);
    const rows = table.rows;
    let sourceData = "data:text/csv;charset=utf-8,";

    // Convert the table to a CSV format
    let csv = [];
    for (let i = 0; i < rows.length; i++) {
        let row = [];
        let cells = rows[i].cells;
        for (let j = 0; j < cells.length; j++) {
            let cell = cells[j];
            let cellText = cell.innerText.trim();

            // Remove <br> tags from the cell content (as they cause cells to be split into separate csv cells)
            cellText = cellText.replace(/<br>/g, ' ');

            // Check if the cell contains multiple lines of text
            if (cellText.includes('\n')) {
                cellText = cellText.replace(/\n/g, ' '); // If they do, replace newlines with spaces
            }
            // Remove commas from the cell text
            cellText = cellText.replace(/,/g, '');

            row.push(cellText);
        }
        csv.push(row.join(','));
    }

    let csvContent = csv.join('\n');
    sourceData += csvContent;
    window.location.href = encodeURI(sourceData);
}
