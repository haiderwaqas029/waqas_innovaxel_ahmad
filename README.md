
//...Innovaxel Home Task Assessment...//

URL Shortener Service
A RESTful API service built with Python Flask that shortens long URLs, tracks access statistics, and provides full CRUD functionality.

Features
Shorten URLs: Convert long URLs into compact, shareable links

URL Management: Update or delete existing shortened URLs

Statistics Tracking: Monitor how many times each URL is accessed

Simple Frontend: User-friendly web interface to interact with the API

Tech Stack
Backend: Python Flask

Frontend: HTML, CSS, JavaScript

Storage: In-memory dictionaries (no database required)

API: RESTful design with JSON responses

Installation & Usage
Clone repository

Install requirements: pip install flask

Run server: python app.py

Access web interface at http://localhost:5000

API Endpoints
POST /shorten - Create short URL

GET /<code> - Redirect to original URL

GET /shorten/<code> - Retrieve URL details

PUT /shorten/<code> - Update target URL

DELETE /shorten/<code> - Remove short URL

GET /shorten/<code>/stats - Get access statistics

