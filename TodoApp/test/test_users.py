from .utils import *
from ..routers.users import get_current_user,get_db
from fastapi import status

app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user

def test_get_user():
    response= client.get("/user")
    assert response.status_code==status.HTTP_200_OK # type: ignore 