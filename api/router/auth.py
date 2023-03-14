from httpx import AsyncClient

from fastapi import APIRouter, HTTPException, status

from api.config import env

from api.schemas.output import User


app = APIRouter(prefix="/auth", tags=["auth"])


@app.get("/", response_model=User)
async def user_info(token: str) -> User:
    """Return user info"""

    async with AsyncClient() as client:
        try:
            response = await client.get(
                f"https://{env.AUTH0_DOMAIN}/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            )

            user = User(**response.json())

            user.create_user()

            return user

        except (HTTPException, Exception) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            ) from exc
