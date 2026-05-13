import os

import bcrypt
import mysql.connector
from flask import Flask, redirect, render_template, request
from mysql.connector import Error


app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("MYSQLHOST") or os.getenv("MYSQL_HOST") or "localhost",
    "user": os.getenv("MYSQLUSER") or os.getenv("MYSQL_USER") or "root",
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("MYSQL_PASSWORD") or "",
    "database": os.getenv("MYSQLDATABASE") or os.getenv("MYSQL_DATABASE") or "user_login_db",
}

db_port = os.getenv("MYSQLPORT") or os.getenv("MYSQL_PORT")
if db_port:
    DB_CONFIG["port"] = int(db_port)


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)





def start_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


start_db()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        password_bytes = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

       
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password),
            )
            conn.commit()

        except mysql.connector.IntegrityError:
            return "email already exists "

        except Error as error:
            return f"something went wrong:{error}"

        finally:
            if conn:
                conn.close()

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, email, password FROM users WHERE email = %s",
                (email,),
            )
            user = cursor.fetchone()
            if user:
                hashed_password = user[3].encode("utf-8")
                login_password_bytes = password.encode("utf-8")
                if bcrypt.checkpw(login_password_bytes, hashed_password):
                    
                    
                    conn.commit()
                    return redirect("/dashboard")

                return "invalid password "
            else:
                return "invalid email"

        except Error as e:
            return f"something went wrong:{e}"

        finally:
            if conn:
                conn.close()

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
