// show next poll page
function changePage(nextOrPrevious) {
    if (event){
        event.preventDefault()
    }
    let allPages = document.querySelectorAll('.POLL-page');
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
    nextPageNr = nextPageNr.toString()
    let nextPage = document.querySelector(`[data-pagenr='${nextPageNr}']`)
    nextPage.classList.remove("BASE-hide")
}

function checkIfPollIsOpen(projectId){
    event.preventDefault()
    // Create the JSON object
    let data = {
        project: projectId
    };
    // Send the data to poll views check_if_poll_open
    fetch("/poll/check_if_poll_open/check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(responseData => {
            if (responseData.status === 'success'){
                submitPollAnswers(projectId) //submit answers if poll is open
            } else {
                let submissionStatus = document.getElementById('POLL-submission-status')
                submissionStatus.textContent = "Unfortunately the poll is closed and your answers could not be submitted."
                changePage('next')
            }
        })
        .catch(error => {
            console.log(error);
        });
}

// submit answers from poll
function submitPollAnswers(projectId){
    // Create an array to store the answers
    let answers = [];

    // Iterate over each question and gather the answers
    let questions = document.querySelectorAll('[data-question]');
    questions.forEach(function (question) {
        let answer = {};
        if (question.type === "text") {
            answer.question = question.dataset.question;
            answer.answer = question.value;
            answer.type = question.dataset.answer;
            answers.push(answer);
        } else if (question.type === "radio" && question.checked) {
            answer.question = question.dataset.question;
            answer.answer = question.value;
            answer.type = question.dataset.answer;
            answers.push(answer);
        }
    });
    // Create the JSON object
    let data = {
        project: projectId,
        answers: answers
    };
    let username = document.getElementById('POLL-username')
    if (username) {
        data.username = username.value;
    }
    // console.log(data)
    // Send the data to poll views get_answers
    fetch("/poll/get_answers/answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            //console.log(response);
            changePage('next')
        })
        .catch(error => {
            console.log(error);
        });
}

//check poll password
function poll_password_check(projectId){
    event.preventDefault()
    //get password and CSRF token from form
    let givenPassword = document.getElementById('projectpassword').value;
    let token = document.getElementById('POLL-token').dataset.token;
    //get wrong password message
    let wrongPwMsg = document.getElementById('POLL-wrong-pw')
    //Create the JSON object
    let data = {
        project: projectId,
        password: givenPassword
    };

    // Send the data to dashboard get_answers
    fetch("/poll/check_poll_password/password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(responseData => {
            if (responseData.status === 'success') {
                //console.log('Password verification successful');
                //if wrong password message shown, hide again
                changePage('next')
                wrongPwMsg.classList.add("BASE-hide")
            } else {
                //console.log('Password verification failed');
                // Show an error message 
                wrongPwMsg.classList.remove("BASE-hide")
            }
        })
        .catch(error => {
            console.log(error);
        });
}