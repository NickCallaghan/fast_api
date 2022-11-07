from typing import List
from fastapi import FastAPI, HTTPException
from models import User, UpdateUserRequest, Gender, Role
from uuid import UUID

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("9771f6e2-d13a-48da-80a2-e33186be7cd4"),
        first_name='Nick',
        middle_name='John',
        last_name='Callaghan',
        gender=Gender.male,
        roles=[Role.admin, Role.user]),
    User(
        id=UUID("3c882cc5-a0d2-4004-a139-4350f7d47f45"),
        first_name='Alfie',
        middle_name='Furball',
        last_name='Callaghan',
        gender=Gender.male,
        roles=[Role.user])
]


@app.get('/api/v1/users')
def get_users():
    return {
        "length": len(db),
        "users": db
    }


@app.post('/api/v1/users')
async def get_users(user: User):
    db.append(user)
    return {'id': user.id}


@app.put('/api/v1/users/{user_id}')
async def get_users(user_id, updated_user: UpdateUserRequest):
    for user in db:
        print({"req": user_id})
        print({"usr": user.id})
        if UUID(user_id) == user.id:
            if updated_user.first_name is not None:
                user.first_name = updated_user.first_name
            if updated_user.middle_name is not None:
                user.middle_name = updated_user.middle_name
            if updated_user.last_name is not None:
                user.last_name = updated_user.last_name
            if updated_user.gender is not None:
                user.gender = updated_user.gender
            if updated_user.roles is not None:
                user.roles = updated_user.roles

            return {'detail': "user updated", "user": user}

    raise HTTPException(
        status_code=404, detail=f'user with id: {user_id} not found')


@app.delete('/api/v1/users/{user_id}')
async def get_users(user_id: UUID):
    for user in db:
        if user_id == user.id:
            db.remove(user)
            return {'id': user_id, 'message': 'user deleted'}

    raise HTTPException(
        status_code=404, detail=f'user with id: {user_id} does not exist')
