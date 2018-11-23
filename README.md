# StackOverflow-lite

StackOverflow-lite is a platform where people can ask questions and provide answers.

[![Build Status](https://travis-ci.org/patrickf949/stackoverflow.svg?branch=deploy)](https://travis-ci.org/patrickf949/stackoverflow)[![Maintainability](https://api.codeclimate.com/v1/badges/6cdbe0208a6102b00787/maintainability)](https://codeclimate.com/github/patrickf949/stackoverflow/maintainability)[![Coverage Status](https://coveralls.io/repos/github/patrickf949/stackoverflow/badge.svg?branch=deploy)](https://coveralls.io/github/patrickf949/stackoverflow?branch=deploy)
### Getting Started

Clone the project using the [link](https://github.com/KengoWada/Stackoverflow-lite).

### Prerequisites

A browser with the access to the internet.

### Installing

* Clone the project to your local machine
```
git clone https://github.com/KengoWada/Stackoverflow-lite.git
```

### Features

* Post a question
* Post an answer for a particular question
* Get all questions
* Get a single question
* Delete a question that a user has created
* A user can login
* A user can register
* A user can select a particular answer as the preferred one to the question he/she asked
* A user can edit an answer they have posted



### Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST|api/v1/questions|Create a question
GET|api/v1/questions/<questionId>|Fetch a specific question
GET|api/v1/questions|Fetch all questions
POST|api/v1/questions/<questionId>/answers|Add an answer
DELETE|api/v1/questions/<questionId>|Delete a question
POST|api/v1/auth/login|Allow a user to login
POST|api/v1/auth/signup|Allow a user to register and use the system
PUT|api/v1/questions/<questionId>/answers/<answerId>|Allow a user to mark an answer as preferred and edit an answer they provided


### Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python.
* [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create isolated Python environments
* [PIP](https://pip.pypa.io/en/stable/) - Python package installer.


### Deployment

The API is hosted on [Heroku](https://kengo-stackoverflow-lite-api.herokuapp.com/api/v1/questions).

### Built With

* Python/Flask

### Authors

Kengo Wada
