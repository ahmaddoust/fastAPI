from uuid import UUID
from fastapi import FastAPI, HTTPException 
from models import User, Gender, Role, UserUpdateRequest 
from typing import List
 
app = FastAPI() 

db: List[User] = [
    User(
         id=UUID("4ceb8bff-5ab9-4abd-9b78-92722a7612e6"), 
         first_name="Jamila", 
         last_name="Ahmed",
         middle_name=None,  
         gender=Gender.female, 
         roles=[Role.student]
    ),
    User(
        id=UUID("d20e73c0-951e-4ce0-9a4e-d9bc4333816e"), 
         first_name="Alex", 
         last_name="Jones",
         middle_name=None, 
         gender=Gender.male, 
         roles=[Role.admin, Role.user]
    ) 
]

@app.get("/") 
async def root(): 
    return {"Hello": "Mundo"} 


@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User): 
    db.append(user) 
    return{"id": user.id} 

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name 
            if user_update.last_name is not None:
                user.last_name = user_update.last_name 
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name 
            if user_update.roles is not None:
                user.roles = user_update.roles
            return 
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {user_id} does not exist"
        )