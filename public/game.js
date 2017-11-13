var newBoard = null;
var currentBoard = null;
var requestDelayCounter = 0;
var currentSelected = [null,null];

function hoverSelect(x, y) {
  if (currentSelected[0] != x || currentSelected[1] != y) {
    $("#" + y + "-" + x).attr("style", "background: #ffffe0;");
  }
}

function clickSelect(x, y) {
  $("#" + currentSelected[1] + "-" + currentSelected[0]).attr("style", "background: white;");
  $("#" + y + "-" + x).attr("style", "background: yellow;");
  let i = 0;
  let searching = true;
  let found;
  while (searching) {
    eval("found = piece" + i + ";");
    i++;
    if (found.pos[0] == x && found.pos[1] == y) {
      searching = false;
    }
  }
  console.log("found: " + found.pos[0] + "-" + found.pos[1]);
  for (var move in found.moves) {
    if (move[0] == "move_capture") {
      $("#" + move[2] + "-" + move[1]).attr("style", "background: red;");
    } else if (move[0] == "move") {
      $("#" + move[2] + "-" + move[1]).attr("style", "background: green;");
    }
  }
  currentSelected = [x,y];
}

function clearHighlightSelection(x, y) {
  if (currentSelected[0] != x || currentSelected[1] != y) {
    $("#" + y + "-" + x).attr("style", "background: white;");
  }
}


$(document).ready(() => {
  // adds event listeners
  for (var i = 0; i < 20; i++) {
    for (var j = 0; j < 20; j++) {
      eval(`$("#" + ${j} + "-" + ${i}).hover(() => {
        hoverSelect(${i},${j});
      }, () => {
        clearHighlightSelection(${i},${j});
      });
      $("#" + ${j} + "-" + ${i}).click(() => {
        console.log("click detected" + ${j} + "-" + ${i});
        clickSelect(${i},${j})
      });`);
    }
  }
  loop = true;
  displayLoop();
  requestLoop();
});

function updateBoard(board) {
  console.log("updating board");
  let i = 0;
  for (var piece in board.pieces) {
    eval(`piece${i} = board.pieces[${i}];`);
    eval(`var y = piece${i}.pos[1];`);
    eval(`var x = piece${i}.pos[0];`);
    eval("currentPiece = piece" + i + ";");
    console.log("current piece: " + currentPiece + " " + i);
    var imghtml = "<img src='img/" + currentPiece.color + "-" + currentPiece.type + ".png' height='28px'>";
    var targetTag = "td#" + y + "-" + x;
    console.log("target Tag: " + targetTag);
    console.log("html: " + imghtml);
    $(targetTag).html(imghtml);
    ++i;
  }
}

function displayLoop () {
  console.log("updating visuals");
  // updates height of board
  $("table#board-table").css("height", $("div#board").css("width"));
  $("table#board-table > tr > td").css("width", $("table#board-table > tr > td").css("height"));
  if (loop) {
    setTimeout(100, displayLoop);
  }
}

function requestLoop() {
  // console.log("getting json");
  // $.ajax({url: "boardState.json", dataType: "text", success: function (result) {
  //   console.log(result);
  //   newBoard = JSON.parse(result);
  // }});
  console.log("faking new board");
  newBoard = {
    pieces: [{
      type: "pawn",
      color: "BLACK",
      pos: [5, 5, 0],
      moves: [
        ["move_capture", 6, 4, 0],
        ["move", 6, 5, 0],
        ["move", 5, 4, 0]
      ]
    }, {
      type: "pawn",
      color: "WHITE",
      pos: [6, 4, 0],
      moves: [
        ["move_capture", 5, 5, 0],
        ["move", 5, 4, 0],
        ["move", 6, 5, 0]
      ]
    }, {
      type: "bishop",
      color: "WHITE",
      pos: [12, 12, 0],
      moves: [
        ["move_capture", 5, 5, 0]
        ["move", 11, 13, 0]
        ["move", 10, 14, 0]
        ["move", 13, 13, 0]
        ["move", 14, 14, 0]
        ["move", 11, 11, 0]
        ["move", 10, 10, 0]
        ["move", 13, 11, 0]
        ["move", 10, 14, 0]
      ]
    }, {
      type: "car-bomb",
      color: "WHITE",
      pos: [12, 7, 0],
      moves: [
        ["move_capture", 12, 7, 0],
        ["move", 5, 4, 0],
        ["move", 6, 5, 0]
      ]
    }, {
      type: "geopolitical-advisor",
      color: "WHITE",
      pos: [17, 15, 0],
      moves: [
        ["move_capture", 5, 5, 0],
        ["move", 5, 4, 0],
        ["move", 6, 5, 0]
      ]
    }, {
      type: "Wall-2",
      color: "WHITE",
      pos: [8, 13, 0],
      moves: [
        ["move_capture", 5, 5, 0],
        ["move", 5, 4, 0],
        ["move", 6, 5, 0]
      ]
    }]
  };

  if (newBoard != currentBoard) {
    updateBoard(newBoard);
    currentBoard = newBoard;
    newBoard = null;
  }
  if (loop) {
    setTimeout(requestLoop, 2000);
  }
}
