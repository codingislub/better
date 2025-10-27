# Task Manager (Full-Stack Application)

A minimal full-stack application with separated backend and frontend:
- **Backend:** Task & Comment CRUD APIs (Flask)
- **Frontend:** Task CRUD interface (React + TypeScript + Vite)

---

## Features

**Backend APIs:**
- Task CRUD: Create, read, update, delete tasks (REST API)
- Comment CRUD: Add, edit, delete, view comments for tasks (REST API)
- Cascade delete: Deleting a task removes all associated comments

**Frontend Interface:**
- Task CRUD: Add, edit, delete, view tasks (UI)
- Clean, responsive design with error handling

**Note:** Backend provides both task and comment endpoints. Frontend currently uses task endpoints for the UI.

---

## Prerequisites

- Windows 10/11
- Node.js 18+ (includes npm)
- Python 3.10+ (recommended 3.12)

---

## Quick Start

Windows one‑liners (PowerShell):

```powershell
# Backend
cd d:\better\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
python app.py
```

```powershell
# Frontend (separate terminal)
cd d:\better\front
npm install
npm run dev
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

If you prefer scripts, use `start-backend.bat` and `start-frontend.bat` from the root.

---

## Project Structure

```
better/
├─ backend/               # Flask REST API - Task & Comment CRUD
│  ├─ app.py             # Task & Comment endpoints
│  ├─ requirements.txt   # Python deps
│  ├─ test_app.py        # 27 automated tests
│  └─ data.json          # Persistent storage (auto-generated)
├─ front/                # React + TS + Vite - Task CRUD UI
│  ├─ index.html         # Vite entry HTML
│  ├─ public/            # Static assets
│  ├─ src/
│  │  ├─ api.ts          # Task API client
│  │  ├─ App.tsx         # Main app (task management)
│  │  ├─ types.ts        # Task types
│  │  └─ components/     # Task UI components
│  │     ├─ Header.tsx   # App header
│  │     ├─ TaskList.tsx # Task list view
│  │     ├─ TaskForm.tsx # Add/edit task form
│  │     └─ TaskDetail.tsx # View task details
│  └─ vite.config.ts     # Dev proxy → http://localhost:5000
└─ README.md             # This file
```

---

## Backend API Summary

**Purpose:** Task & Comment CRUD operations with JSON file persistence

Base path: `/api`

**Task Endpoints:**
- GET `/api/tasks` – list all tasks
- POST `/api/tasks` – create new task
- GET `/api/tasks/{task_id}` – get specific task
- PUT `/api/tasks/{task_id}` – update task
- DELETE `/api/tasks/{task_id}` – delete task (cascades to comments)

**Comment Endpoints:**
- POST `/api/tasks/{task_id}/comments` – create comment
- GET `/api/tasks/{task_id}/comments` – list all comments for a task
- GET `/api/comments/{comment_id}` – get specific comment
- PUT `/api/comments/{comment_id}` – update comment (content/author)
- DELETE `/api/comments/{comment_id}` – delete comment

**Utility:**
- GET `/api/health` – health check

---

## Frontend UI Summary

**Purpose:** Task CRUD interface

**Task Operations:**
- ✅ View all tasks in a list
- ✅ Create new tasks (title + description)
- ✅ Edit existing tasks
- ✅ Delete tasks (with confirmation)
- ✅ View task details

**Components:**
- Header: App title and "New Task" button
- TaskList: List of all tasks with edit/delete actions
- TaskForm: Form to add or edit tasks
- TaskDetail: View full task information

---

## Architecture Notes

- Backend and frontend have **separate responsibilities**
  - Backend: Comment API (stores and manages comments)
  - Frontend: Task UI (stores and manages tasks in frontend state)
- `task_id` in backend is just a reference string
- No direct integration between task and comment features
- CORS enabled; Vite dev proxy forwards `/api` to Flask on port 5000

---

## Testing (backend)

```powershell
cd d:\better\backend
.\.venv\Scripts\Activate.ps1
pytest test_app.py -v
```

22 automated tests covering comment CRUD and validation.

---

## Troubleshooting

- Frontend shows "Failed to fetch tasks" → Start backend on port 5000.
- Python not found → install from https://www.python.org/downloads/windows/ and check "Add python.exe to PATH". Reopen PowerShell.
- Policy blocks venv activation →
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- Port conflict → change `app.run(..., port=5000)` in backend/app.py and update `vite.config.ts` proxy.

---

## License

MIT (for demo purposes)

## Error Responses

The API uses standard HTTP status codes:

- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found

Error response format:
```json
{
  "error": "Error message description"
}
```

## Project Structure

```
better/
├── app.py              # Main Flask application
├── test_app.py         # Automated tests
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Data Storage

Currently uses in-memory storage (dictionaries). In production, you would replace this with a database like:
- PostgreSQL
- MySQL
- MongoDB
- SQLite

## Future Enhancements

- [ ] Database integration (PostgreSQL/MySQL)
- [ ] User authentication and authorization
- [ ] Comment threading (replies to comments)
- [ ] Comment reactions/likes
- [ ] Pagination for large comment lists
- [ ] Search and filter capabilities
- [ ] Rate limiting
- [ ] API documentation with Swagger/OpenAPI
# better
