//load the page on full screen mode ( function from https://www.w3schools.com/howto/howto_js_fullscreen.asp#:%7E:text=Try%20it%20Yourself%20%C2%BB-,Fullscreen%20Document,-To%20open%20the)

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

// if user exits full screen mode, show button again
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

// show next page if user presses 'enter'
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
    }
    nextPageNr = nextPageNr.toString()
    let nextPage = document.querySelector(`[data-pagenr='${nextPageNr}']`)
    nextPage.classList.remove("BASE-hide")
}

document.addEventListener("keydown", (event) =>{
    if(event.keyCode === 13){
        changePage("next")
    }
})

