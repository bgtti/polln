function openPoll(){
    event.preventDefault();
    let element = document.querySelector("[name='WEBSITEprojectcode']");
    let projectCode = element.value;
    window.location.href = `/poll/${projectCode}`
}