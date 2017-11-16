function setup(){
	var parts = document.location.href.split("/");
	var game_id = parseInt(parts[parts.length-2]);
	var color = parts[parts.length-1].toUpperCase();
	var is_my_turn = false;
	var is_both = false;

	var curr_dragged_over = null;

	var sock = io.connect('//' + document.domain + ':' + location.port);
	sock.on("connect", function(){
		table = $("#play-table");
		for(y=0;y<20;y++){
			child = $("<tr></tr>");
			table.append(child);
			for(x=0;x<20;x++){
				child.append($("<td data-x='"+x+"' data-y='"+y+"' class='play-cell' id=\"cell-"+x+"-"+y+"\"></td>"));
			}
		}

		function get_cell(x, y){
			return $("#cell-"+x+"-"+y);
		}

		var drag_moveset = [];

		function display_moves(piece){
			$("#selected-info").show();
			$("#selected-info-box").empty();
			$("#selected-info-box").append(piece.color + " " + piece.identifier+" at "+piece.pos);
			piece.desc_text.split("\n").forEach(function(l){
				$("#selected-info-box").append("<br/>"+l);
			});
			$(".move-info").remove();
			drag_moveset=piece.actions;
			piece.actions.forEach(function(action){
				var action_div = $("<pre class='move-info'></pre>");
				var ax = action.pos[0];
				var ay = action.pos[1];
				get_cell(ax, ay).append(action_div);
				var desc = action_mappings[action.name];
				if (desc==undefined){
					console.log("NO ACTION MAPPING: "+action.name);
					desc = {"name":"?"+action.name+"?", "color":[0,0,0]};
				}
				action_div.text(desc.name);
				action_div.css("background-color", "rgba("+desc.color.join(",")+",0.4)");
				action_div.on("dragenter", drag_over);
				action_div.mousedown(function(e){
					e.preventDefault();
					if (e.which === 3) {
						apply_action(piece, action.name, ax, ay, action.pos[2]);
					}
				});
			});
		}

		function apply_action_by_xy(piece, x, y){
			$(".drag-hint").remove();
			var ok = false;
			drag_moveset.forEach(function(action){
				if((action.pos[0]==x) && (action.pos[1]==y)){
					ok=true;
					apply_action(piece, action.name, x, y, action.pos[2]);
				}
			});
			if (!ok) alert("Sorry, you can't move here");
		}

		function drag_over(e){
			if(curr_dragged_over) $(".drag-hint").remove();
			curr_dragged_over = $(e.target);
			var o = $("<div class='drag-hint'></div>");
			curr_dragged_over.parent().append(o);
		}

		function draw_piece(container, piece){
			container.empty();
			var px = piece.pos[0];
			var py = piece.pos[1];
			if (piece_mappings[piece.identifier]==undefined){
				console.log("NO PIECE MAPPING: "+piece.identifier);
				return;
			}
			var img = $("<img class='piece-image' src='/i/"+piece_mappings[piece.identifier](piece)+"'>");
			container.append(img);

			curr_dragged_over = null;
			img.on("dragstart", function(e){
				display_moves(piece);
			});
			img.on("dragenter", drag_over);
			img.on("dragend", function(e){
				apply_action_by_xy(piece, parseInt(curr_dragged_over.parent().attr("data-x")), parseInt(curr_dragged_over.parent().attr("data-y")));
			});
		}

		function render_board(board_state){
			$("#selected-info").hide();
			$("#item-stack-container").hide();
			$(".piece-image").off("cick");
			$(".piece-image").off("mousedown");
			$(".play-cell").empty();
			$(".drag-hint").remove()

			var pieces_in_tiles = [];

			for(y=0;y<20;y++){
				var l = [];
				pieces_in_tiles.push(l);
				for(x=0;x<20;x++){
					l.push([]);
					get_cell(x, y).empty();
					get_cell(x, y).append("<img class='piece-image' src='/i/blank.bmp'>");
				}
			}

			function get_in(x, y){
				return pieces_in_tiles[y][x];
			}

			board_state.pieces.forEach(function(piece){
				get_in(piece.pos[0], piece.pos[1]).push(piece);
				get_in(piece.pos[0], piece.pos[1]).sort((a, b) => a.pos[2]>b.pos[2])
			});

			for(y=0;y<20;y++){
				for(x=0;x<20;x++){
					var l = get_in(x, y);
					if (l.length!=0){
						draw_piece(get_cell(x, y), l[l.length-1]);
						get_cell(x, y).click(function(l){return function(e){
							$("#item-stack-container").hide();
							if(l.length==1){
								display_moves(l[l.length-1]);
							}else{
								$("#item-stack-container").show();
								$("#item-stack").empty();
								l.forEach(function(p){
									var cell = $("<td></td>");
									draw_piece(cell, p);
									cell.click(function(e){
										display_moves(p);
									});
									var row = $("<tr><td>"+p.pos[2]+"</td></tr>");
									row.append(cell);
									$("#item-stack").append(row);
								});
							}
						}}(l));
					}else{
						get_cell(x, y).empty();
						var img = $("<img class='piece-image' src='/i/blank.bmp'>");
						get_cell(x, y).append(img);
						img.on("dragenter", drag_over);
					}
				}
			}
		}

		// $.getJSON("/api/get_board_state/1", render_board);

		// function apply_action(px, py, pz, name, ax, ay, az){
		// 	$.getJSON("/api/apply_action/1/"+px+"/"+py+"/"+pz+"/"+name+"/"+ax+"/"+ay+"/"+az, render_board);
		// }

		function apply_action(piece, name, ax, ay, az){
			if (!(piece.color==color && is_my_turn)){
				alert("Sorry, this is not your peice and/or it is not your turn.");
				return;
			}
			sock.emit("send_action", {
				"game_id":game_id,
				"name": name,
				"piece": piece.pos,
				"pos": [ax, ay, az]
			});
		}

		sock.on("update_board", render_board);
		sock.on("start_turn", function(data){
			if(is_both) color = data.color;
			is_my_turn = data.color == color;
			var s = data.color+"'s ";
			if(is_my_turn) s+=" (Your)";
			s+= " Turn.";
			$("#status").text(s);
		});

		if(color=="WHITE" || color=="BLACK"){
			sock.emit("client_start", {"game_id":game_id, "color": color});
		}else if (color=="BOTH"){
			is_both = true;
			sock.emit("client_start", {"game_id":game_id, "color": "WHITE"});
			sock.emit("client_start", {"game_id":game_id, "color": "BLACK"});
		}else{
			sock.emit("client_start", {"game_id":game_id, "color": "OBSERVE"});
		}
		

		$("#status").text("Waiting for Opponent...");
	});
}