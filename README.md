# fastAPI-social-media

This is going to be a fullstack project simulating a social media app, including a basic frontend and a backend using Python and FastAPI.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
<!--- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)-->

## Installation

Instructions for installing the project: 

1. First create a virtual environment and activate it (The project requires Python version 3.10 or above):
```
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Install the necessary dependencies using the `requirements.txt` file:
```
$ pip install -r requirements.txt
```

## Usage

How to use the project:

1. Run the live server:
```
$ uvicorn main:app 
```

2. By default the uvicorn server will run in http://127.0.0.1:8000

3. Meanwhile the automatic documentation provided by SwaggerUI can be found in http://127.0.0.1:8000/docs