from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the game board
def initialize_game():
    return [['' for _ in range(3)] for _ in range(3)]

# Check if someone has won
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return True  # Row win
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return True  # Column win
    if board[0][0] == board[1][1] == board[2][2] != '':
        return True  # Diagonal win
    if board[0][2] == board[1][1] == board[2][0] != '':
        return True  # Diagonal win
    return False

# Reset game if necessary
@app.route('/')
def home():
    # Start a new game
    session['board'] = initialize_game()
    session['player'] = 'X'  # Player X starts first
    return render_template('home.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Render the game board or process player move
    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])
        if session['board'][row][col] == '':
            session['board'][row][col] = session['player']
            if check_winner(session['board']):
                return redirect(url_for('game_winner'))
            session['player'] = 'O' if session['player'] == 'X' else 'X'  # Switch player
    return render_template('game.html', board=session['board'], player=session['player'])

@app.route('/game')
def game_winner():
    return render_template('game.html')

if __name__ == "__main__":
    app.run(debug=True)
