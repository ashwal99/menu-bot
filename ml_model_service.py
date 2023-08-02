import requests


def getFlaskServiceData():
    flask_url = "http://ec2-13-126-188-69.ap-south-1.compute.amazonaws.com:5000/"
    response = requests.get(flask_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response data
        data = response.text
        # Do something with the data
    else:
        # Handle the error
        print(
            f"API call to Flask application failed. Status code: {response.status_code}")
        return f"API call to Flask application failed. Status code: {response.status_code}"
    return data


def getTopKRelavantItemsData(refined_query):
    flask_url = "http://localhost:5000/relavant_items"
    headers = {'Content-Type': 'application/json'}
    data = {'query': refined_query}
    response = requests.post(flask_url, json=data, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        # Do something with the data
    else:
        # Handle the error
        print(
            f"API call to Flask application failed. Status code: {response.status_code}")
        return f"API call to Flask application failed. Status code: {response.status_code}"
    return data
