from flask import Flask , request ,render_template ,redirect
import sqlite3


app=Flask(__name__)

def start_db():
    conn=sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("""   
                   CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT , email TEXT UNIQUE , password TEXT 
                   )
                   """)
    conn.commit()
    conn.close()
    
start_db()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method =="POST":
        
        email = request.form["email"]
        password = request.form["password"]
        conn=None
        try:
            conn = sqlite3.connect("database/users.db")
            cursor = conn.cursor()
            cursor.execute(
            "INSERT INTO users ( email , password ) VALUES (?,?)",(email,password)
            )
            conn.commit()
            
            
        except sqlite3.IntegrityError:
            return "email already exists"
        
        except Exception as e :
            return f"something went wrong:{e}"
        
        finally:
            if conn:
                conn.close()
        
        return redirect("/login")
    
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]
        
        conn=None
        try:
            
            conn = sqlite3.connect("database/users.db")
            cursor = conn.cursor()
            cursor.execute("select * from users where email = ? ",(email,))
            user = cursor.fetchone()
            if user:
                if user[2]==password:
                    return redirect("/dashboard")
            
                else :
                   return "invalid password "   
            else:
                return "invalid email"
            
        except Exception as e :
            return f"something went wrong:{e}"
        
        finally:
            if conn:
                conn.close()
            
        
        
          
       
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True)

        
        
    
    

