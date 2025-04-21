// Open poll when respondent joins a presentation by entering the code in homepage
function openPoll() {
 event.preventDefault();
 let element = document.querySelector("[name='WEBSITEprojectcode']");
 let projectCode = element.value;
 window.location.href = `/poll/${projectCode}`
}

//Homepage image animation
//Tablet
let counterTablet = 1;
let intervalTablet;
let milisecTablet = 2500;
const imageTablet = document.getElementById('WEBSITE-img-present');
function tabletImageChange() {
 let src = `/static/website/media/img_PollN_presentation_${counterTablet}.png`
 imageTablet.src = src
 if (counterTablet === 2) {
  milisecTablet = 150;
  clearInterval(intervalTablet);
  intervalTablet = setInterval(tabletImageChange, milisecTablet);
 } else if (counterTablet === 12) {
  milisecTablet = 2500;
  clearInterval(intervalTablet);
  intervalTablet = setInterval(tabletImageChange, milisecTablet);
 } else if (counterTablet === 14) {
  milisecTablet = 4000;
  clearInterval(intervalTablet);
 }
 counterTablet === 14 ? counterTablet = 1 : counterTablet++
}
intervalTablet = setInterval(tabletImageChange, milisecTablet);

//Smartphone
let counterPhone = 1;
let intervalPhone;
let milisecPhone = 1500;
const imagePhone = document.getElementById('WEBSITE-img-poll');
function phoneImageChange() {
 let src = `/static/website/media/img_PollN_poll_${counterPhone}.png`
 imagePhone.src = src
 //There are 5 images.
 //Wait for end of Tablet animation before continuing. Reset counter at the end:
 if (counterPhone === 2) {
  milisecPhone = 600;
  clearInterval(intervalPhone);
  intervalPhone = setInterval(phoneImageChange, milisecPhone);
 } else if (counterPhone === 5) {
  milisecPhone = 1500;
  clearInterval(intervalPhone);
  // intervalPhone = setInterval(phoneImageChange, milisecPhone);
 }
 counterPhone === 5 ? counterPhone = 1 : counterPhone++
}
intervalPhone = setInterval(phoneImageChange, milisecPhone);

//Re-sync interval
function resetAnimation() {
 imageTablet.src = `/static/website/media/img_PollN_presentation_1.png`
 imagePhone.src = `/static/website/media/img_PollN_poll_1.png`
 clearInterval(intervalTablet);
 milisecTablet = 2500;
 counterTablet = 1;
 clearInterval(intervalPhone);
 milisecPhone = 1500;
 counterPhone = 1;
 intervalTablet = setInterval(tabletImageChange, milisecTablet);
 intervalPhone = setInterval(phoneImageChange, milisecPhone);
}
setInterval(resetAnimation, 15000)