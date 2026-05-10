A simple web app where users can create an account, log in, and access a basic dashboard.
I built this to learn how user authentication works in real projects.
#Login-authentication-system

## What This Project Does

- User can **sign up** with name, email and password
- User can **log in** with their credentials
- Passwords are **not stored directly** — bcrypt is used to hash them before saving
- After login, user is redirected to a **simple dashboard**
- All user data is stored in **MySQL database**

## Tech Used

- Python (Flask)
- MySQL
- bcrypt (for password hashing)
- HTML & CSS (for frontend)
- Jinja2 (Flask templating)

## Why I Made This

I wanted to understand how login systems actually work behind the scenes —
like how passwords are stored safely 
This is one of my first backend projects.

