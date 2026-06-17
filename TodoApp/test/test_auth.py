from .utils import *
from ..routers.auth import get_db,authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
app.dependency_overrides[get_db]=override_get_db
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException


def test_authenticate_user(test_user):
    db=TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username,'roman',db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    non_existent_user = authenticate_user('wrongUsername','roman',db)
    assert non_existent_user is False
    wrong_pw_user=authenticate_user(test_user.username,'wrongpw',db)
    assert wrong_pw_user is False

def test_create_access_token():
    username='shyam'
    user_id=1
    role='user'
    expires_delta=timedelta(days=1)
    token = create_access_token(username, user_id,role, expires_delta)
    decoded_token=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM],options={'verify_signature': False})
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio                                                    
async def test_get_current_user():
    encode={'sub':'shyam','id':1, 'role':'admin'}
    token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user= await get_current_user(token=token)
    assert user == {'username':'shyam','user_id':1,'user_role':'admin'}

                #     encode
                # {
                #   sub: "shyam",
                #   id: 1,
                #   role: "admin"
                # }
                #         ↓

                # jwt.encode()------->eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
                                        # .
                                        # eyJzdWIiOiJzaHlhbSIsImlkIjoxLCJyb2xlIjoiYWRtaW4ifQ---->Header.Payload.Signature
                                        # .
                                        # Q3KJ8dskJHF8324jkhdfkjsdhfkjshdf...

                #         ↓

                # JWT Token

                #         ↓
                # get_current_user()

                #         ↓
                # jwt.decode()

                #         ↓
                # {
                #   username: "shyam",
                #   user_id: 1,
                #   user_role: "admin"


@pytest.mark.asyncio
async def test_current_user_missing_payload():
    encode={'role':'user'}
    token = jwt.encode(encode, SECRET_KEY,algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)                 #Call the async function get_current_user()
                                                            # Pass the JWT token to it
                                                                # Wait until it finishes
                                                                # Return the result

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'couldnot validate user.'