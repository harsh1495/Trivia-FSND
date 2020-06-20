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

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

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


## API Endpoints

### GET ```"/categories"```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.


#### Sample Response

```

{
    '1': "Science",
    '2': "Art",
    '3': "Geography",
    '4': "History",
    '5': "Entertainment",
    '6': "Sports"
}

```

### GET ```"/questions?page=<page_number>"```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Fetches a dictionary of questions in which the keys are the answer, category, difficulty, id and question.
- Request Arguments: Page Number
- Returns: List of questions, number of total questions, categories and current category.

#### Sample Response

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
    "questions":[
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 1,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'??"
        },
        {
            "answer": "Muhammad Ali",
            "category": 6,
            "difficulty": 2,
            "id": 2,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "success": true,
    "total_questions": 20
}

```

### DELETE ```"/questions/<question_id>"```

- Delete a question from the list of questions.
- Request Arguments: Question Id.
- Returns: true if successfully deleted, removes the question from the frontend and returns all questions as above.

#### Sample Response

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
    "questions":[
        {
            "answer":"Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 1,
            "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'??"
        },
        {
            "answer":"Muhammad Ali",
            "category": 6,
            "difficulty": 2,
            "id": 2,
            "question":"What boxer's original name is Cassius Clay?"
        }
    ],
    "success": true,
    "total_questions": 19
}

```

### POST ```"/questions"```

- Creates a new question
- Request Body: question, answer, difficulty and category.
- Returns: true if successfully creates a new question.

#### Sample request payload

```

{
    "question":"What is your name",
    "answer":"My name is Harsh",
    "difficulty": 4,
    "category": 1
}

```

#### Sample Response

```

{
    "success": true,
    "created": <newly_created_question_id>
}

```

### POST ```"/questions/search"```

- Searches for the questions
- Request Arguments: Page Number
- Request Body: search_term
- Returns: List of questions, number of total questions and current category.

#### Sample request payload

```

{
    "searchTerm": "the"
}

```

#### Sample Response

```

{
    "questions": [
        {
            "answer":"Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 1,
            "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'??"
        },
        {
            "answer":"Muhammad Ali",
            "category": 6,
            "difficulty": 2,
            "id": 2,
            "question":"What boxer's original name is the Cassius Clay?"
        }
    ],
    "success": true,
    "total_questions": 4,
    "current_category": 1
}

```

### GET ```"/categories/<int: category_id>/questions"```

- To get questions based on a specific category
- Request Arguments: <category_id> and <page_number>
- Returns: List of questions, number of total questions, current category and categories.

#### Sample Response

```

{
    "questions":[
        {
            "answer": "Artery",
            "category": 1,
            "difficulty": 2,
            "id": 2,
            "question": "Which of the following is a large blood vessel that carries blood away from the heart?"
        },
        {
            "answer": "206",
            "category": 1,
            "difficulty": 2,
            "id": 5,
            "question": "How many bones are present in human body?"
        }
    ],
    "current_category": 1,
    "success": true,
    "total_questions": 2
}

```


### POST ```"/quizzes"```

- Fetch questions to start the trivia game.
- Request Body: quiz_category and previous_questions.
- Returns: Randomised questions from the selected category.


#### Sample request payload

```

{
    "previous_questions": [],
    "quiz_category": {
        "type": "Science",
        "id": 1
    }
}

```

#### Sample Response

```

{
    "success": true,
    "question": {
            "answer":"206",
            "category": 1,
            "difficulty": 2,
            "id": 5,
            "question":"How many bones are present in human body?"
        }
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