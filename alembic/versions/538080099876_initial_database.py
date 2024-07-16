"""initial_database

Revision ID: 538080099876
Revises: 
Create Date: 2024-07-16 12:08:08.720046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '538080099876'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.String(), nullable=True),
    sa.Column('receiver', sa.String(), nullable=True),
    sa.Column('subject', sa.String(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('is_processed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emails_id'), 'emails', ['id'], unique=False)
    op.create_index(op.f('ix_emails_receiver'), 'emails', ['receiver'], unique=False)
    op.create_index(op.f('ix_emails_sender'), 'emails', ['sender'], unique=False)
    op.create_index(op.f('ix_emails_subject'), 'emails', ['subject'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_emails_subject'), table_name='emails')
    op.drop_index(op.f('ix_emails_sender'), table_name='emails')
    op.drop_index(op.f('ix_emails_receiver'), table_name='emails')
    op.drop_index(op.f('ix_emails_id'), table_name='emails')
    op.drop_table('emails')
    # ### end Alembic commands ###