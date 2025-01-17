
# Full Stack Trivia API Backend

  

## Getting Started

  

### Installing Dependencies

  

#### Python 3.7

  

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

  

#### Virtual Enviornment

  

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

  

#### PIP Dependencies

  

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

  

```bash

pip install -r requirements.txt

```

  

This will install all of the required packages we selected within the `requirements.txt` file.

  

##### Key Dependencies

  

-  [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

  

-  [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

  

-  [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

  

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash

psql trivia < trivia.psql

```

  

## Running the server

  

From within the `backend` directory first ensure you are working using your created virtual environment.

  

To run the server, execute:

  

```bash

export FLASK_APP=flaskr

export FLASK_ENV=development

flask run

```

  

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

  

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

  

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

## API
A flask based REST API for trivia application.

#### Base URL
Base URL: This app can be run locally and is not hosted as a base URL. The backend is hosted at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) This is set as a proxy in the frontend configuration.


### Error Handling
Errors are returned as JSON objest in the below format:
```
  {
	'success':  False,
	'error':  500,
	'message':  'Error in API'
  }
```
The API may return following of errors:
- 400: Bad Request
- 404: Not Found
- 422: Unprocessable Entity
- 500: Error in API


### Resource Endpoint Library

  ```
  GET		'/categories'
  GET		'/categories/<category_id>/questions'
  
  GET		'/questions'
  POST		'/questions'
  DELETE		'/questions/<question_id>'
  
  POST		'/quizzes'
  ```

GET  &nbsp;&nbsp;/categories

- Fetches an array containing names of categories
- Request Arguments: None
- Returns a JSON object with success value, categories and total categories

Sample Output
```
GET	/categories

{
"categories":  [
	"Science",
	"Art",
	"Geography",
	"History",
	"Entertainment",
	"Sports"
	],
"success":  true,
"total_categories":  6
}
```

GET &nbsp;&nbsp;/categories/<category_id>/questions

- Fetches an array of questions  within category
- Request Arguments: valid category id in url
- Returns a JSON object with success value, current category, array of questions and total questions with in the category.

Sample Output
```
GET	'/categories/6/questions'

{
"current_category":  "6",
"questions":  [
	{
	 "answer":  "Brazil",
	 "category":  6,
	 "difficulty":  3,
	 "id":  10,
	 "question":  "Which is the only team to play in every soccer World Cup tournament?"
	},
	{
	 "answer":  "Uruguay",
	 "category":  6,
	 "difficulty":  4,
	 "id":  11,
	 "question":  "Which country won the first ever soccer World Cup in 1930?"
	}
],
"success":  true,
"total_questions":  2
}
```


GET &nbsp;&nbsp;'/questions'
- Fetches an array of questions  with pagination
- Request Arguments: page -> integer (optional, defualts to 1)
- Returns a JSON object with success value, current category, array of questions and total questions with in the category.

Sample Output
```
GET	'/questions?page=3'

{
"categories":  [
	"Science",
	"Art",
	"Geography",
	"History",
	"Entertainment",
	"Sports"
	],
"current_category":  null,
"questions":  [
	{
	 "answer":  "The Liver",
	 "category":  1,
	 "difficulty":  4,
	 "id":  20,
	"question":  "What is the heaviest organ in the human body?"
	},
	{
	 "answer":  "Alexander Fleming",
	 "category":  1,
	 "difficulty":  3,
	 "id":  21,
	 "question":  "Who discovered penicillin?"
	},
],
"success":  true,
"total_questions":  29
}
```

POST &nbsp;&nbsp;'/questions'

i. To add new questions
- Adds new question to database.
- Request Arguments: None
- Request Body: Required (JSON)
	```
	{
		"question": "What is the heaviest organ in the human body?",
		"answer": "The Liver",
		"category": "1",
		"difficulty": 4
	}
	```
- Returns a JSON object with success value and question id of the newly inserted question.

Sample Output
```
{
"question_id":  39,
"success":  true
}
```

ii. To perform search 
- Retrives questions containing input search term.(case-insensitive)
- Request Arguments: None
- Request Body: Required (JSON)
	```
	{
		"searchTerm": "Body",
	}
	```
- Returns a JSON object with success value, array of questions, current category and total questions count.

Sample Output
```
{
"current_category":  null,
"questions":  [
	{
	 "answer":  "The Liver",
	 "category":  1,
	 "difficulty":  4,
	 "id":  20,
	 "question":  "What is the heaviest organ in the human body?"
	}
],
"success":  true,
"total_questions":  1
}
```
DELETE  &nbsp;&nbsp;/questions/<question_id>

- Deletes the question with specific id provided in URL
- Request Arguments: None
- Returns a JSON object with success value.

Sample Output
```
DELETE	/questions/1

{
	'success':  True
}
```

POST  &nbsp;&nbsp;/quizzes

- Fetches the random question from requested category.
- Request Arguments: None
- Request Body: Required (JSON)
	````
	{
		"previous_questions": [],
		"quiz_category": 4
	}
	````
- Returns a JSON object with success value and question.

Sample Output
```
POST	/quizzes
{
"question":  {
	"answer":  "Muhammad Ali",
	"category":  4,
	"difficulty":  1,
	"id":  9,
	"question":  "What boxer's original name is Cassius Clay?"
	},
"success":  true
}
```



## Testing

To run the tests, run

```

dropdb trivia_test

createdb trivia_test

psql trivia_test < trivia.psql

python test_flaskr.py

```
