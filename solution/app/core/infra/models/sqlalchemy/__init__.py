__all__ = ['Base', 'load_models']

import sqlalchemy.ext.declarative

Base: sqlalchemy.ext.declarative.DeclarativeMeta = (
    sqlalchemy.ext.declarative.declarative_base()
)


def load_models() -> None:
    import app.core.infra.models.advertiser.sqlalchemy.advertiser
    import app.core.infra.models.client.sqlalchemy.client
