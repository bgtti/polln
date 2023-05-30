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

// submit answers from poll
function submitPollAnswers(projectId){
    event.preventDefault()
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

    // Send the data to dashboard get_answers
    fetch("/poll/get_answers/answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            //console.log(response);
            // Redirect or show a success message
            changePage('next')
        })
        .catch(error => {
            console.log(error);
            // Show an error message 
        });
}
