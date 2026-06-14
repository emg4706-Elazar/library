from routes.book_routes import router, HTTPException
from database.member_db import *
from models.models import *
from logs.logging_config import logger


@router.post("/members", status_code=201)
def post_member(data: Member):
    logger.info("Create new member started")
    data = data.model_dump()
    try:
        member_db.create_member(data)
    except IntegrityError:
        logger.error("Create new member failed. Email not unique")
        raise HTTPException(status_code=400, detail="This email is not unique")
    except ProcessFailed:
        logger.error("Create new member failed. Process failed")
        raise HTTPException(status_code=500, detail="Process failed for any reason")
    logger.info("New member was created successfully")
    return "New member was created successfully"


@router.get("/members")
def get_members():
    if not member_db.get_all_members():
        return "There's no members yet"
    logger.info("Get all members performed")
    return member_db.get_all_members()


@router.get("/members/{id}")
def get_member_by_id(id: int):
    member = member_db.get_member_by_id(id)
    if not member:
        logger.error(f"Get member by id Failed. There's no id: {id}")
        raise HTTPException(status_code=404, detail="Member not found")
    logger.info("Get member by id Performed")
    return member


@router.put("/members/{id}")
def put_member(id: int, data: Member):
    logger.info("Update member started")
    member = member_db.get_member_by_id(id)
    if not member:
        logger.error(f"Update member failed. There's no id: {id}")
        raise HTTPException(status_code=404, detail="Member not found")
    data = data.model_dump()
    try:
        member_db.update_member(id, data)
    except IntegrityError:
        logger.error("Update member failed. Email not unique")
        raise HTTPException(status_code=400, detail="This email is not unique")
    except ProcessFailed:
        logger.error("Update member failed. Process failed")
        raise HTTPException(status_code=500, detail="Process failed for any reason")
    logger.info("Member was updated successfully")
    return "Member was updated successfully"


@router.put("/members/{id}/deactivate")
def deactivate(id: int):
    logger.info("Deactivate member started")
    member = member_db.get_member_by_id(id)
    if not member:
        logger.error(f"Deactivate member failed. There's no member id: {id}")
        raise HTTPException(status_code=404, detail="Member not found")
    if not member["is_active"]:
        logger.error(f"Deactivate member failed. Member is already not active")
        raise HTTPException(status_code=400, detail="Member is already not active")
    member_db.deactivate_member(id)
    logger.info("Deactivate member was successfully")
    return "Member doesn't active from now"



@router.put("/members/{id}/activate")
def activate(id: int):
    logger.info("Activate member started")
    member = member_db.get_member_by_id(id)
    if not member:
        logger.error(f"Activate member failed. There's no member id: {id}")
        raise HTTPException(status_code=404, detail="Member not found")
    if member["is_active"]:
        logger.error(f"Activate member failed. Member is already active")
        raise HTTPException(status_code=400, detail="Member is already active")
    member_db.activate_member(id)
    logger.info("Activate member was successfully")
    return "Member does active from now"