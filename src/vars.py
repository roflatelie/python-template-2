from contextvars import ContextVar


PGConnection: ContextVar = ContextVar("PGConnection")
