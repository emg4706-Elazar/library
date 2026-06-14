from routes.book_routes import router, HTTPException
from database.member_db import *
from models.models import *


@router.post("/members", status_code=201)
def post_member(data: Member):
    data = data.model_dump()
    try:
        member_db.create_member(data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="This email is not unique")
    except ProcessFailed:
        raise HTTPException(status_code=500, detail="Process failed for any reason")
    return "New member was created successfully"


@router.get("/members")
def get_members():
    if not member_db.get_all_members():
        return "There's no members yet"
    return member_db.get_all_members()


@router.get("/members/{id}")
def get_member_by_id(id: int):
    member = member_db.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/members/{id}")
def put_member(id: int, data: Member):
    member = member_db.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    data = data.model_dump()
    try:
        member_db.update_member(id, data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="This email is not unique")
    except ProcessFailed:
        raise HTTPException(status_code=500, detail="Process failed for any reason")
    return "New member was updated successfully"


@router.put("/members/{id}/deactivate")
def deactivate(id: int):
    member = member_db.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not member["is_active"]:
        raise HTTPException(status_code=400, detail="Member is already not active")
    member_db.deactivate_member(id)
    return "Member doesn't active from now"



@router.put("/members/{id}/activate")
def activate(id: int):
    member = member_db.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if member["is_active"]:
        raise HTTPException(status_code=400, detail="Member is already active")
    member_db.activate_member(id)
    return "Member does active from now"