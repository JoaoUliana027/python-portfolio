from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()

    # Filtros
    status_filter = request.args.get("status", "all")
    search_query = request.args.get("search", "").lower()

    if status_filter == "done":
        tasks = [t for t in tasks if t["done"]]
    elif status_filter == "pending":
        tasks = [t for t in tasks if not t["done"]]

    if search_query:
        tasks = [t for t in tasks if search_query in t["title"].lower()]

    return render_template("index.html", tasks=tasks, status_filter=status_filter, search_query=search_query)

@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()
    new_task = {
        "title": request.form["title"],
        "done": False,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect("/")

@app.route("/toggle/<int:task_index>")
def toggle_task(task_index):
    tasks = load_tasks()
    tasks[task_index]["done"] = not tasks[task_index]["done"]
    save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:task_index>")
def delete_task(task_index):
    tasks = load_tasks()
    tasks.pop(task_index)
    save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
