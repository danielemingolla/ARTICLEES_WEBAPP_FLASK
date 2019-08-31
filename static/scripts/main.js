var MAXCHARACTERS = 600;

$(".card-text").each(function (i) {
  oldText = $(this).text();
  windowSize = window.innerWidth;
  //IPHONE 5/SE
  if (windowSize < 321) {
    MAXCHARACTERS = 420;
  }
  //IPAD
  else if (windowSize >= 768 && windowSize < 1020) {
    MAXCHARACTERS = 300;
  }
  //IPAD PRO
  else if (windowSize < 1900) {
    MAXCHARACTERS = 560;
  }
  //MY BROWSER SIZE
  else {
    MAXCHARACTERS = 650;
  }
  if (oldText.length > MAXCHARACTERS) {
    newText = oldText.substring(0, MAXCHARACTERS);
    $(this).text(newText + " [...]");
  }
});

//SIMULA IL CLICK SULL'INPUT CHOOSEN IN MODO DA PERSONALIZZARE LA LABEL COME SI VUOLE
$(document).ready(function () {
  $('.btn-info').on('click', function () {
    $('.input-custom').trigger('click');
  })
});
