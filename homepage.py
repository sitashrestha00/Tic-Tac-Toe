from flask import Flask, render_template, request, redirect, url_for
import main  # Import your main.py file

app = Flask(__name__)

# Global variables for game state
xState = [0] * 9
zState = [0] * 9
turn = 1  # 1 for X's turn, 0 for O's turn


@app.route('/')
def home():
    return render_template('home.html')  # The homepage with "Start the Game" button


@app.route('/game', methods=['GET', 'POST'])
def game():
    global xState, zState, turn
    if request.method == 'POST':
        value = int(request.form['cell'])  # Get which cell the user clicked on

        if turn == 1:
            xState[value] = 1  # X's move
        else:
            zState[value] = 1  # O's move

        winner = main.checkWin(xState, zState)  # Use the checkWin function from main.py
        if winner != -1:
            return render_template('game.html', xState=xState, zState=zState, message=f"Player {'X' if winner == 1 else 'O'} won!")

        turn = 1 - turn  # Switch turns

    return render_template('game.html', xState=xState, zState=zState, message="")

# Reset the game state for a new game
@app.route('/reset')
def reset():
    global xState, zState, turn
    xState = [0] * 9
    zState = [0] * 9
    turn = 1
    return redirect(url_for('game'))


if __name__ == '__main__':
    app.run(debug=True)
