function setup(){
	var parts = document.location.href.split("/");
	var game_id = parseInt(parts[parts.length-2]);
	var color = parts[parts.length-1].toUpperCase();
	var is_my_turn = false;

	var sock = io.connect('//' + document.domain + ':' + location.port);
	sock.on("connect", function(){
		table = $("#play-table");
		for(y=0;y<20;y++){
			child = $("<tr></tr>");
			table.append(child);
			for(x=0;x<20;x++){
				child.append($("<td class='play-cell' id=\"cell-"+x+"-"+y+"\"></td>"));
			}
		}

		function get_cell(x, y){
			return $("#cell-"+x+"-"+y);
		}

		function display_moves(piece){
			if (!(piece.color==color && is_my_turn)) return;
			console.log("actions for: "+piece.identifier);
			$(".move-info").remove();
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
				action_div.mousedown(function(e){
					e.preventDefault();
					if (e.which === 3) {
						apply_action(piece.pos[0], piece.pos[1], piece.pos[2], action.name, ax, ay, action.pos[2]);
					}
				});
			});
		}

		function draw_piece(container, piece){
			container.empty();
			var px = piece.pos[0];
			var py = piece.pos[1];
			if (piece_mappings[piece.identifier]==undefined){
				console.log("NO PIECE MAPPING: "+piece.identifier);
				return;
			}

			container.append("<img class='piece-image' src='/i/"+piece_mappings[piece.identifier](piece)+"'>");
		}

		function render_board(board_state){
			$("#item-stack-container").hide();
			var pieces_in_tiles = [];
			$(".play-cell").empty();

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
					}
				}
			}
		}

		// $.getJSON("/api/get_board_state/1", render_board);

		// function apply_action(px, py, pz, name, ax, ay, az){
		// 	$.getJSON("/api/apply_action/1/"+px+"/"+py+"/"+pz+"/"+name+"/"+ax+"/"+ay+"/"+az, render_board);
		// }

		function apply_action(px, py, pz, name, ax, ay, az){
			sock.emit("send_action", {
				"game_id":game_id,
				"name": name,
				"piece": [px, py, pz],
				"pos": [ax, ay, az]
			});
		}

		sock.on("update_board", render_board);
		sock.on("start_turn", function(data){
			is_my_turn = data.color == color;
			$("#status").text(data.color+"'s turn");
		});
		sock.emit("client_start", {"game_id":game_id, "color": color});
	});
}