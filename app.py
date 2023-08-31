import sqlite3
import random
from geopy.distance import geodesic
from flask import Flask, render_template, request, session, redirect, url_for
from utils import get_coordinates
import os

# Display previous guesses
# Extend Locations
# Additional rounds of clue
# Images

app = Flask(__name__)

# Get the secret key from the environment variable or use a default value
app.secret_key = os.environ.get('SECRET_KEY_CC')

# Get City and Clue from DB
def get_random_city_and_clues():
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cities')
        cities = cursor.fetchall()
        if not cities:
            return None, "No cities found in the database."
        
        random_city = random.choice(cities)
        
        cursor.execute('SELECT * FROM Clues WHERE city_id=?', (random_city[0],))
        clues = cursor.fetchall()
        if not clues:
            return None, "No clues found for the selected city."
        
        conn.close()
        return random_city, clues
    except sqlite3.Error as e:
        return None, f"Database error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['action'] == 'restart':
            # Reset the game and redirect to the index
            session.pop('city', None)
            session.pop('clues', None)
            session.pop('shown_clues', None)
            session.pop('remaining_guesses', None)
            return redirect(url_for('index'))

    city, clues = get_random_city_and_clues()
    session['city'] = city
    session['clues'] = clues
    session['shown_clues'] = [clues[0]]
    session['remaining_guesses'] = 3
    message = ''  # Initialize with an empty string

    return render_template('index.html', clue=clues[0], message=message)

@app.route('/guess', methods=['POST'])
def guess():
    user_guess = request.form['user_guess']
    city = session.get('city')
    remaining_guesses = session.get('remaining_guesses') - 1
    session['remaining_guesses'] = remaining_guesses

    message = ""  # Placeholder for our message
    new_clue = None  # Initialize new_clue to None at the start

    if user_guess.lower() == city[1].lower():
        message = f"Correct! The answer was {city[1]}!"
        return render_template('index.html', message=message)
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
                message = f"Wrong guess! You are {distance:.2f} km away from the correct city. You have {remaining_guesses} guesses left."
            else:
                message = f"Wrong guess! The city was not found. You have {remaining_guesses} guesses left."
        else:
            message = f"Game over! The correct city was {city[1]}"
        return render_template('index.html', message=message, city=city, clue=session.get('shown_clues')[-1])

    if new_clue:  # Only pass new_clue if it is not None
        return render_template('index.html', clue=new_clue, message=message)
    else:
        return render_template('index.html', message=message)

@app.route('/restart', methods=['POST'])
def restart():
    session.clear()  # Clear the session
    return redirect('/')  # Redirect to the index to restart the game


if __name__ == '__main__':
    app.run(debug=True)



