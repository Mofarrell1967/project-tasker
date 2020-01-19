import os
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'project-tracker'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("task.html", 
                           tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
                           projects=mongo.db.projects.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.projects.find()
    return render_template('edittask.html', task=the_task,
                           projects=all_projects)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'project_name':request.form.get('project_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_projects')
def get_categories():
    return render_template('projects.html',
                           projects=mongo.db.projects.find())


@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    mongo.db.projects.remove({'_id': ObjectId(project_id)})
    return redirect(url_for('get_projects'))


@app.route('/edit_project/<project_id>')
def edit_project(project_id):
    return render_template('editproject.html',
    project=mongo.db.projects.find_one({'_id': ObjectId(project_id)}))


@app.route('/update_project/<project_id>', methods=['POST'])
def update_project(project_id):
    mongo.db.projects.update(
        {'_id': ObjectId(project_id)},
        {'project_name': request.form.get('project_name')})
    return redirect(url_for('get_projects'))


@app.route('/insert_project', methods=['POST'])
def insert_project():
    project_doc = {'project_name': request.form.get('project_name')}
    mongo.db.projects.insert_one(project_doc)
    return redirect(url_for('get_projects'))


@app.route('/add_project')
def add_project():
    return render_template('addproject.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)