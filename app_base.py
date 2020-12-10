from flask import Flask
from flask import url_for, render_template, request, redirect
from models import db, User, Answers, Questions
from sqlalchemy import func
import sqlite3
con = sqlite3.connect('Gaming.bd')
cur = con.cursor()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Gaming.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cur.execute("""CREATE TABLE IF NOT EXISTS User (
   userid INT PRIMARY KEY,
   gender TEXT);
""")
con.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS Question (
   q_id INT PRIMARY KEY,
   quest TEXT);
""")
con.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS Answer (
   a_id INT PRIMARY KEY,
   answ TEXT);
""")
con.commit()
db.app = app
db.init_app(app)


@app.route("/")
def show_base():
    return render_template("base.html")

@app.route("/statistica")
def show_stat():
    return render_template("statistic.html")

@app.route("/opros")
def show_questionnaire():
    return render_template("opros.html")


@app.route("/opros")
def getting_res():
    if request.values:
        gender = request.values.get('gend')
        user = User(gender=gender)
        # добавляем в базу
        db.session.add(user)
        # сохраняемся
        db.session.commit()
        # получаем юзера с айди (автоинкремент)
        db.session.refresh(user)
        q1 = request.values.get('sup_plot')
        q2 = request.values.get('sup_pers')
        q3 = request.values.get('sup_pr')
        q4 = request.values.get('up_as')
        q5 = request.values.get('sup_gr')
        q6 = request.values.get('sup_di')

        # привязываем к пользователю (см. модели в проекте)
        answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6)
        # добавляем ответ в базу
        db.session.add(answer)
        # сохраняемся
        db.session.commit()

    return 'Ok'


@app.route('/statistica')
def stats():
    all_info = {}
    gen_stats = db.session.query(
        func.count(User.gender)
    ).one()
    all_info['total_count'] = User.query.count()
    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0]
    q1_answers = db.session.query(Answers.q1).all()
    return render_template('statistic.html', all_info=all_info)


if __name__ == '__main__':
    app.run(debug=False)


