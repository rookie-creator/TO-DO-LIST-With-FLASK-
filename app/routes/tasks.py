from flask import Blueprint ,render_template ,url_for,session,redirect,flash,request
from app import db
from app.models import Task


task_bp =Blueprint('tasks',__name__)

@task_bp.route('/')
def view_tasks():
    if 'user_id' not in session:
        flash("Please login to view your tasks", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    print("Fetched tasks:", tasks)# Only current user's tasks
    return render_template('tasks.html', tasks=tasks)

@task_bp.route('/add',methods=["POST"])
def add_task():
    if 'user_id' not in session:
        flash("please login first ","warning")
        return redirect(url_for('auth.login'))
    
    title =request.form.get('title')
    if title:
        task =Task(title=title,user_id=session['user_id'])
        db.session.add(task)
        db.session.commit()
        print("Task added:", title)
        flash('Task Added Succesfully','success')
        print("Task added:", title)

    return redirect(url_for('tasks.view_tasks'))


@task_bp.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 'user_id' not in session:
        flash("Login required", "warning")
        return redirect(url_for('auth.login'))

    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        flash("Unauthorized to delete this task", "danger")
        return redirect(url_for('tasks.view_tasks'))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully", "info")
    return redirect(url_for('tasks.view_tasks'))

@task_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    if 'user_id' not in session:
        flash("Login required", "warning")
        return redirect(url_for('auth.login'))

    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        flash("You cannot modify others' tasks", "danger")
        return redirect(url_for('tasks.view_tasks'))

    if task.status == 'pending':
        task.status = 'working'
    elif task.status == 'working':
        task.status = 'done'
    else:
        task.status = 'pending'

    db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


@task_bp.route('/clear',methods=["POST"])
def clear_tasks():
    if 'user_id' not in session:
        flash("Login required", "warning")
        return redirect(url_for('auth.login'))

    Task.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash("All your tasks cleared", "info")
    return redirect(url_for('tasks.view_tasks'))    
    
