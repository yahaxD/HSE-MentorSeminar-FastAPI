# 📝 Todo Manager
## Project Description

Welcome to the ToDo manager, developed using FastAPI and SQLAlchemy. This application allows users to create, update, delete, and manage tasks.

## 🚀 Features

- Create new tasks
- Retrieve all tasks
- Retrieve a specific task by ID
- Get lists of completed and incomplete tasks
- Search tasks by title and/or description
- Update task details
- Update task completion status
- Delete tasks
- Get statistics on tasks

## 🛠 Technologies

- **Backend**: FastAPI
- **Database**: SQLAlchemy
- **Language**: Python 3.9+
- **Validation**: Pydantic

## Endpoints
 
* Root Information
  
	**GET /**

	*Returns information about the app and available endpoints.*
	
* Create a New Task
  
	**POST /item**

	Request Body: 
	
	```json
		{
			"title": "Task title",
			"description": "Optional task description",
			"completed": false
		}
	```
	
	*Creates a new task with the specified title, description, and status.*
	
* List All Tasks
  
	**GET /items**

	*Returns a list of all tasks.*

* Get Task Details
  
	**GET /item/{item_id}**

  	*Fetches details of a task by its ID.*
	
* List Incomplete Tasks
  
	**GET /items/incomplete**

	*Returns a list of all tasks that are not marked as completed.*

* List Completed Tasks
  
	**GET /items/completed**

	*Returns a list of all tasks that are marked as completed.*
	
* Task Statistics
  
	**GET /items/stats**

	*Returns statistics including the total number of tasks, completed tasks, and incomplete tasks.*

* Search Tasks
  
	**GET /items/search**
	
	Query Parameters:

	- title: (Optional) Search for tasks containing this title.
	- description: (Optional) Search for tasks containing this description.
	
	*Returns a list of tasks based on the title and/or description.*
	
* Update a Task
  
	**PUT /item/{item_id}**

	```json
		{
			"title": "Updated title",
			"description": "Updated description",
			"completed": true
		}
	```

	*Updates the details of a specific task by its ID.*
	
* Update Task Completion Status
  
	**PATCH /item/{item_id}/status**

	Query Parameters:
	
	- completed: (Boolean) The new completion status of the task.
	
	*Updates the completion status of a task by its ID.*

* Delete a Task
  
	**DELETE /item/{item_id}**

	*Deletes a specific task by its ID.*	
	
See full documentaion on ***http://localhost/docs***

<div align="center">
    <img alt="image" src="https://github.com/user-attachments/assets/a447daf6-ce84-4ae2-beb6-8cdb4a194bc9" width="960">
</div>
	
## 📦 Installation

### Via GitHub

1. **Clone the Repository**

	```bash
	git clone https://github.com/yahaxD/HSE-MentorSeminar-FastAPI/tree/main
	cd todo_app
	```

2.  **Using Docker**

   2.1 **Build Docker Image**

	```bash
	docker build -t todo-service:latest todo_app/  
	```
	
	2.2 **Run Docker Image**
	
	```bash
	docker run -d -p 8000:80 -v todo_data:/app/data --name todo-service todo-service:latest
	```

2.  **Without Docker**

	2.1 **Create Virtual Environment**

	```bash
	python3 -m venv venv
	source venv/bin/activate  # For Linux/macOS
	# or
	source venv\Scripts\activate  # For Windows
	```
	
	2.2 **Install Dependencies**
	
	```bash
	pip install -r requirements.txt
	```
	
	2.3 **Run the Application**
	
	```bash
	uvicorn main:app --host 0.0.0.0 --port 80 --reload
	```

3. **Access the application**
   
   Go to the address: ***http://localhost:80*** .


### Via DockerHub

1. **Clone and Run the Image**

	```bash
	docker run -d -p 8000:80 -v todo_data:/app/data --name todo-service yahaxd/todo-service:latest
	```

2. **Access the application**
   
   Go to the address: ***http://localhost:80*** .

## License

This project is licensed under the MIT License.
