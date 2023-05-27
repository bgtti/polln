function openPoll(){
    event.preventDefault();
    let element = document.querySelector("[name='WEBSITEprojectcode']");
    console.log(element)
    let projectCode = element.value;
    window.location.href = `/poll/${projectCode}`
}