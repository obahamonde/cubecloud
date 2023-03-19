from fastapi import APIRouter, HTTPException, status

from api.config import env

from api.hooks import fetch

from api.data.models import User


app = APIRouter(prefix="/auth", tags=["auth"])

    
@app.get("/")
async def user_info(token: str):
    """
    Get user info from Auth0.

    :param token: The token to use to get the user info.

    :return: The user info.
    
    """
    data = await fetch(
        method="GET",
        url=f"https://{env.AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    return User(**data).dict()