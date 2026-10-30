"""승인된 업체만 쓰는 기능(견적 요청함, 견적서 제출, 공사기간)에 거는 의존성 (FBF-01)."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import require_role
from app.auth.models import User
from app.db import get_session
from app.shared.errors import AppError
from app.vendor.repository import vendor_status_of


async def approved_vendor(
    user: User = Depends(require_role("vendor")), s: AsyncSession = Depends(get_session)
) -> User:
    if await vendor_status_of(s, user.id) != "approved":
        raise AppError(403, "vendor_not_approved", "관리자 승인 뒤에 쓸 수 있어요.")
    return user
