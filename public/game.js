var newBoard = null;

$(document).ready(() => {
  loop = true;
  updateLoop();
});

function updateLoop() {
  // updates height of board
  $("table#board-table").css("height", $("div#board").css("width"));
  $("table#board-table > tr > td").css("width", $("table#board-table > tr > td").css("height"));
  // updates board
  $.ajax({url: "boardState.json", success: (result) => {
    newBoard = JSON.parse(result);
    if (newBoard == oldBoard) {
      newBoard = null;
    }
  }});
  if (newBoard) {
    for (var piece in newBoard.pieces) {
      var color = piece.color;
      var type = piece.type;
      var x = piece.pos[0];
      var y = piece.pos[1];
      for (var move in piece.move)
      var moves = piece.moves
    }
    oldBoard = newBoard;
    newBoard = null;
  }
  // makes visuals
  
  if (loop) {
    setTimeout(updateLoop, 100);
  }
}

// adds event listeners
for (var i = 0; i < 20; i++) {
  for (var j = 0; j < 20; j++) {
    $("tr." + i + " > td." + j).hover(() => {
      $("tr." + i + " > td." + j).addClass("red");
    }, () => {
      $("tr." + i + " > td." + j).removeClass("red");
    }));
    $("tr." + i + " > td." + j).click(clickSelect);
  }
}

function hoverSelect(x, y) {
  
}

function clickSelect(x, y) {
  
}

function clearSelection() {
  
}
