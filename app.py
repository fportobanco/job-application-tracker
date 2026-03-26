from flask import Flask, render_template, request, redirect, flash
from database import JobTrackerDB

app = Flask(__name__)
app.secret_key = 'secret_key'

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
def companies():
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        company_name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']

        try:
            db.insert_company(company_name, industry, website, city, state, notes)
            message = "Company successfully added to database."
            #To fix resubmission problem
            flash("Company added successfully!")
            return redirect('/companies')
        except:
            message = "Unable to add company to database."

    companies = db.get_all_companies()
    db.disconnect()

    return render_template('companies.html', companies=companies, message=message)

@app.route('/companies/edit/<int:company_id>', methods=['GET','POST'])
def edit_company(company_id):
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        company_name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']

        db.edit_company(company_name, industry, website, city, state, notes, company_id)
        db.disconnect()

        flash("Company edited successfully!")
        return redirect('/companies')
    
    cursor=db.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
    company = cursor.fetchone()
    companies = db.get_all_companies()
    db.disconnect()

    return render_template(
        'companies.html',
        companies=companies,
        editing_company=company
    )

@app.route('/companies/delete/<int:company_id>', methods=['GET','POST'])
def delete_company(company_id):
    db = JobTrackerDB()
    db.connect()
    message = ""

    try:
        if request.method == 'POST':
            db.delete_company(company_id)
            message = "Company successfully deleted."

        companies = db.get_all_companies()

        deleting_company = None
        if request.method == 'GET':
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
            deleting_company = cursor.fetchone()

    except Exception as e:
        message = f"Error: {e}"
        companies = []
        deleting_company = None

    finally:
        db.disconnect()

    return render_template(
        'companies.html',
        companies=companies,
        deleting_company=deleting_company,
        message=message
    )
if __name__ == '__main__':
    app.run(debug=True)
