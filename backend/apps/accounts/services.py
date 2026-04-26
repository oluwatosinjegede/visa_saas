from dataclasses import dataclass
from .models import Role, User


@dataclass
class AccessContext:
    user: User


class RBACService:
    @staticmethod
    def can_manage_users(context: AccessContext) -> bool:
        return context.user.role in {Role.SUPER_ADMIN, Role.PLATFORM_ADMIN}
