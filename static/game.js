let currentPlayer = "X";

// Dynamically create the board
function createBoard() {
    const gameBoard = document.getElementById('game-board');
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.classList.add('game-cell');
        cell.id = `cell-${i}`;
        cell.addEventListener('click', () => handleMove(i));
        gameBoard.appendChild(cell);
    }
}

// Handle player move
function handleMove(position) {
    $.ajax({
        url: '/make_move',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ position: position }),
        success: function(response) {
            const board = response.board;
            currentPlayer = response.current_player;
            updateBoard(board);
            if (checkWinner(board)) {
                alert(`${currentPlayer === "X" ? "O" : "X"} Wins!`);
            }
        },
        error: function() {
            alert("Invalid move, try again.");
        }
    });
}

// Update the game board with new data
function updateBoard(board) {
    for (let i = 0; i < board.length; i++) {
        const cell = document.getElementById(`cell-${i}`);
        cell.textContent = board[i];
    }
}

// Check if someone has won
function checkWinner(board) {
    const winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  // Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  // Columns
        [0, 4, 8], [2, 4, 6]  // Diagonals
    ];

    for (const combination of winningCombinations) {
        if (board[combination[0]] === board[combination[1]] && board[combination[1]] === board[combination[2]] && board[combination[0]] !== "") {
            return true;
        }
    }
    return false;
}

// Reset the game board
document.getElementById('reset-btn').addEventListener('click', function() {
    $.ajax({
        url: '/reset',
        type: 'POST',
        success: function() {
            createBoard();
        }
    });
});

// On document ready
$(document).ready(function() {
    createBoard();
});
