__all__ = ['Base']

import sqlalchemy.ext.declarative

Base: sqlalchemy.ext.declarative.DeclarativeMeta = (
    sqlalchemy.ext.declarative.declarative_base()
)
