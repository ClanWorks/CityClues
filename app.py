import sqlite3
import random
from geopy.distance import geodesic
from flask import Flask, render_template, request, session
from utils import get_coordinates
import os

app = Flask(__name__)

# Get the secret key from the environment variable or use a default value
app.secret_key = os.environ.get('SECRET_KEY_CC')

# Get City and Clue from DB
def get_random_city_and_clues():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Cities')
    cities = cursor.fetchall()
    random_city = random.choice(cities)
    cursor.execute('SELECT * FROM Clues WHERE city_id=?', (random_city[0],))
    clues = cursor.fetchall()
    conn.close()
    return random_city, clues

@app.route('/')
def index():
    city, clues = get_random_city_and_clues()
    session['city'] = city
    session['clues'] = clues
    session['shown_clues'] = [clues[0]]
    session['remaining_guesses'] = 3
    return render_template('index.html', clue=clues[0])

@app.route('/guess', methods=['POST'])
def guess():
    user_guess = request.form['user_guess']
    city = session.get('city')
    remaining_guesses = session.get('remaining_guesses') - 1

    if user_guess.lower() == city[1].lower():
        return "Correct!"
    else:
        if remaining_guesses > 0:
            session['remaining_guesses'] = remaining_guesses

            # Show another clue, if available
            shown_clues = session.get('shown_clues')
            all_clues = session.get('clues')

            if len(shown_clues) < len(all_clues):
                new_clue = all_clues[len(shown_clues)]
                shown_clues.append(new_clue)
                session['shown_clues'] = shown_clues

            guessed_coords = get_coordinates(user_guess)
            if guessed_coords:
                distance = geodesic((city[2], city[3]), guessed_coords).kilometers
                return render_template('index.html', clue=new_clue, message=f"Wrong guess! You are {distance:.2f} km away from the correct city. You have {remaining_guesses} guesses left.")
            else:
                return render_template('index.html', clue=new_clue, message=f"Wrong guess! The city was not found. You have {remaining_guesses} guesses left.")
        else:
            return "Game over! The correct city was " + city[1]

if __name__ == '__main__':
    app.run(debug=True)



