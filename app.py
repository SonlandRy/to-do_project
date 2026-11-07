from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)

class Task:
    def __init__(self, task_id: int, text: str, done: bool = False):
        self.id = task_id
        self.task = text
        self.done = done

    def toggle(self):
        self.done = not self.done


class TaskManager:
    def __init__(self):
        self.todos = [
            Task(1, "Buy pizza", done=False),
            Task(2, "Learn Flask development", done=True)
        ]

    def add_task(self, text: str):
        if not text:
            return
        new_id = self.todos[-1].id + 1 if self.todos else 1
        new_task = Task(new_id, text)
        self.todos.append(new_task)

    def delete_task(self, task_id: int):
        self.todos = [t for t in self.todos if t.id != task_id]

    def toggle_task(self, task_id: int):
        for t in self.todos:
            if t.id == task_id:
                t.toggle()
                break


manager = TaskManager()

@app.route('/')
def index():
    return render_template('index.html', todos=manager.todos)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    manager.add_task(task_text)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    manager.delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    manager.toggle_task(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
