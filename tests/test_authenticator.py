import pytest

from backend.authenticator import *


class FakeRequest:
    def __init__(self):
        self.headers = {}

@pytest.fixture
def authenticator():
    return Authenticator()

def test_validateAuthentication_01(authenticator):
    request = FakeRequest()
    request.headers["Cookie"] = "authenticationKey=00001#99999999999;"
    
    authenticator.authorization_list["00001"] = "00001#99999999999"
    
    assert authenticator.validateAuthentication(request) == True

def test_validateAuthentication_02(authenticator):
    request = FakeRequest()
    request.headers["Cookie"] = "authenticationKey=00002#99999999999;"
    
    authenticator.authorization_list["00001"] = "00001#99999999999"
    
    assert authenticator.validateAuthentication(request) == False

def test_validateAuthentication_03(authenticator):
    request = FakeRequest()
    request.headers["Cookie"] = "randomCookie=123434;"
    
    authenticator.authorization_list["00001"] = "00001#99999999999"
    
    assert authenticator.validateAuthentication(request) == False

def test_validateAuthentication_04(authenticator):
    request = FakeRequest()
    
    authenticator.authorization_list["00001"] = "00001#99999999999"
    
    assert authenticator.validateAuthentication(request) == False

def test_validateAuthentication_05(authenticator):
    request = FakeRequest()
    request.headers["Cookie"] = "authenticationKey=00001#99999999999;"
    
    authenticator.authorization_list["00001"] = "00001#88888888888"
    
    assert authenticator.validateAuthentication(request) == False

def test_getUserIdAndAuthKeyFromCookies(authenticator):
    request = FakeRequest()
    request.headers["Cookie"] = "authenticationKey=00001#99999999999;"
    
    authenticator.authorization_list["00001"] = "00001#99999999999"
    
    assert authenticator.getUserIdAndAuthKeyFromCookies(request) == ("00001", "00001#99999999999")


