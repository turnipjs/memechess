function setup(){
	table = $("#play-table");
	for(y=0;y<20;y++){
		child = $("<tr></tr>");
		table.append(child);
		for(x=0;x<20;x++){
			child.append($("<td id=\"cell-"+x+"-"+y+"\"><pre id=\"move-"+x+"-"+y+"\" class='move-info'></pre><img id=\"img-"+x+"-"+y+"\" class='piece-image'/></td>"));
			set_tile(x, y, null);
		}
	}

	function get_tile(x, y){
		return $("#img-"+x+"-"+y);
	}

	function get_move_slot(x, y){
		return $("#move-"+x+"-"+y);
	}

	function set_tile(x, y, path){
		if (path==null){
			path="/i/blank.bmp";
		}
		get_tile(x, y).attr("src", path);
	}

	function clear_actions(){
		for(y=0;y<20;y++){
			for(x=0;x<20;x++){
				get_move_slot(x, y).text("");
				get_move_slot(x, y).css("background-color", "rgba(0,0,0,0)");
				// get_move_slot(x, y).off("click");
				get_move_slot(x, y).off("mousedown");
			}
		}
	}

	function render_board(board_state){
		clear_actions();
		for(y=0;y<20;y++){
			for(x=0;x<20;x++){
				set_tile(x, y, null);
			}
		}

		board_state.pieces.forEach(function(piece){
			var px = piece.pos[0];
			var py = piece.pos[1];
			if (piece_mappings[piece.identifier]==undefined){
				console.log("NO PIECE MAPPING: "+piece.identifier);
				return;
			}
			set_tile(px, py, "/i/"+piece_mappings[piece.identifier](piece));
			get_move_slot(px, py).click(function(e){
				clear_actions();
				piece.actions.forEach(function(action){
					var ax = action.pos[0];
					var ay = action.pos[1];
					var desc = action_mappings[action.name];
					if (desc==undefined){
						console.log("NO ACTION MAPPING: "+action.name);
						desc = {"name":"?"+action.name+"?", "color":[0,0,0]};
					}
					get_move_slot(ax, ay).text(desc.name);
					get_move_slot(ax, ay).css("background-color", "rgba("+desc.color.join(",")+",0.4)");
					get_move_slot(ax, ay).mousedown(function(e){
						e.preventDefault();
						if (e.which === 3) {
							$.getJSON("/api/apply_action/1/"+px+"/"+py+"/"+piece.pos[2]+"/"+action.name+"/"+ax+"/"+ay+"/"+action.pos[2], render_board);
						}
					});
				});
			});
		});
	}

	$.getJSON("/api/get_board_state/1", render_board);
}