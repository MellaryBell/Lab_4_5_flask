from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)
conn = psycopg2.connect(database="service",
                        user="postgres",
                        password="12345",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')

            if len(username) == 0:
                return 'Введите имя пользователя'
            if len(password) == 0:
                return 'Введите пароль'
            try:
                cursor.execute("SELECT name FROM public.users WHERE login=%s AND password=%s", (str(username),
                                                                                                str(password)))
                records = cursor.fetchall()[0]
            except TypeError:
                return render_template('er.html')
            return render_template('account.html', full_name=records)
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if len(name)==0:
            return 'Введите имя пользователя'
        elif [a for a in name if a in '1234567890!@#$%^&*()_']:
            return 'Имя должно состоять тользко из букв'
        elif len(login)==0:
            return 'Вы не ввели логин'
        elif len(password)==0:
            return 'Вы не ввели пароль'
        if login:
            cursor.execute('SELECT * FROM public.users')
            rows = cursor.fetchall()
            for row in rows:
                print (row[1])
                if login == row[1]:
                    return render_template('already.html')

        cursor.execute('INSERT INTO public.users (name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html')
app.run(debug=True)