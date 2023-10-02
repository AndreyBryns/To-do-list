from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Task

main = Blueprint('main', __name__)

@main.route('/home')
@login_required
def home():
    todo_list = Task.query.filter_by(user_id = current_user.get_id(), type="todo")
    done_list = Task.query.filter_by(user_id = current_user.get_id(), type="done")
    failed_list = Task.query.filter_by(user_id = current_user.get_id(), type="failed")
    return render_template("home.html", todo_list = todo_list, done_list = done_list, failed_list = failed_list)

@main.route('/home', methods=['POST'])
@login_required
def home_post():
    if 'inputTask' in request.form:
        description = request.form.get('inputTask')
        new_task = Task(user_id=current_user.get_id(), type="todo", description=description)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('main.home'))
    if 'taskToDelete' in request.form:
        id = request.form.get('taskToDelete')
        task = Task.query.filter_by(id=id)
        if task:
            task.delete()
            db.session.commit()
        return redirect(url_for('main.home'))
    if 'taskToDone' in request.form:
        id = request.form.get('taskToDone')
        task = db.session.query(Task).get(id)
        if task:
            task.type = 'done'
            db.session.commit()
        return redirect(url_for('main.home'))
    if 'taskToFail' in request.form:
        id = request.form.get('taskToFail')
        task = db.session.query(Task).get(id)
        if task:
            task.type = "failed"
            db.session.commit()
        return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))

@main.route('/')
@login_required
def main_page():
    return redirect(url_for('main.home'))