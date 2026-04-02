#AI Usage Documentation

##Tools Used
-ChatGPT (free version)

##Key Prompts
Can you give me a plain base.html that imports Bootstrap to start off with?”
How do I go about connecting Flask to MySQL using MySQL.connector? I don’t have much experience with Flask so please explain it simply and guide me on how to create Flask routes.
Can you help me with companies.html by creating a form to edit a company? Also, can you edit the companies.html so I can display all companies below the add companies form?
Can you help me convert my company_id text boxes so that they display a drop down of the different company id’s?
Can you help me with the Job Match feature?

##What Worked Well
It gave me a concise base.html where I could add on the rest of the pages as I completed them.
It gave me a great base for the Company page, that I could modify later according to the needs of the project. It was also reusable for the rest of the necessary pages.
It was able to help me better understand Flask and its role in the project, as well as how to create Flask routes.

##What I modified
I changed the colors of things like the navigation bar.
I added the Company ID column to the table displaying company records so that it would be more complete/thorough, and did the same for other tables and their respective ID’s.
I changed the html types of input boxes so that they better matched up with the database.
Refined forms to meet requirements, such as adding the ability to edit company id’s in the contacts form.

##Lessons Learned
Ask it for help on general or broad problems, attempt it yourself, and when you get stuck keep asking follow-up questions to debug and understand where you went wrong, or what you’re missing. For the first response it gives, you will likely need a lot of back-and-forth to get it working and integrated with the rest of your project, so don’t just use the code all at once and expect it to work.
Take some time to double-check that everything is syncing up correctly with your database. I had an issue where when I would hit the back button or refresh, and it would re-insert whatever was in the form at the time, leading to multiple duplicate companies in my company table in the database. It was a simple one line fix but could’ve caused a lot of discrepancies if left alone.
Review your code to double check that you meet the necessary requirements, it will likely give you more generalized help and you will need to go back and either add things you’re missing, or remove unnecessary features. 
