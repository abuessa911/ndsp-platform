from fastapi import APIRouter
from app.services.db import get_conn

router=APIRouter()

@router.post("/activate")
def activate(email:str, plan:str="pro"):
    conn=get_conn()
    c=conn.cursor()

    c.execute("INSERT INTO users(email,plan) VALUES(?,?)",(email,plan))
    user_id=c.lastrowid

    conn.commit()
    conn.close()

    return {"status":"activated","user_id":user_id}
