import mysql.connector
from mysql.connector import Error

class JobTrackerDB:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'YOUR_PASSWORD',
            'database': 'job_tracker_project'
        }
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return True
        except Error as e:
            print(f'Connection error: {e}')
            return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def get_all_companies(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM companies')
        return cursor.fetchall()
    
    def insert_company(self, company_name, industry, website, city, state, notes):
        cursor = self.connection.cursor(dictionary=True)
        insert_query = '''
            INSERT INTO companies (company_name, industry, website, city, state, notes)
            VALUES(%s, %s, %s, %s, %s, %s)
        '''
        values = (company_name, industry, website, city, state, notes)
        cursor.execute(insert_query, values)
        self.connection.commit()
        print(f'Company added successfully!')
        print(f'New company ID: {cursor.lastrowid}')

    def edit_company(self, company_name, industry, website, city, state, notes, company_id):
        cursor = self.connection.cursor(dictionary=True)
        edit_query = '''
            UPDATE companies 
            SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s
            WHERE company_id = %s
        '''
        values = (company_name, industry, website, city, state, notes, company_id)
        cursor.execute(edit_query, values)
        self.connection.commit()
        print(f'Company edited successfully!')
    
    def delete_company(self, company_id):
        cursor = self.connection.cursor(dictionary=True)
        delete_query = '''
            DELETE FROM companies 
            WHERE company_id = %s
        '''
        cursor.execute(delete_query, (company_id,))
        self.connection.commit()
        print(f'Company deleted successfully!')

    def get_jobs_by_salary(self, min_salary):
        cursor = self.connection.cursor(dictionary=True)
        query = 'SELECT * FROM jobs WHERE salary_min >= %s'
        cursor.execute(query, (min_salary,))
        return cursor.fetchall()
    
    def get_all_applications(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM applications')
        return cursor.fetchall()

    def get_all_jobs(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jobs')
        return cursor.fetchall()
    
    def get_all_contacts(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM contacts')
        return cursor.fetchall()

    def insert_application(self, application_date, status, resume_version, cover_letter_sent, interview_data, job_id):
        cursor = self.connection.cursor(dictionary=True)
        insert_query = '''
            INSERT INTO applications (application_date, status, resume_version, cover_letter_sent, interview_data, job_id)
            VALUES(%s, %s, %s, %s, %s, %s)
        '''
        values = (application_date, status, resume_version, cover_letter_sent, interview_data, job_id)
        cursor.execute(insert_query, values)
        self.connection.commit()
        print(f'Application added successfully!')
        print(f'New application ID: {cursor.lastrowid}')    
    
    def edit_application(self, application_date, status, resume_version, cover_letter_sent, interview_data, application_id):
        cursor = self.connection.cursor(dictionary=True)
        edit_query = '''
            UPDATE applications 
            SET application_date = %s, status = %s, resume_version = %s, cover_letter_sent = %s, interview_data = %s
            WHERE application_id = %s
        '''
        values = (application_date, status, resume_version, cover_letter_sent, interview_data, application_id)
        cursor.execute(edit_query, values)
        self.connection.commit()
        print(f'Application edited successfully!')

    def delete_application(self, application_id):
        cursor = self.connection.cursor(dictionary=True)
        delete_query = '''
            DELETE FROM applications 
            WHERE application_id = %s
        '''
        cursor.execute(delete_query, (application_id,))
        self.connection.commit()
        print(f'Application deleted successfully!')

    def insert_job(self, date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, company_id):
        cursor = self.connection.cursor(dictionary=True)
        insert_query = '''
            INSERT INTO jobs (date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, company_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, company_id)
        cursor.execute(insert_query, values)
        self.connection.commit()
        print(f'Job added successfully!')
        print(f'New job ID: {cursor.lastrowid}')    
    
    def edit_job(self, date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, job_id):
        cursor = self.connection.cursor(dictionary=True)
        edit_query = '''
            UPDATE jobs 
            SET date_posted = %s, job_title = %s, job_type = %s, salary_min = %s, salary_max = %s, job_url = %s, requirements = %s
            WHERE job_id = %s
        '''
        values = (date_posted, job_title, job_type, salary_min, salary_max, job_url, requirements, job_id)
        cursor.execute(edit_query, values)
        self.connection.commit()
        print(f'Job edited successfully!')

    def delete_job(self, job_id):
        cursor = self.connection.cursor(dictionary=True)
        delete_query = '''
            DELETE FROM jobs 
            WHERE job_id = %s
        '''
        cursor.execute(delete_query, (job_id,))
        self.connection.commit()
        print(f'Job deleted successfully!')
    
    def insert_contact(self, contact_name, title, email, phone, linkedin_url, notes, company_id):
        cursor = self.connection.cursor(dictionary=True)
        insert_query = '''
            INSERT INTO contacts (contact_name, title, email, phone, linkedin_url, notes, company_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        '''
        values = (contact_name, title, email, phone, linkedin_url, notes, company_id)
        cursor.execute(insert_query, values)
        self.connection.commit()
        print(f'Contact added successfully!')
        print(f'New contact ID: {cursor.lastrowid}') 

    def edit_contact(self, contact_name, title, email, phone, linkedin_url, notes, contact_id):
        cursor = self.connection.cursor(dictionary=True)
        edit_query = '''
            UPDATE contacts 
            SET contact_name = %s, title = %s, email = %s, phone = %s, linkedin_url = %s, notes = %s
            WHERE contact_id = %s
        '''
        values = (contact_name, title, email, phone, linkedin_url, notes, contact_id)
        cursor.execute(edit_query, values)
        self.connection.commit()
        print(f'Contact edited successfully!')

    def delete_contact(self, contact_id):
        cursor = self.connection.cursor(dictionary=True)
        delete_query = '''
            DELETE FROM contacts 
            WHERE contact_id = %s
        '''
        cursor.execute(delete_query, (contact_id,))
        self.connection.commit()
        print(f'Contact deleted successfully!')