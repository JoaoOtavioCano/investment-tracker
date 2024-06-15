from backend.login import Login, __createAuthenticationKey__

import unittest
from unittest.mock import MagicMock, patch
import json
import bcrypt

def test__createAuthenticationKey__():
    userID = 1
    authKey = __createAuthenticationKey__(userID)

    assert authKey.find('#') == 10
    assert len(authKey) == 75
    assert authKey.split('#', 1)[0] == "0000000001"

@patch('backend.login.PayloadValidator')
@patch('backend.login.Database')
def test_respond_invalid_payload(MockDatabase, MockPayloadValidator):
    request_handler = MagicMock()
    payload = {"email": "test@example.com"}  # Missing "password" key

    # Mock PayloadValidator
    payload_validator_instance = MockPayloadValidator.return_value
    payload_validator_instance.validate.return_value = False

    login = Login(request_handler, payload)
    login.respond()

    request_handler.send_error.assert_called_once_with(500, "INVALID PAYLOAD")
    request_handler.end_headers.assert_called_once()

@patch('backend.login.PayloadValidator')
@patch('backend.login.Database')
def test_respond_invalid_credentials(MockDatabase, MockPayloadValidator):
    request_handler = MagicMock()
    payload = {"email": "test@example.com", "password": "password"}

    # Mock PayloadValidator
    payload_validator_instance = MockPayloadValidator.return_value
    payload_validator_instance.validate.return_value = True

    # Mock Database
    db_instance = MockDatabase.return_value
    db_instance.getUser.return_value = []

    login = Login(request_handler, payload)
    login.respond()

    request_handler.send_error.assert_called_once_with(500, "INVALID CREDENTIALS")
    request_handler.end_headers.assert_called_once()

@patch('backend.login.PayloadValidator')
@patch('backend.login.Database')
@patch('backend.login.bcrypt.checkpw')
@patch('backend.login.AuthCookie')
def test_respond_valid_credentials(MockAuthCookie, MockCheckpw, MockDatabase, MockPayloadValidator):
    request_handler = MagicMock()
    payload = {"email": "test@example.com", "password": "password"}

    # Mock PayloadValidator
    payload_validator_instance = MockPayloadValidator.return_value
    payload_validator_instance.validate.return_value = True

    # Mock Database
    db_instance = MockDatabase.return_value
    db_instance.getUser.return_value = [(1, "test_user", bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode())]

    # Mock bcrypt
    MockCheckpw.return_value = True

    # Mock AuthCookie
    mock_cookie_instance = MockAuthCookie.return_value
    mock_cookie_instance.generateHTTPheaders.return_value = "Set-Cookie: authentication_key"

    login = Login(request_handler, payload)
    login.respond()

    # Expected JSON response
    expected_response = json.dumps({'user': 'test_user'}).encode('utf-8')

    request_handler.send_response.assert_called_once_with(200, "OK")
    request_handler.send_header.assert_any_call('Set-Cookie', 'Set-Cookie: authentication_key')
    request_handler.send_header.assert_any_call('Content-type', 'application/json')
    request_handler.end_headers.assert_called_once()
    request_handler.wfile.write.assert_called_once_with(expected_response)