from fastapi import APIRouter

router = APIRouter()

@router.get("/regulation")
def get_regulation():
    return {"message": "Regulation endpoint placeholder"}
