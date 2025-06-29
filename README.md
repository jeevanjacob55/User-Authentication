# User-Authentication

## Overview

This is a simple user authentication system built using Flask. It supports user registration, login, logout, and a protected page that is accessible only to logged-in users. Additionally, authenticated users can download a protected file.

## Features

* User Registration with hashed password storage
* Secure Login and Logout
* Protected route (`/secrets`) accessible only to logged-in users
* File download route protected by login
* Flash messages for feedback (e.g., duplicate emails, incorrect credentials)

## Technologies Used

* Flask
* Flask SQLAlchemy
* Flask-Login
* Werkzeug for password hashing
* SQLite database

## File Structure

```
project/
├── main.py
├── users.db
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── secrets.html
├── static/
│   └── files/
│       └── cheat_sheet.pdf
```

## Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Set Up Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Application**

```bash
python main.py
```

5. **Access the App**
   Visit `http://127.0.0.1:5000/` in your browser.

## Routes

### `/`

* Home page.

### `/register`

* Allows new users to register.

### `/login`

* Existing users can log in.

### `/logout`

* Logs out the current user.

### `/secrets`

* Protected page accessible only after logging in.

### `/download`

* Protected file download endpoint.

## Security Notes

* Passwords are hashed using Werkzeug's `generate_password_hash`.
* User sessions are managed securely using Flask-Login.
