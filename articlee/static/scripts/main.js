var maxCharacterCardText = 400;
var maxCharacterCardTitle = 25;

// Limita i caratteri dell'anteprima degli articoli

$(".card-text").each(function (i) {
  oldText = $(this).text();
  windowSize = window.innerWidth;
  if (windowSize > 1900) {
    maxCharacterCardText = 500;
  }
  else if (windowSize > 1300) {
    maxCharacterCardText = 430;
  }
  else if (windowSize < 414) {
    maxCharacterCardText = 330;
  }
  if (oldText.length > maxCharacterCardText) {
    newText = oldText.substring(0, maxCharacterCardText);
    $(this).text(newText + " [...]");
  }
});

$(".card-title").each(function (i) {
  oldText = $(this).text();
  if (oldText.length > maxCharacterCardTitle) {
    newText = oldText.substring(0, maxCharacterCardTitle - 6);
    $(this).text(newText + " [...]");
  }
});