from flask import Flask, render_template, request, redirect, url_for, jsonify, abort;
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jin@localhost:5432/to_do_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)


    def __repr__():
        return f"{self.id}: {self.description}"


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    todos = db.relationship('Todo', backref = 'list')

    def __repr__():
        return f"{self.id}, {self.name}"


@app.route('/todolists/<list_id>')
def get_list_todos(list_id):    
    return render_template('index.html', 
        data = Todo.query.filter_by(list_id = list_id).order_by('id').all(),
        lists=TodoList.query.all(),
        active_list=TodoList.query.get(list_id),
    )


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id = 1))

@app.route('/todos/create', methods=['POST'])
def create_todos():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description)
        active_list = TodoList.query.get(list_id)
        todo.list = active_list
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()       
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        return jsonify(body)
    else:
        abort(400)

@app.route('/todos/<dataId>/set-completed', methods = ['POST'])
def set_completed(dataId):    
    try:
        status = request.get_json()['completed']
        todo = Todo.query.get(dataId)
        todo.completed = status
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todoId>', methods=['delete'])
def set_deleted(todoId):
    try:
        todo = Todo.query.get(todoId)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')