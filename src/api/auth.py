from fastapi import APIRouter, HTTPException, status
from src.config import env
from src.handlers.fetch import fetch
from src.schemas.models import User

app = APIRouter(prefix="/auth", tags=["auth"])


@app.get("/")
async def user_info(token: str):
    user = await fetch(
        method="GET",
        url=f"https://{env.AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    User(**user).save()
    return user
    """
    Get user info from Auth0.

    :param token: The token to use to get the user info.

    :return: The user info.
    
    """
    try:
        data = await fetch(
            method="GET",
            url=f"https://{env.AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {token}"},
        )

        return User(**data).dict()
    except (HTTPException, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
