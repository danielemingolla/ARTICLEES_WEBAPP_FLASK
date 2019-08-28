var MAXCHARACTERS = 512;

$(".card-text").each(function(i) {
  oldText = $(this).text();
  console.log("OLD: " + oldText);
  if (oldText.length > MAXCHARACTERS) {
    newText = oldText.substring(0, MAXCHARACTERS);
    $(this).text(newText + " [...]");
    console.log("NEW: " + newText);
  }
});


