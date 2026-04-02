# Job Application Tracker

A web application to help track job applications during the job search process.

## Features
- Track companies and job listings
- Record application submissions
- Manage interview schedules
- Store contact information

## Technologies
- MySQL Database
- Python with Flask
- HTML/CSS for the web interface

## IMPORTANT SETUP INSTRUCTIONS
1. Clone from GitHub Repository for example:
    git clone https://github.com/fportobanco/job-application-tracker.git job_tracker_example
    cd job_tracker_example
2. Create your database in MySQL Workbench, make sure your server is running beforehand and execute the following:
    SOURCE schema.sql;
3. Remember to edit your database.py and replace ‘YOUR_PASSWORD’ with your own MySQL password.
4. Install the requirements:
    pip install -r requirements.txt
5. Run it
    python app.py
6. Go to the following on your browser:
    http://127.0.0.1:5000/
