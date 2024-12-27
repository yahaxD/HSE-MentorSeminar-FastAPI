# 🔗 URL Shortener Service

## Project Description

A simple and efficient service for shortening long URLs using FastAPI and SQLAlchemy. Transform complex, lengthy web addresses into concise, manageable links.

## 🚀 Features

- Create short links from long URLs
- Redirect to original URLs
- View all shortened URLs
- Get short link information
- Delete shortened links

## 🛠 Technologies

- **Backend**: FastAPI
- **Database**: SQLAlchemy
- **Language**: Python 3.9+
- **Validation**: Pydantic

## Endpoints
 
* Root Information
  
	**GET /**

	*Returns information about the app and available endpoints.*
	
* Shorten a URL
  
	**POST /shorten**

	Request Body: {"url": "https://example.com"}

	*Accepts a full URL and returns the shortened URL.*
	
* Redirect to Full URL
  
	**GET /{short_id}**

	*Redirects to the original URL.*

* Get Information for a Short URL
  
	**GET /stats/{short_id}**

  	*Returns short identifier and the original full URL.*
	
* List All URLs
  
	**GET /urls/all**

	*Returns a list of all short URLs and their full URLs.*

* Delete a Short URL
  
	**DELETE /delete/{short_id}**

	*Deletes a specific short URL.*
	
See full documentaion on ***http://localhost/docs***

<div align="center">
    <img alt="image" src="https://github.com/user-attachments/assets/00572278-1deb-4446-a5ba-17e0c251fd97" width="960">
</div>
	
## 📦 Installation

### Via GitHub

1. **Clone the Repository**

	```bash
	git clone https://github.com/yahaxD/HSE-MentorSeminar-FastAPI/tree/main
	cd shorturl_app
	```

#####  **Using Docker**
2.1 **Build Docker Image**

	```bash
	docker build -t shorturl-service:latest shorturl_app/  
	```
	
2.2 **Run Docker Image**
	
	```bash
	docker run -d -p 8001:80 -v shorturl_data:/app/data --name shorturl-service shorturl-service:latest
	```
	

#####  **Without Docker**

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
   	uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   	```

3. **Access the application**
   
   Go to the address: ***http://localhost:8000*** .
   


### Via DockerHub

1. **Clone and Run the Image**

	```bash
	docker run -d -p 8001:80 -v shorturl_data:/app/data --name shorturl-service yahaxd/shorturl-service:latest
	```

2. **Access the application**
   
   Go to the address: ***http://localhost:8000*** .



## License

This project is licensed under the MIT License.
