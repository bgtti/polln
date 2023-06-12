//load the page on full screen mode 
//The function bellow was taken from W3Schools, available at https://www.w3schools.com/howto/howto_js_fullscreen.asp#:%7E:text=Try%20it%20Yourself%20%C2%BB-,Fullscreen%20Document,-To%20open%20the)

function openFullscreen() {
    event.preventDefault(event);
    let elem = document.querySelector('#PRESENT-presentation')
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen();
    }
    let theBtn = document.querySelector('#PRESENT-page-1-btn')
    console.log(theBtn)
    theBtn.classList.add("BASE-hide")
}

// If user exits full screen mode, show button again
function checkFullscreenClose(){
    if (document.fullscreenElement === null) {
        let theBtn = document.querySelector('#PRESENT-page-1-btn')
        theBtn.classList.remove("BASE-hide")
    }
}
window.addEventListener("fullscreenchange", (event) => {
    checkFullscreenClose();
})

// Show number of votes being casted on presentation page
function showNrVotes(projectId) {
    fetch(`/present/live_vote_count/${projectId}`)
        .then(response => response.json())
        .then(data => {
            const voteCount = data.vote_count;
            // Update the number of votes in the presentation
            const voteDisplay = document.getElementById('PRESENT-display-live-vote');
            voteDisplay.textContent = voteCount;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
// When the page loads, start counting votes received
// Logic based on helpful tutorial: https://www.tutorialspoint.com/How-to-use-setInterval-function-call-in-JavaScript
let votesOnInterval = null;

// start vote count when page is loaded
window.onload = function (){
    let projectId = document.querySelector('#PRESENT-presentation').dataset.presentprojectid
    // set showNrVotes to run on an interval to update the count
    // this function is triggered with an onload event on the template
    votesOnInterval = setInterval(() => {
        showNrVotes(parseInt(projectId));
    }, 2500); // 2.5 seconds in milliseconds
}

// stop vote count update
function stopVoteCount() {
    clearInterval(votesOnInterval);
}

// function that closes the poll to avoid misrepresenting results
function closePoll(projectId) {
    fetch(`/dashboard/close_poll/${projectId}`)
        .then(response => response.json())
        // .then(data => {
        //     console.log(data);
        // })
        .catch(error => console.error(error));
}

// get the answers to display
function getPollResults(projectId) {
    fetch(`/present/deliver_answers/${projectId}`)
        .then(response => response.json())
        .then(data => {
            //console.log(data);
            // get the data objects
            const questionsData = JSON.parse(data.questions);
            const answersData = JSON.parse(data.answers);

            // get an array of questions
            const theQuestions = questionsData.map(question => [question.pk, question.fields.question_type]);

            // for each question in theQuestions, get the answers:
            theQuestions.forEach(question =>{
                // get answers
                const answersToThisQuestion = answersData.filter(answer => answer.fields.question === question[0]);
                // get div where the answers will be presented
                if (question[1] === "Open-ended Question"){
                    let answerPresentation = document.getElementById(`PRESENT-OE-${question[0]}`)
                    //remove any previous child element of parent node:
                    while (answerPresentation.firstChild) {
                        answerPresentation.removeChild(answerPresentation.lastChild);
                    }
                    //create and add new elements
                    let theAnswers = answersToThisQuestion.map(answer => answer.fields.users_answer)
                    let moreThan10Answers = 0;
                    if (theAnswers.length > 10){
                        theAnswers = theAnswers.slice(0, 10);
                        moreThan10Answers = theAnswers.length - 10;
                    } 
                    theAnswers.forEach(ans => {
                        let displayAns = document.createElement('p');
                        displayAns.textContent = ans;
                        answerPresentation.append(displayAns);
                    })
                    if (moreThan10Answers > 0){
                        let displayMoreThan10 = document.createElement('p');
                        displayMoreThan10.classList.add('PRESENT-displayMoreThan10')
                        displayMoreThan10.textContent = `+ ${moreThan10Answers} answers`;
                    }
                } else if (question[1] === "Question and Answer"){
                    let answerPresentation = document.getElementById(`PRESENT-QA-${question[0]}`)
                    //remove any previous child element of parent node:
                    while (answerPresentation.firstChild) {
                        answerPresentation.removeChild(answerPresentation.lastChild);
                    }
                    //create and add new elements
                    let theAnswers = answersToThisQuestion.map(answer => answer.fields.is_correct)
                    let nrCorrectAns = 0
                    for (let correctAns of theAnswers){
                        if (correctAns === 1){
                            nrCorrectAns++;
                        }
                    }
                    let percentCorrect = (nrCorrectAns/theAnswers.length)*100

                    if (!Number.isInteger(percentCorrect)){
                        percentCorrect = percentCorrect.toFixed(1);
                    }
                    let theResultLine1 = document.createElement('p');
                    theResultLine1.textContent = `${percentCorrect}% of the respondents got it right!`;
                    theResultLine1.classList.add('PRESENT-QA-correct-ans')
                    let theResultLine2 = document.createElement('p');
                    theResultLine2.textContent = `That is ${nrCorrectAns} respondents out of ${theAnswers.length}!`;
                    theResultLine2.classList.add('PRESENT-QA-sub')
                    answerPresentation.append(theResultLine1, theResultLine2);
                } else if (question[1] === "Multiple Choice"){
                    // GET VOTES AND OPTIONS
                    let theVotes = answersToThisQuestion.map(vote => vote.fields.users_choice)
                    // reduce array to object (count nums of elements): https://stackoverflow.com/a/66002712/14517941
                    let votesResult = theVotes.reduce((acc, curr) => (acc[curr] = (acc[curr] || 0) + 1, acc), {});
                    // get array of votes for each option
                    let votesResultArray = [votesResult["1"] ??= 0, votesResult["2"] ??= 0];
                    // get the MC options: nullish coalescing assignment (??=) operator https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_assignment
                    let thisQ = questionsData.filter(theQ => theQ.pk === question[0]);
                    thisQ = thisQ[0];
                    let numQs = thisQ.fields.nr_choices;
                    let optionsQ = [thisQ.fields.option1, thisQ.fields.option2] //chart labels
                    if (numQs > 2){
                        if (numQs >= 3){
                            optionsQ.push(thisQ.fields.option3)
                            votesResultArray.push(votesResult["3"] ??= 0)
                        }
                        if (numQs >= 4) {
                            optionsQ.push(thisQ.fields.option4)
                            votesResultArray.push(votesResult["4"] ??= 0)
                        }
                        if (numQs === 5) {
                            optionsQ.push(thisQ.fields.option5)
                            votesResultArray.push(votesResult["5"] ??= 0)
                        }
                    }
                    // GRAPH: using charts js, check https://www.chartjs.org/docs/latest/getting-started/
                    // Plug-in for datalabels: https://chartjs-plugin-datalabels.netlify.app/guide/getting-started.html#integration
                    const ctx = document.getElementById(`PRESENT-chart-${question[0]}`);
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: optionsQ,
                            datasets: [{
                                label: '# of Votes',
                                data: votesResultArray,
                                backgroundColor: '#f9aa33'
                            }]
                        },
                        plugins: [ChartDataLabels],
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            },
                            layout: {
                                padding: 20
                            },
                            plugins:{
                                legend:{
                                    display: false
                                },
                                datalabels: {
                                    anchor: 'end',
                                    align: 'top',
                                    formatter: Math.round,
                                    font: {
                                        weight: 'bold',
                                        size: 12
                                    }
                                }
                            }
                        }
                    });
                    //DISPLAY RESULTS OF MULTIPLE CHOICE
                    let elementToDisplayResults = document.getElementById(`PRESENT-MC-${question[0]}`)
                    //remove any previous child element of parent node:
                    while (elementToDisplayResults.firstChild) {
                        elementToDisplayResults.removeChild(elementToDisplayResults.lastChild);
                    }
                    // Check if there was a correct option
                    let correctOptionEnabled = thisQ.fields.correctOptionEnabled;
                    // if there was a correct option, check how many respondents got it right
                    if (correctOptionEnabled){
                        let theCorrectOption = thisQ.fields.correctOption; //the correct answer
                        let howManyGotItRight = votesResultArray[theCorrectOption-1]; //how many votes on the correct option
                        let percentThatGotRight = (howManyGotItRight / theVotes.length)*100 //representation of right answers in %
                        if (!Number.isInteger(percentThatGotRight)) {
                            percentThatGotRight = percentThatGotRight.toFixed(1);
                        }

                        let theResultsLine1 = document.createElement('p');
                        theResultsLine1.textContent = `Correct answer: ${optionsQ[theCorrectOption - 1]}`;
                        theResultsLine1.classList.add('PRESENT-MC-correct-ans')
                        let theResultsLine2 = document.createElement('p');
                        theResultsLine2.textContent = `${percentThatGotRight}% of the respondents got it right!`;
                        theResultsLine2.classList.add('PRESENT-MC-sub');
                        elementToDisplayResults.append(theResultsLine1, theResultsLine2);
                    } else{
                        // if there was not correct answer, display most voted answer or a tie
                        let optWithMostVotes = Math.max(...votesResultArray) //votes of most voted option
                        let countMostVotedOption = 0 // if the counter is > 1, there was a tie
                        for (let optMostVoted of votesResultArray){
                            if (optMostVoted === optWithMostVotes){
                                countMostVotedOption++;
                            }
                        }
                        if (countMostVotedOption > 1){
                            let theResultsLine1 = document.createElement('p');
                            theResultsLine1.textContent = `There was a tie!`;
                            theResultsLine1.classList.add('PRESENT-MC-sub');
                            elementToDisplayResults.append(theResultsLine1);
                        } else{
                            let indexOfMostVotes = votesResultArray.indexOf(optWithMostVotes) //index of most voted option
                            let winningOption = optionsQ[indexOfMostVotes]; //most voted option
                            let percentOfVotesInWinningOption = (optWithMostVotes / theVotes.length)*100 //in %
                            if (!Number.isInteger(percentOfVotesInWinningOption)) {
                                percentOfVotesInWinningOption = percentOfVotesInWinningOption.toFixed(1);
                            }
                            let theResultsLine1 = document.createElement('p');
                            theResultsLine1.textContent = `${percentOfVotesInWinningOption}% voted ${winningOption}`;
                            theResultsLine1.classList.add('PRESENT-MC-correct-ans');
                            elementToDisplayResults.append(theResultsLine1);
                        }
                    }
                }
            })
        })
        .catch(error => console.error(error));
}

// Change to next or previous page according to user's key press or finger swipe
function changePage(nextOrPrevious){
    let allPages = document.querySelectorAll('.PRESENT-page');
    let currentPage;
    allPages.forEach(page => {
        if (!page.matches('.BASE-hide')) {
            currentPage = parseInt(page.dataset.pagenr)
            page.classList.add('BASE-hide')
        }
    })
    // dont forget to include the logic to check if first and last page to avoid problems
    let nextPageNr;
    if (nextOrPrevious === "next") {
        nextPageNr = currentPage + 1
    } else {
        nextPageNr = currentPage - 1
    }
    if (currentPage === 1){
        let projectId = document.querySelector('#PRESENT-presentation').dataset.presentprojectid
        closePoll(projectId) // close the poll to stop new votes comming in
        stopVoteCount() // stop vote count update when showing the results
        getPollResults(projectId) //get the results
    }
    nextPageNr = nextPageNr.toString()
    let nextPage = document.querySelector(`[data-pagenr='${nextPageNr}']`)
    nextPage.classList.remove("BASE-hide")
}

document.addEventListener("keydown", (event) =>{
    if(event.keyCode === 13){ //Enter key
        changePage("next")
    } else if (event.keyCode === 37){//Left arrow key
        changePage("previous")
    } else if (event.keyCode === 39) {//Right arrow key
        changePage("next")
    } else if (event.keyCode === 8) {//Backspace key
        changePage("previous")
    }
})

// Change page on touch devices by swiping.
// This function was written by Damjan Pavlica and available at https://stackoverflow.com/a/56663695/14517941
let touchstartX = 0
let touchendX = 0

function checkDirection() {
    if (touchendX < touchstartX){//swiped left
        changePage("next")
    } else if (touchendX > touchstartX){//swiped right
        changePage("previous") 
    }
    touchstartX = 0
    touchendX = 0
}

document.addEventListener('touchstart', e => {
    touchstartX = e.changedTouches[0].screenX
})

document.addEventListener('touchend', e => {
    touchendX = e.changedTouches[0].screenX
    checkDirection()
})