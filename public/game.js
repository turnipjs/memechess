var newBoard = null;
var currentBoard = null;
var requestDelayCounter = 0;

function hoverSelect(x, y) {
  $("#" + y + "-" + x).attr("style", "background: grey;");
}

function clickSelect(x, y) {
  $("#" + y + "-" + x).attr("style", "background: black;");
}

function clearSelection(x, y) {
  $("#" + y + "-" + x).attr("style", "background: white;");
}


$(document).ready(() => {
  // adds event listeners
  for (var i = 0; i < 20; i++) {
    for (var j = 0; j < 20; j++) {
      $("#" + j + "-" + i).hover(() => {
        hoverSelect(i,j);
      }, () => {
        clearSelection(i,j);
      });
      $("#" + j + "-" + i).click(() => {
        clickSelect(i,j)
      });
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
    var imghtml = "<img src='img/" + currentPiece.color + "-" + currentPiece.type + ".png' height='24px'>";
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
