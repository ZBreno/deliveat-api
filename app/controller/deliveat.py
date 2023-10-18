from fastapi import APIRouter

router = APIRouter()

@router.get("/deliveat/{portal_id}")
def access_portal(portal_id:int): 
    return {'message': 'Deliveat System'}

 