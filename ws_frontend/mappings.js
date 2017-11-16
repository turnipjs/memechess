function simple(name){
	return (piece) => piece.color+"-"+name+".png";
}

var piece_mappings={
	"pawn": simple("Pawn"),
	"rook": simple("Rook"),
	"bishop": simple("Bishop"),
	"queen": simple("Queen"),
	"king": simple("King"),
	"knight": simple("Knight"),
	"pope": simple("Pope"),
	"beekeeper": simple("Tower-Poly"),
	"cave_portal": () => "WHITE-Tower-Star.png",
	"wall": () => "BLACK-Tower-Square.png",
	"portal_entrance": () => "BLACK-Geopolitical-Advisor.png",
	"portal_exit": () => "BLACK-Geopolitical-Expert.png"
}

var action_mappings = {
	"move": {"name":"Move", "color":[0,255,0]},
	"move_capture": {"name":"Capture", "color":[255,0,0]}
}