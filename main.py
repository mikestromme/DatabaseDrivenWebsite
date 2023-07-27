import pyodbc
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

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
        param3 = ''

        proc_name = text('EXEC tc_create_flask :param1, :param2, :param3') # Use text() to wrap the stored procedure call
        params = {'param1': param1, 'param2': param2, 'param3': param3}

        try:
            result = db.session.execute(proc_name, params) # This should now correctly call your stored procedure
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


@app.route('/execute_proc', methods=['POST'])
def execute_proc():
    data = request.get_json()

    # Stored procedure name.
    proc_name = data['proc_name']

    # The parameters are expected to be passed in the request as a dictionary.
    # Each key is a parameter name and each value is the corresponding parameter value.
    params = data['params']

    try:
        result = db.session.execute(proc_name, params)
        db.session.commit()

        # If the procedure is supposed to return something, you can fetch it with result.fetchall()

        return {'status': 'success'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400
    

@app.route('/viewdata')
def viewdata():
    result = db.session.execute(text("SELECT top 10 * FROM catavolt_users"))
    data = result.fetchall()

    # Get the keys (column names) from the ResultProxy object
    keys = result.keys()

   # Convert each row to a dictionary
    data = [dict(zip(keys, row)) for row in data]

    #return {'data': data, 'columns': list(keys)}


    return render_template('viewdata.html',data=data)



if __name__ == '__main__':
    app.run(debug=True)
