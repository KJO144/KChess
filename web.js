var url_base = 'http://127.0.0.1:5000/'
var black_square_col = "darkgrey"
var white_square_col = "lightyellow"
var piece_colours = {'W': "salmon", 'WK': 'darkred', 'B': "royalblue", 'BK': 'mediumblue'}
var square_size = 50
var board_size = 8
var player_names = {'W': 'White', 'B': 'Black'}

function draw_piece(sq, piece){
    // The piece images are expected to be in a sub-folder 'img'
    let element = document.getElementById(sq)
    let game = get_game()
    let src = `img/${game}_${piece}.png`
    element.setAttribute('src', src)		
    element.setAttribute('data-piece', piece)		
}

function drawBoard(){
    /*
     Initialize the html table representing the board.
     Each element is a square containing a canvas with id 'S23' for example.
    */
    let table = document.getElementById("board");
    for(i=0; i<board_size; i++){
        let row = table.insertRow(0)			
        for(j=0; j<board_size; j++){
            let cell = row.insertCell(-1)
            let sq = 'S' + String(i) + String(j)
            if((i+j)%2==0) {col = black_square_col} else {col = white_square_col}

            cell.innerHTML=`<img id=${sq} width=${square_size} height=${square_size} style="background-color:${col}"
            draggable="true" ondragstart="dragstart(event)" ondrop="dragDrop(event)" ondragover="allowDrop(event)"
            class="board_square" data-piece="E">
            `
        }	
    }		
}

function update_board(position){
    /*
    Given a new position, update the board.
    */
    let board_pos = position['position']
    let tomove = position['player_to_move']
    let previous_move = position['previous_move']
    for(i=0; i<board_size; i++){			
        for(j=0; j<board_size; j++){
            let sq = 'S' + String(i) + String(j)
            draw_piece(sq, board_pos[sq])
        }	
    }
    document.getElementById('previous-move').setAttribute('value', previous_move)
    document.getElementById('to-move').setAttribute('to-move', tomove)
    document.getElementById('to-move-box').setAttribute('style','fill:' + piece_colours[tomove] )

    let winner = position['winner']
    if(winner != null){
        document.getElementById('move_button').disabled = true
        document.getElementById('indicator').innerHTML = player_names[winner] + " wins!"
    }

    if (get_game() == 'chess'){
        for( ctype of ['WKS', 'WQS', 'BKS', 'BQS']){
            let val = position['can_castle'][ctype]
            let sval = String(val)	
        
            document.getElementById(ctype).setAttribute('value', sval)
        }
    }
}

function restart_game(){
    document.getElementById('move_button').disabled = false
    get_initial_position()
}

function get_position(){
    // Returns an object representing the current board position
    let pos = {}
    let board_squares = document.getElementsByClassName('board_square')
    for(board_square of board_squares){
        let sq = board_square.getAttribute('id')
        let piece = board_square.getAttribute('data-piece')
        pos[sq] = piece
    }
    let tomove = get_tomove()
    let previous_move = get_previous_move()

    let ret = {position: pos, player_to_move: tomove, previous_move: previous_move}

    let castling = document.getElementsByClassName('castling')
    
    let castling_rights = {}
    for(element of castling){
        let value = element.getAttribute('value')
        let key = element.getAttribute('id')
        castling_rights[key] = JSON.parse(value)
    }
    
    ret['can_castle'] = castling_rights
    return(ret)
}

function get_game(){
    return(document.getElementById('game').getAttribute('game'))
}

function get_tomove(){
    return(document.getElementById('to-move').getAttribute('to-move'))
}

function get_previous_move(){
    return(document.getElementById('previous-move').getAttribute('value'))
}

function get_initial_position(){
    let url = url_base + get_game() + "/initial_position"
    fetch(url).then(response => response.json()).then(json => update_board(json));
}

function getMoveFromServer(){
    let pos = get_position()
    let pos_json = JSON.stringify(pos)
    let old_tomove = get_tomove()
    
    let url = url_base + get_game() + "/pos/" + pos_json

    fetch(url)
        .then(response => response.json())
        .then(json => update_board(json))
        .then(function(){
            let new_tomove = get_tomove()
            if(new_tomove == old_tomove){getMoveFromServer()}
        }
        );
}

function play_move(move){
    // Move is of the format S12_S23.
    // 1. Sends the move to the server
    // 2. Gets back the new board and calls update_board
    // 3. Requests the server to play a move
    
    let pos = get_position()
    pos['move'] = move
    let tomove = pos['player_to_move']
    let pos_and_move_json = JSON.stringify(pos)
    url = url_base + get_game() + "/" + "move/" + pos_and_move_json
    
    fetch(url)
// first call the 'move' API to make the user's move
        .then(response => response.json())
        .then(json => update_board(json))
// now call the 'pos' API to get the computer's response
        .then(function(){
            let new_mover = get_tomove()
            if( new_mover != tomove ){
                getMoveFromServer()
            }	
        }
        );
}

function dragstart(event){
    let source_ID = event.target.id
    event.dataTransfer.setData("some_text", source_ID);
}

function dragDrop(event){
    event.preventDefault();
    let orig = event.dataTransfer.getData("some_text"); 
    let dest = event.target.id
    if(orig != dest){
        let move = orig + "_" + dest
        console.log(`move ${move}`)
        play_move(move)
    }
}

function allowDrop(event){
    event.preventDefault(); 
}

function setGame(game){
    document.getElementById('game').setAttribute('game', game)
    restart_game()
}
