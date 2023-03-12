from typing import Optional
from datetime import datetime

from api.orm import FaunaModel as Q, q, Field, BaseModel, Optional
from api.utils import (

    gen_name,

    gen_ip,

    gen_password,

    gen_port,

    gen_secret,

    gen_oid,

    gen_now,
)



class DBContainer(Q):

    """Container model."""


    sub: str = Field(..., index=True, unique=True)

    image: str = Field(...)

    cid: Optional[str] = Field(default=None, index=True, unique=True)

    name: str = Field(default_factory=gen_name, index=True, unique=True)

    port: int = Field(default_factory=gen_port, index=True, unique=True)

    password: str = Field(default_factory=gen_password)

    database: str = Field(default_factory=gen_name, index=True, unique=True)

    database_uri: Optional[str] = Field(default=None)





class User(Q):

    """User model."""


    sub: str = Field(..., index=True, unique=True)

    nickname: Optional[str] = Field(default=None)

    name: Optional[str] = Field(default=None)

    picture: Optional[str] = Field(default=None)
    updated_at: str = Field(

        default_factory=lambda: datetime.now().isoformat(), index=True
    )

    email: Optional[str] = Field(default=None, index=True)

    email_verified: Optional[bool] = Field(default=None, index=True)

    given_name: Optional[str] = Field(default=None)

    family_name: Optional[str] = Field(default=None)

    locale: Optional[str] = Field(default=None, index=True)


    def create_user(self) -> dict:

        """Create a user"""

        response = self.find_unique("sub", self.sub)
        if not response:

            return self.create()
        return response

