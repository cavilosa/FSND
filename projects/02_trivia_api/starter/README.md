# Full Stack API Second Project

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

Following commands are for bash command line on Windows 10.

### Authentication
This version of the application does not require authentication or API keys.

### Environment Variables

All environment variables are stored in the `.env` file and called in the code with `python-dotenv` library. In order to create the database path you will need your password, stored in the .env file in the root folder of the backend.

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

#### Installing Node.js and NPM

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

The game designed to play all the questions in the category and will end when there are no more new questions to ask.


## Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
},
{
  "error": 404,
  "messages": "resource not found",
  "success": false
},
{
  "error": 422,
  "messages": "You are trying to delete a question that does not exists in the database.",
  "success": false
},
{
   "success": False,
   "error": 500,
    "messages": "Internal server error."
}
```

The API can return these error types:

* 404 - resource not found,
* 400 - bad request,
* 422 - You are trying to delete a question that does not exists in the database,
* 500 - Internal Server Error.


## Endpoints

#### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: An object with a single key, categories:
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
`curl http://127.0.0.1:5000/categories`


#### GET /questions/
- Returns categories, current_category, paginated list of questions(10 per page),
and a number of total questions:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
    ],
    "total_questions": 16
}
```
- Request Arguments: None

- If number of page is higher then available questions in the database (`curl http://127.0.0.1:5000/questions/?page=100`), the route will return an error 404.

- Sample: `curl http://127.0.0.1:5000/questions/`


#### Delete /questions/<id>
- Deletes a question from the database by its id and doesn't return new data except the success value.

- Requests Arguments: `<id>`
- Returns:
```
({
    "success": True
})
```
-Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

If the question doesn't exist returns the error 422.


#### POST /questions/submit
Addes a new question to the database. Returns:
```
({
    "success": True,
    "answer": answer,
    "question": question,
    "difficulty": difficulty,
    "category": category
})
```
- Request Arguments: answer, question, difficulty and category.

- In the frontend the application will reset the form.

- Sample: `curl http://127.0.0.1:5000/questions/submit -X POST -H "Content-Type: application/json" -d '{"answer":"Neverwhere", "question":"What wrote Neil Gaiman", "difficulty":"3",
"category": "2"}'`

- If json didn't provide with full information, e.g. no answer or question, the application will return the error 400.


#### POST /questions/search

- Returns a list of questions, containing the searchTerm, success, a number of total questions in the list and a current category, in a format of a jsonified object:
```
({
    "success": True,
    "questions": questions,
    "total_questions": len(questions),
    "current_category": None
})
```
-Request Arguments: searchTerm.

- Inappropriate request, like `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search": "title"}' ` will give an error 400.

- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`

#### GET /categories/<id>
- Returns all questions in the category by its id number, success, a number of questions in the category and a selected category's id number.
```
({
    "success": True,
    "questions": questions,
    "total_questions": len(questions),
    "current_category": category.format()["id"]
})
```
- Request Arguments: `<id>`

- Sample ` curl http://127.0.0.1:5000/categories/1/questions`

- Returns 404 error if the category is not found and an empty list of questions if there are none in the category.


#### POST /quizzes/
- Returns success value, next question, last question and the length of total questions on the selected category. The additional "categories" dictionary will allow modify number of categories further in the development.
```
{
  "last_question": false,
  "question": {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "questions": 2,
  "success": true
}

```
- Request Argiment: previous_question, quiz_category and categories.

- Sample: `curl http://127.0.0.1:5000/quizzes/ -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Geography", "id": "3"}, "categories": {"1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports"}}'`


## Testing
Log into your psql and run:
```bash
drop database trivia_test
create database trivia_test
```
After exiting psql, populate the database with entries and run the tests:
```bash
psql -d trivia_test -U postgres -a -f trivia.psql
python test_flaskr.py
```
