from flask import Flask, render_template, request, jsonify, session
import cx_Oracle
import bcrypt
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hello1YTVP'


def get_connection():
    return cx_Oracle.connect('hr/hr@localhost:1521/xe')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        entered_password = request.form.get('password')
        session['user_email'] = email

        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql = "SELECT EMAIL, USER_PASSWORD FROM CART1 WHERE EMAIL = :3  "
            cursor.execute(sql, (email,))
            user_data = cursor.fetchone()

            if user_data:
                stored_email, stored_password = user_data
                #print(stored_email, stored_password)
                if bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8')):

                    return render_template("index2.html")
                else:
                    return jsonify({'error': 'Invalid email or password'})
            else:
                return jsonify({'error': 'Invalid email or password'})


        except Exception as e:
            return jsonify({'error': str(e)})

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                print("connection closed")

    return render_template("login.html")



@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        address = request.form.get('address')
        email = request.form.get('email')
        pincode = request.form.get('pincode')
        product_name = request.form.get('product_name')
        try:
            con = get_connection()
            cursor = con.cursor()
            num = 1
            sql = "INSERT INTO PAYMENT (NAME, GENDER, ADDS, EMAIL, PIN, PRODUCT) VALUES (:1, :2, :3, :4, :5, :6)"
            print(num)
            num = num + 1
            cursor.execute(sql, (name, gender, address, email, pincode, product_name))

            con.commit()
            print("values inserted")

        except Exception as e:
            return jsonify({'error': str(e)})

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()
                print("connection closed")

        return render_template("index2.html")

    product_name = request.args.get('product_name')
    return render_template("paymentform.html", product_name=product_name)

@app.route('/logout')
def logout():
    return render_template("logout.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('Uname')
        mobile = request.form.get('Mobnum')
        email = request.form.get('Email')
        encpass = request.form.get('pwd')

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(encpass.encode('utf-8'), salt)

        try:
            con = get_connection()
            cursor = con.cursor()

            sql = "INSERT INTO CART1 (UNAME, MOBILE, EMAIL, USER_PASSWORD) VALUES (:1, :2, :3, :4)"
            cursor.execute(sql, (name, mobile, email, hashed_password.decode('utf-8')))

            con.commit()

        except Exception as e:
            return jsonify({'error': str(e)})


        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()
                print("connection closed")
        return render_template("login.html")

    return render_template("signup.html")

@app.route('/delete')
def delete():
    try:
        email = session.get('user_email')
        if email:
            # Perform the DELETE query to delete records from the database.
            con = get_connection()
            cursor = con.cursor()

            # Assuming 'CART1' is the table name and 'email' is the column to match.
            sql = "DELETE FROM CART1 WHERE email = :email"
            cursor.execute(sql, email=email)

            con.commit()
            con.close()

            return render_template("index.html")
        else:
            return jsonify({'email': email})


    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)