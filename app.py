from flask import Flask, render_template, request, redirect, flash
from database import JobTrackerDB
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key')

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
            flash("Company deleted successfully!")
            return redirect('/companies')

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

@app.route('/applications', methods=['GET','POST'])
def applications():
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        application_date = request.form['application_date']
        status = request.form['status']
        resume_version = request.form['resume_version']

        if 'cover_letter_sent' in request.form:
            cover_letter_sent = 1;
        else:
            cover_letter_sent = 0

        job_id = request.form['job_id']

        try:
            interview_data = json.loads(request.form['interview_data'])
            interview_data = json.dumps(interview_data)
        except json.JSONDecodeError:
            flash("Interview data is not JSON.", "danger")
            return redirect('/applications')

        try:
            db.insert_application(application_date, status, resume_version, cover_letter_sent, interview_data, job_id)
            message = "Application successfully added to database."
            #To fix resubmission problem
            flash("Application added successfully!")
            return redirect('/applications')
        except:
            message = "Unable to add application to database."

    applications = db.get_all_applications()
    jobs = db.get_all_jobs()
    db.disconnect()

    return render_template('applications.html', applications=applications, jobs=jobs, message=message)

@app.route('/applications/edit/<int:application_id>', methods=['GET','POST'])
def edit_application(application_id):
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        application_date = request.form['application_date']
        status = request.form['status']
        resume_version = request.form['resume_version']

        if 'cover_letter_sent' in request.form:
            cover_letter_sent = 1;
        else:
            cover_letter_sent = 0

        try:
            interview_data = json.loads(request.form['interview_data'])
            interview_data = json.dumps(interview_data)
        except json.JSONDecodeError:
            flash("Interview Data is not JSON.", "danger")
            return redirect('/applications')

        db.edit_application(application_date, status, resume_version, cover_letter_sent, interview_data, application_id)
        db.disconnect()

        flash("Application edited successfully!")
        return redirect('/applications')
    
    cursor=db.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications WHERE application_id = %s", (application_id,))
    application = cursor.fetchone()
    applications = db.get_all_applications()
    jobs = db.get_all_jobs()

    db.disconnect()

    return render_template(
        'applications.html',
        applications=applications,
        jobs=jobs,
        editing_application=application
    )

@app.route('/applications/delete/<int:application_id>', methods=['GET','POST'])
def delete_application(application_id):
    db = JobTrackerDB()
    db.connect()
    message = ""

    try:
        if request.method == 'POST':
            db.delete_application(application_id)
            flash("Application deleted successfully!")
            return redirect('/applications')

        applications = db.get_all_applications()

        deleting_application = None
        if request.method == 'GET':
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM applications WHERE application_id = %s", (application_id,))
            deleting_application = cursor.fetchone()

    except Exception as e:
        message = f"Error: {e}"
        applications = []
        deleting_application = None

    finally:
        db.disconnect()

    return render_template(
        'applications.html',
        applications=applications,
        deleting_application=deleting_application,
        message=message
    )
if __name__ == '__main__':
    app.run(debug=True)
