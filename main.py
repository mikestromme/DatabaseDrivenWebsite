import pyodbc
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
database_server = os.getenv("database_server")
database = os.getenv("database")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")

app = Flask(__name__)

# Replace the values in the connection string with your actual server details.
connection_string = f"mssql+pyodbc://{db_user}:{db_password}@{database_server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/form1', methods=['GET', 'POST'])
def form1():
    if request.method == 'POST':
        param1 = request.form.get('param1')
        param2 = request.form.get('param2')

        proc_name = 'my_stored_proc_1'
        params = {'param1': param1, 'param2': param2}

        try:
            result = db.session.execute(proc_name, params)
            db.session.commit()

            # If no errors, redirect to a success page
            return redirect(url_for('success'))
        except Exception as e:
            # If there's an error, pass it to the template and it will be displayed on the form
            return render_template('form1.html', error=str(e))

    # Render the form
    return render_template('form1.html')

@app.route('/form2', methods=['GET', 'POST'])
def form2():
    if request.method == 'POST':
        param1 = request.form.get('param1')
        param2 = request.form.get('param2')

        proc_name = 'my_stored_proc_2'
        params = {'param1': param1, 'param2': param2}

        try:
            result = db.session.execute(proc_name, params)
            db.session.commit()

            # If no errors, redirect to a success page
            return redirect(url_for('success'))
        except Exception as e:
            # If there's an error, pass it to the template and it will be displayed on the form
            return render_template('form2.html', error=str(e))

    # Render the form
    return render_template('form2.html')

# Continue with more form routes...

@app.route('/success')
def success():
    return 'Form successfully submitted!'

if __name__ == '__main__':
    app.run(debug=True)
