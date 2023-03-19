from typing import Optional
from datetime import datetime

from api.data.orm import FaunaModel as Q, Field, Optional

from api.utils.misc import gen_name, gen_password, gen_port


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
