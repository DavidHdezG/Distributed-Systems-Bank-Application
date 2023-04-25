# Distributed Systems Bank Application 
## Description
This is a simplified distributed banking application that allows users to create accounts, ask for a lean and wait until it's approved. A staff user can approve or reject the lean, see the list of leans, and see/create branches. The app is implemented using Django and two Oracle database containers connected using Docker to emulate a distributed system.

## How to run
1. Clone the repository
2. Migrate the database using `python manage.py migrate`
3. Run the server using `python manage.py runserver`
4. Open the browser and go to `localhost:8000`

## How to use
1. Create a user account
2. Login using the created account
3. Create a lean
4. Login using a staff account
5. Approve or reject the lean
6. Create a branch
7. See the list of leans
8. Logout