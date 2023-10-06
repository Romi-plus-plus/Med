from enum import Enum


class Permission(Enum):
    ChatAccess = "Chat access"
    UserMngr = "User management"
    ChatMngr = "Chat management"
    OpMngr = "Operation management"
    KBMngr = "KB management"
