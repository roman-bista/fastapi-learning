from .utils import *
from ..routers.users import get_current_user,get_db
from fastapi import status

app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user

def test_get_user(test_user):
    response= client.get("/user")
    assert response.status_code == status.HTTP_200_OK 
    assert response.json() is not None
    assert response.json()['username']=='roman'
    assert response.json()['phone_number']=='1234567890'

def test_change_password_sucess(test_user):
    response= client.put("/user/password", json={"password": "roman","new_password":"newpassword"})
    assert response.status_code == status.HTTP_200_OK

def test_change_pw_invalid_current_pw(test_user):
    response= client.put("/user/password", json={'password': "wrong",
                                                 'new_password':"newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':' error on password change '}

def change_change_phone_number_sucess(test_user):
    response=client.put("/user/phonenumber/2222222")
    assert response.status_code== status.HTTP_204_NO_CONTENT