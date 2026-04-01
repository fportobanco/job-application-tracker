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
    company_stats = cursor.fetchone()

    cursor.execute('SELECT COUNT(*) as count FROM applications')
    applications_stats = cursor.fetchone()

    cursor.execute('SELECT COUNT(*) as count FROM jobs')
    jobs_stats = cursor.fetchone()

    cursor.execute('SELECT COUNT(*) as count FROM contacts')
    contacts_stats = cursor.fetchone()

    stats = {
        "companies": company_stats['count'],
        "applications": applications_stats['count'],
        "jobs": jobs_stats['count'],
        "contacts": contacts_stats['count']
    }
    
    application_stats = db.application_statuses()
    db.disconnect()
    return render_template('dashboard.html', stats=stats, application_stats=application_stats)

@app.route('/companies', methods=['GET','POST'])
def companies():
    message = ""
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        company_name = request.form['company_name'].strip()
        industry = request.form['industry'].strip()
        website = request.form['website'].strip()
        city = request.form['city'].strip()
        state = request.form['state'].strip()
        notes = request.form['notes'].strip()

        if not company_name:
            flash("Please include a company name.")
            return redirect('/companies')

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
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        company_name = request.form['company_name'].strip()
        industry = request.form['industry'].strip()
        website = request.form['website'].strip()
        city = request.form['city'].strip()
        state = request.form['state'].strip()
        notes = request.form['notes'].strip()

        if not company_name:
            flash("Please include a company name.")
            return redirect('/companies')
        
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
        resume_version = request.form['resume_version'].strip()
        interview_data = request.form['interview_data'].strip()

        if 'cover_letter_sent' in request.form:
            cover_letter_sent = 1;
        else:
            cover_letter_sent = 0

        job_id = request.form['job_id']

        if not application_date:
            flash("Please include an application date")
            return redirect('/applications')

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
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        job_id = request.form['job_id']
        application_date = request.form['application_date']
        status = request.form['status']
        resume_version = request.form['resume_version'].strip()
        interview_data = request.form['interview_data'].strip()
        
        if 'cover_letter_sent' in request.form:
            cover_letter_sent = 1;
        else:
            cover_letter_sent = 0

        if not application_date:
            flash("Please include an application date.")
            return redirect('/applications')
        
        try:
            interview_data = json.loads(request.form['interview_data'])
            interview_data = json.dumps(interview_data)
        except json.JSONDecodeError:
            flash("Interview Data is not JSON.")
            return redirect('/applications')

        db.edit_application(job_id, application_date, status, resume_version, cover_letter_sent, interview_data, application_id)
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
        date_posted = request.form['date_posted'].strip()
        job_title = request.form['job_title'].strip()
        job_type = request.form['job_type']
        salary_min = request.form.get('salary_min', '').strip()
        salary_max = request.form.get('salary_max', '').strip()
        job_url = request.form['job_url'].strip()
        requirements = request.form['requirements'].strip()
        company_id = request.form['company_id']

        salary_min = int(salary_min) if salary_min else None
        salary_max = int(salary_max) if salary_max else None

        if not job_title:
            flash("Please include a job title.")
            return redirect('/jobs')
        
        if salary_min and salary_max and salary_min > salary_max:
            flash("Please enter a Salary Min that is less than Salary Max.")
            return redirect('/jobs')
        
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
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        company_id = request.form['company_id']
        date_posted = request.form['date_posted'].strip()
        job_title = request.form['job_title'].strip()
        job_type = request.form['job_type']
        salary_min = request.form.get('salary_min', '').strip()
        salary_max = request.form.get('salary_max', '').strip()
        job_url = request.form['job_url'].strip()
        requirements = request.form['requirements'].strip()

        salary_min = int(salary_min) if salary_min else None
        salary_max = int(salary_max) if salary_max else None

        if not job_title:
            flash("Please include a job title.")
            return redirect('/jobs')
        
        if salary_min and salary_max and salary_min > salary_max:
            flash("Please enter a Salary Min that is less than Salary Max.")
            return redirect('/jobs')
        
        try:
            requirements = json.loads(request.form['requirements'])
            requirements = json.dumps(requirements)
        except json.JSONDecodeError:
            flash("Requirements Data is not JSON.")
            return redirect('/jobs')

        db.edit_job(company_id, date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, job_id)
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
        contact_name = request.form['contact_name'].strip()
        title = request.form['title'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()
        linkedin_url = request.form['linkedin_url'].strip()
        notes = request.form['notes'].strip()

        if not contact_name:
            flash("Please include a contact name.")
            return redirect('/contacts')
        
        if email and '@' not in email:
            flash("Please include a valid email format.")
            return redirect('/contacts')
        
        if phone and not phone.replace('-', '').isdigit():
            flash("Please enter a phone number with only dashes or numbers.")
            return redirect('/contacts')
        
        if linkedin_url and 'linkedin' not in linkedin_url:
            flash("Please include a LinkedIn URL.")
            return redirect('/contacts')

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
    db = JobTrackerDB()
    db.connect()

    if request.method == 'POST':
        company_id = request.form['company_id']
        contact_name = request.form['contact_name'].strip()
        title = request.form['title'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()
        linkedin_url = request.form['linkedin_url'].strip()
        notes = request.form['notes'].strip()

        if not contact_name:
            flash("Please include a contact name.")
            return redirect('/contacts')
        
        if email and '@' not in email:
            flash("Please include a valid email format.")
            return redirect('/contacts')
        
        if phone and not phone.replace('-', '').isdigit():
            flash("Please enter a phone number with only dashes or numbers.")
            return redirect('/contacts')
        
        if linkedin_url and 'linkedin' not in linkedin_url:
            flash("Please include a LinkedIn URL.")
            return redirect('/contacts')

        db.edit_contact(company_id, contact_name, title, email, phone, linkedin_url, notes, contact_id)
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

@app.route('/job_match', methods=['GET', 'POST'])
def job_match():
    results = []
    user_skills = []

    if request.method == 'POST':
        skills_input = request.form.get('skills')
        user_skills = [s.strip().lower() for s in skills_input.split(',')]

        db = JobTrackerDB()
        db.connect()
        jobs = db.get_all_jobs()
        db.disconnect()

        for job in jobs:
            job_skills = [s.lower() for s in json.loads(job['requirements'] or "[]")]
            matched = set(user_skills) & set(job_skills)
            missing = set(job_skills) - set(user_skills)
            match_pct = int(len(matched) / len(job_skills) * 100) if job_skills else 0

            results.append({
                'job_title': job['job_title'],
                'company_id': job['company_id'],
                'match_percentage': match_pct,
                'missing_skills': list(missing)
            })

        # Sort highest match first
        results.sort(key=lambda x: x['match_percentage'], reverse=True)

    return render_template('job_match.html', results=results, user_skills=user_skills)
if __name__ == '__main__':
    app.run(debug=True)
