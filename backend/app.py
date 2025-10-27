from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
import uuid
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.json'

tasks = {}
comments = {}


def load_data():
    global tasks, comments
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                tasks = data.get('tasks', {})
                comments = data.get('comments', {})
                print(f"Loaded {len(tasks)} tasks and {len(comments)} comments from {DATA_FILE}")
        except Exception as e:
            print(f"Error loading data: {e}")
            tasks = {}
            comments = {}
    else:
        print(f"No data file found, starting with empty storage")


def save_data():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({'tasks': tasks, 'comments': comments}, f, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")


load_data()


def get_comments_by_task(task_id):
    return [comment for comment in comments.values() if comment['task_id'] == task_id]


@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(list(tasks.values())), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task_id = str(uuid.uuid4())
    task = {
        'id': task_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    
    tasks[task_id] = task
    save_data()
    return jsonify(task), 201


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task), 200


@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = tasks.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        if not data['title'].strip():
            return jsonify({'error': 'Title cannot be empty'}), 400
        task['title'] = data['title']
    
    if 'description' in data:
        task['description'] = data['description']
    
    save_data()
    return jsonify(task), 200


@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = tasks.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    deleted_task = tasks.pop(task_id)
    
    task_comment_ids = [c_id for c_id, c in comments.items() if c['task_id'] == task_id]
    for c_id in task_comment_ids:
        comments.pop(c_id)
    
    save_data()
    return jsonify({
        'message': 'Task deleted successfully',
        'task': deleted_task
    }), 200


@app.route('/api/tasks/<task_id>/comments', methods=['POST'])
def create_comment(task_id):
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400
    
    if not data['content'].strip():
        return jsonify({'error': 'Content cannot be empty'}), 400
    
    comment_id = str(uuid.uuid4())
    comment = {
        'id': comment_id,
        'task_id': task_id,
        'content': data['content'],
        'author': data.get('author', 'Anonymous'),
        'created_at': datetime.now(timezone.utc).isoformat(),
        'updated_at': datetime.now(timezone.utc).isoformat()
    }
    
    comments[comment_id] = comment
    save_data()
    return jsonify(comment), 201


@app.route('/api/tasks/<task_id>/comments', methods=['GET'])
def get_comments(task_id):
    task_comments = get_comments_by_task(task_id)
    task_comments.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({
        'task_id': task_id,
        'comments': task_comments,
        'count': len(task_comments)
    }), 200


@app.route('/api/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = comments.get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    return jsonify(comment), 200


@app.route('/api/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = comments.get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'content' in data:
        if not data['content'].strip():
            return jsonify({'error': 'Content cannot be empty'}), 400
        comment['content'] = data['content']
    
    if 'author' in data:
        comment['author'] = data['author']
    
    comment['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    save_data()
    return jsonify(comment), 200


@app.route('/api/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = comments.get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    deleted_comment = comments.pop(comment_id)
    save_data()
    
    return jsonify({
        'message': 'Comment deleted successfully',
        'comment': deleted_comment
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
