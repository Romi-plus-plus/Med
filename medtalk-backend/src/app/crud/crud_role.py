from app.crud.base import CRUDBase
from app.models.role_perm import Role, RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    ...


role = CRUDRole(Role)
