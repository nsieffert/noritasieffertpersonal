from flask import Flask, render_template, redirect, jsonify, url_for, flash
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
application = app
app.secret_key = 'onetwothree' # Required for flash messages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            # Grab the data from the HTML form
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # Connect to SQLite database (creates file if it doesn't exist)
            conn = sqlite3.connect('messages.db')
            cur = conn.cursor()

            # Create table if it does not exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS messages
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     email TEXT NOT NULL,
                     message TEXT NOT NULL,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                        ''')

            # Insert form data into table
            cur.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))

            # Save changes and close the connection
            conn.commit()
            conn.close()

            # Return a successful JSON response
            return jsonify({'status': 'success', 'message': 'Your message has been sent!'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500

    return render_template('contact.html')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/watch')
def watch():
    return render_template('watch.html')

@app.route('/books')
def books():
    return render_template('books.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route("/form")
def form():
    # Serve the HTML form directly
    with open("contact.html", "r") as f:
        return f.read()


if __name__ == '__main__':
    app.run(debug=True)