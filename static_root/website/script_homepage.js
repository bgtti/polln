// Open poll when respondent joins a presentation by entering the code in homepage
function openPoll() {
 event.preventDefault();
 let element = document.querySelector("[name='WEBSITEprojectcode']");
 let projectCode = element.value;
 window.location.href = `/poll/${projectCode}`
}

<<<<<<< HEAD
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
=======
// Homepage Tablet & Phone animation

// =====================
// Image Preloading
// =====================
const preloadImages = (paths) => {
 return Promise.all(
  paths.map((path) => {
   return new Promise((resolve) => {
    const img = new Image();
    img.src = path;
    img.onload = resolve;
    img.onerror = resolve; // Resolve even on error to avoid blocking
   });
  })
 );
};

// =====================
// Tablet Animation
// =====================
let counterTablet = 1;
let milisecTablet = 2500;
const imageTablet = document.getElementById('WEBSITE-img-present');

const tabletImages = Array.from({ length: 14 }, (_, i) =>
 `/static/website/media/img_PollN_presentation_${i + 1}.png`
);

function tabletImageChange() {
 imageTablet.src = tabletImages[counterTablet - 1];

 if (counterTablet === 2) {
  milisecTablet = 150;
 } else if (counterTablet === 12) {
  milisecTablet = 2500;
 } else if (counterTablet === 14) {
  milisecTablet = 4000;
 }

 counterTablet = counterTablet === 14 ? 1 : counterTablet + 1;

 setTimeout(tabletImageChange, milisecTablet);
}

// =====================
// Phone Animation
// =====================
let counterPhone = 1;
let milisecPhone = 1500;
const imagePhone = document.getElementById('WEBSITE-img-poll');

const phoneImages = Array.from({ length: 5 }, (_, i) =>
 `/static/website/media/img_PollN_poll_${i + 1}.png`
);

function phoneImageChange() {
 imagePhone.src = phoneImages[counterPhone - 1];

 if (counterPhone === 2) {
  milisecPhone = 600;
 } else if (counterPhone === 5) {
  milisecPhone = 1500;
 }

 counterPhone = counterPhone === 5 ? 1 : counterPhone + 1;

 setTimeout(phoneImageChange, milisecPhone);
}

// =====================
// Reset animation (re-sync)
function resetAnimation() {
 imageTablet.src = tabletImages[0];
 imagePhone.src = phoneImages[0];
 counterTablet = 1;
 counterPhone = 1;
 milisecTablet = 2500;
 milisecPhone = 1500;
}

// =====================
// Run after preload
// =====================
Promise.all([
 preloadImages(tabletImages),
 preloadImages(phoneImages)
]).then(() => {
 tabletImageChange();
 phoneImageChange();
 setInterval(resetAnimation, 15000);
});
>>>>>>> main
