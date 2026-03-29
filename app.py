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
            flash("Interview Data is not JSON.")
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

@app.route('/jobs', methods=['GET','POST'])
def jobs():
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        date_posted = request.form['date_posted']
        job_title = request.form['job_title']
        job_type = request.form['job_type']
        salary_min = request.form['salary_min']
        salary_max = request.form['salary_max']
        job_url = request.form['job_url']
        requirements = request.form['requirements']
        company_id = request.form['company_id']

        try:
            requirements = json.loads(request.form['requirements'])
            requirements = json.dumps(requirements)
        except json.JSONDecodeError:
            flash("Requirements data is not JSON.")
            return redirect('/jobs')

        try:
            db.insert_job(date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, company_id)
            message = "Job successfully added to database."
            #To fix resubmission problem
            flash("Job added successfully!")
            return redirect('/jobs')
        except:
            message = "Unable to add job to database."

    jobs = db.get_all_jobs()
    companies = db.get_all_companies()
    db.disconnect()

    return render_template('jobs.html', jobs=jobs, companies=companies, message=message)

@app.route('/jobs/edit/<int:job_id>', methods=['GET','POST'])
def edit_job(job_id):
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        date_posted = request.form['date_posted']
        job_title = request.form['job_title']
        job_type = request.form['job_type']
        salary_min = request.form['salary_min']
        salary_max = request.form['salary_max']
        job_url = request.form['job_url']
        requirements = request.form['requirements']

        try:
            requirements = json.loads(request.form['requirements'])
            requirements = json.dumps(requirements)
        except json.JSONDecodeError:
            flash("Requirements Data is not JSON.")
            return redirect('/jobs')

        db.edit_job(date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, job_id)
        db.disconnect()

        flash("Job edited successfully!")
        return redirect('/jobs')
    
    cursor=db.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    job = cursor.fetchone()
    jobs = db.get_all_jobs()
    companies = db.get_all_companies()

    db.disconnect()

    return render_template(
        'jobs.html',
        jobs=jobs,
        companies=companies,
        editing_job=job
    )

@app.route('/jobs/delete/<int:job_id>', methods=['GET','POST'])
def delete_job(job_id):
    db = JobTrackerDB()
    db.connect()
    message = ""

    try:
        if request.method == 'POST':
            db.delete_job(job_id)
            flash("Job deleted successfully!")
            return redirect('/jobs')

        jobs = db.get_all_jobs()

        deleting_job = None
        if request.method == 'GET':
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
            deleting_job = cursor.fetchone()

    except Exception as e:
        message = f"Error: {e}"
        jobs = []
        deleting_job = None

    finally:
        db.disconnect()

    return render_template(
        'jobs.html',
        jobs=jobs,
        deleting_job=deleting_job,
        message=message
    )

@app.route('/contacts', methods=['GET','POST'])
def contacts():
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        company_id = request.form['company_id']
        contact_name = request.form['contact_name']
        title = request.form['title']
        email = request.form['email']
        phone = request.form['phone']
        linkedin_url = request.form['linkedin_url']
        notes = request.form['notes']

        try:
            db.insert_contact(contact_name, title, email, phone, linkedin_url, notes, company_id)
            message = "Contact successfully added to database."
            #To fix resubmission problem
            flash("Contact added successfully!")
            return redirect('/contacts')
        except:
            message = "Unable to add contact to database."

    contacts = db.get_all_contacts()
    companies = db.get_all_companies()
    db.disconnect()

    return render_template('contacts.html', contacts=contacts, companies=companies, message=message)

@app.route('/contacts/edit/<int:contact_id>', methods=['GET','POST'])
def edit_contact(contact_id):
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        contact_name = request.form['contact_name']
        title = request.form['title']
        email = request.form['email']
        phone = request.form['phone']
        linkedin_url = request.form['linkedin_url']
        notes = request.form['notes']

        db.edit_contact(contact_name, title, email, phone, linkedin_url, notes, contact_id)
        db.disconnect()

        flash("Contact edited successfully!")
        return redirect('/contacts')
    
    cursor=db.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts WHERE contact_id = %s", (contact_id,))
    contact = cursor.fetchone()
    contacts = db.get_all_contacts()
    companies = db.get_all_companies()

    db.disconnect()

    return render_template(
        'contacts.html',
        contacts=contacts,
        companies=companies,
        editing_contact=contact
    )

@app.route('/contacts/delete/<int:contact_id>', methods=['GET','POST'])
def delete_contact(contact_id):
    db = JobTrackerDB()
    db.connect()
    message = ""

    try:
        if request.method == 'POST':
            db.delete_contact(contact_id)
            flash("Contact deleted successfully!")
            return redirect('/contacts')

        contacts = db.get_all_contacts()

        deleting_contact = None
        if request.method == 'GET':
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM contacts WHERE contact_id = %s", (contact_id,))
            deleting_contact = cursor.fetchone()

    except Exception as e:
        message = f"Error: {e}"
        contacts = []
        deleting_contact = None

    finally:
        db.disconnect()

    return render_template(
        'contacts.html',
        contacts=contacts,
        deleting_contact=deleting_contact,
        message=message
    )
if __name__ == '__main__':
    app.run(debug=True)
