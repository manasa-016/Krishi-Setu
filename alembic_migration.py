"""add user_locations table

This is a draft migration file. When the plugin is merged into the main repo, 
you can drop this into `alembic/versions/` or run `alembic revision --autogenerate`.

Revision ID: ____________
Revises: ____________
Create Date: 2026-03-08 19:15:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        'user_locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )

def downgrade() -> None:
    op.drop_table('user_locations')
