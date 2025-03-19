import pytest, os

# Set the environment variable before importing the app
os.environ["AUTH_TOKEN"] = "correcttoken"

from app import app, slackAlert

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sms_webhook_missing_auth(client):
    response = client.get('/sms?from=1234567890&message=Hello')
    assert response.status_code == 400

def test_sms_webhook_incorrect_auth(client):
    response = client.get('/sms?auth=wrongtoken&from=1234567890&message=Hello')
    assert response.status_code == 401

def test_sms_webhook_missing_from(client):
    response = client.get('/sms?auth=correcttoken&message=Hello')
    assert response.status_code == 400

def test_sms_webhook_missing_message(client):
    response = client.get('/sms?auth=correcttoken&from=1234567890')
    assert response.status_code == 400

def test_sms_webhook_success(client, mocker):
    # Mock the slackAlert function to avoid sending real Slack messages
    mocker.patch('app.slackAlert', return_value=None)

    response = client.get('/sms?auth=correcttoken&from=1234567890&message=Hello')
    assert response.status_code == 200
    assert response.data == b'OK'