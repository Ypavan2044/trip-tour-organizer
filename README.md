# Trip Tour Organizer and Booking Management System

Console-based tour management and booking system built with **Python, PyMySQL, and MySQL**.

## Technologies
Python, PyMySQL, MySQL, SQL, bcrypt.

## Features
### Admin
- Add, view, update, and delete tours
- View customer bookings

### Viewer
- View available tours
- Search tours
- View tour details
- Book tours
- View personal bookings
- Cancel bookings
- Automatic seat management

## Main Database Tables
1. `users`
2. `tours`
3. `bookings`

## Setup
1. Install Python.
2. Run `pip install -r requirements.txt`
3. Run `schema.sql` in MySQL Workbench.
4. In `db.py`, replace `YOUR_MYSQL_PASSWORD` with your local MySQL password.
5. Run `python app.py`

New registrations are viewers by default. To create an admin:
```sql
UPDATE users SET role='admin' WHERE email='admin@gmail.com';
```

**Never upload your real MySQL password to GitHub.**
