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
    if (newBoard == currentBoard) {
      newBoard = null;
    }
  }});
  if (newBoard) {
    let i = 0;
    for (var piece in newBoard.pieces) {
      eval(`piece${i} = {};`);
      eval(`var piece${i}.color = piece.color`);
      eval(`var piece${i}.type = piece.type`);
      eval(`var piece${i}.x = piece.pos[0]`);
      eval(`var piece${i}.y = piece.pos[1]`);
      let j = 0;
      for (var move in piece.moves) {
        eval(`piece${i}.move${j} = piece.moves[${j}]`);
        ++j;
      }
      $(`"tr." + piece${i}.y + " > td." + piece${i}.x`).innerHTML;
      ++i;
    }
    currentBoard = newBoard;
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
