"""Ensure model modules are imported so SQLAlchemy metadata is populated.

This module purposely imports submodules (not names) to avoid
import-time circular imports between model modules. Importing the
modules registers tables/columns with SQLAlchemy's metadata which is
required for Alembic autogenerate.
"""
import importlib

# Import modules for their side-effects (registering models/metadata).
importlib.import_module('app.models.user')
importlib.import_module('app.models.employee')
importlib.import_module('app.models.business')
importlib.import_module('app.models.order')
importlib.import_module('app.models.product')
importlib.import_module('app.models.table')

__all__ = []
