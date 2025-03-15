import requests

TOKEN = "some_token"                         # Your token here
SUBMIT_URL = "149.156.182.9:6060/extra-task-trumpf/submit"
PY_FILE_TO_SUBMIT = "example_submission.py"   # Assuming the file is in the same directory


def submitting_example():

    response = requests.post(
        SUBMIT_URL, 
        headers={"token": TOKEN}, 
        files={"file": open(PY_FILE_TO_SUBMIT, "rb")})
    print(response.status_code, response.text)


if __name__ == '__main__':
    submitting_example()