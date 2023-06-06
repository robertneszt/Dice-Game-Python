import re
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "demo_key" #sets secret key, necessary

def validate_player_name(name):
    pattern = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')  #regex name validation
    return bool(pattern.match(name))

@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    if request.method == "POST":
        player1 = request.form.get("player1", None)
        player2 = request.form.get("player2", None)

        if player1 is not None and player2 is not None:
            if not validate_player_name(player1) or not validate_player_name(player2):
                error_message = "Player names must be between 3 and 20 characters and can only contain letters, numbers, dashes, and underscores."
            elif len(player1) < 3 or len(player2) < 3:
                error_message = "Player names must be 3 or more characters in length."
            else:
                session["player1"] = player1
                session["player2"] = player2
                session["score1"] = 0
                session["score2"] = 0
                session["running_score"] = 0
                session["current_player"] = 1
                return redirect(url_for("game"))
            
    return render_template("index.html", error_message=error_message)

@app.route("/game", methods=["GET", "POST"])
def game():
    dice_picture = None
    winner = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "roll":
            roll = RollDice()
            dice_picture = f"/static/img/die{roll}.bmp" # set the picture of the dice using roll variable
            if roll == 1:
                session["running_score"] = 0
                SwitchTurn()  # switch turns if the rolled number is 1
            else:
                session["running_score"] += roll
        elif action == "hold":
            UpdateScore() # update player's score
            SwitchTurn()  # switch turns

        winner = DetermineWin() #ends game as a win state has been declared!

    return render_template("game.html", dice_picture=dice_picture, winner=winner)

def SwitchTurn():
    if session["current_player"] == 1:
        session["current_player"] = 2
    else:
        session["current_player"] = 1
    session["running_score"] = 0
    
    # generate a random number between 1 and 6
def RollDice():
    return random.randint(1, 6)

def DetermineWin():
    if session["score1"] >= 20:
        return session["player1"]
    elif session["score2"] >= 20:
        return session["player2"]
    else:
        return None

def UpdateScore():
    if session["current_player"] == 1:
        session["score1"] += session["running_score"]
    else:
        session["score2"] += session["running_score"]

#ensures script is run directly, not by another module
if __name__ == "__main__":
    app.run(debug=True) #starts flask and runs it with debug enabled for bug fixing