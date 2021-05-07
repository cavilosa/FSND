# Full Stack API Final Project

## Full Stack Trivia API

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game. This is a full stack application with backend and frontend directories.

What this application can:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

### Backend

The `./backend` directory contains Flask and SQLAlchemy server.
All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).
The backend runs on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server.

## Getting Started

### Authentication
This version of the application does not require authentication or API keys.

### Environment Variables

All environment variables are stored in the .env file and called in the code with python-dotenv library. In order to create the database path you will need your password, stored in the .env file on the root folder of the backend.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the Python 3.7 version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) as higher versions, like Python 3.9, are not supporting some of Flask functionality, at least for now.

#### Virtual Environment

It is recommend to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
From the backend folder with Postgres running (Windows) in bash CLI:
```bash
drop database trivia;
create database trivia;
```
Exit psql with ```\q``` and run this command to populate trivia database:
```bash
psql -d trivia -U postgres -a -f trivia.psql

```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment:
```bash
source env/Scripts/activate
```

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
or alternatively :
```bash
set FLASK_APP=flaskr && set FLASK_ENV=development && flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.


### Running FrontEnd

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. To install them run:

```bash
npm install
```

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Game Play Mechanics

The game designed to play all the questions in the category and will end when there are no more new questions.


## Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return w error types:
    404 - resource not found,
    400 - bad request,
    422 - You are trying to delete a question that does not exists in the database.


## Endpoints

#### GET /categories
This endpoint  handles GET requests for all available categories. Returns jesonyfied object with success value and a dictionary of categories:
```
({
    "success":True,
    "categories": dict
})
```
The dictionary of categories contains "id" and "type" keys:
```
{
    "id": 2,
    "type": Art
}
```
Sample:
```bash
curl http://127.0.0.1:5000/categories
```


## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
Log into your psql and run:
```bash
drop database trivia_test
create database trivia_test
```
After exiting the psql, populate the database with entries and run the tests:
```bash
psql -d trivia_test -U postgres -a -f trivia.psql
python test_flaskr.py
```
