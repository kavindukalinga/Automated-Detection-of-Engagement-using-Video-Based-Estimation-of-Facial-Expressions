# Automated-Detection-of-Engagement-using-Video-Based-Estimation-of-Facial-Expressions

How computer vision techniques can be used to detect engagement of students


## Guide to Run:

Using `venv` in Python is a great way to create isolated environments for the project.

### Create a Virtual Environment

```sh
python -m venv myenv
```

`myenv` is the name of the virtual environment. You can replace it with any name you prefer.

### Activate the Virtual Environment

```sh
myenv\Scripts\activate
# or myenv\Scripts\Activate.ps1
# or source myenv/bin/activate
```

Once activated, you should see (myenv) in your terminal prompt.

### Install Packages Inside the Virtual Environment
After activation, install dependencies using pip:  

Install `cmake` before run the application.  

To install dependencies:  

```sh
pip install -r requirements.txt
```

If you install any new dependencies:

```sh
pip freeze > requirements.txt
```

### Deactivate the Virtual Environment
To exit the virtual environment, simply run:

```sh
deactivate
```

### Delete the Virtual Environment (Optional)

If you no longer need the environment, delete the folder:

```sh
rmdir /s /q myenv
# rm -rf myenv
```

### To run the api:

```sh
python -m uvicorn src.api:app --reload
```