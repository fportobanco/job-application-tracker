from flask import Flask, render_template, request, redirect
# import mysql.connector
from database import JobTrackerDB

app = Flask(__name__)


@app.route('/')
def dashboard():
    db = JobTrackerDB()
    db.connect()
    cursor = db.connection.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as count FROM companies')
    stats = cursor.fetchone()
    db.disconnect()
    return render_template('dashboard.html', stats=stats)

@app.route('/companies', methods=['GET','POST'])
def insert_company():
    message = ""
    if request.method == 'POST':
        company_name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']

        try:
            db = JobTrackerDB()
            db.connect()
            db.insert_company(company_name, industry, website, city, state, notes)
            db.disconnect()
            message = "Company successfully added to database."
        except:
            message = "Unable to add company to database."
    return render_template('companies.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
