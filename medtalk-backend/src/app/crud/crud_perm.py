from app.crud.base import CRUDBase
from app.models.role_perm import Perm, PermCreate, PermUpdate


class CRUDPerm(CRUDBase[Perm, PermCreate, PermUpdate]):
    ...


perm = CRUDPerm(Perm)
