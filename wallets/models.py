import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func, text, types
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class TransactionType(str, Enum):
    inbound = 'inbound'
    outbound = 'outbound'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text('gen_random_uuid()'),
    )
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    full_name: Mapped[str]

    wallets: Mapped[list['Wallet']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Wallet:
    __tablename__ = 'wallets'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text('gen_random_uuid()'),
    )
    title: Mapped[str]
    description: Mapped[str]
    balance: Mapped[float]

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(init=False, back_populates='wallets')

    transactions: Mapped[list['Transaction']] = relationship(
        init=False, back_populates='wallet', cascade='all, delete-orphan'
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Transaction:
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text('gen_random_uuid()'),
    )
    transaction_type: Mapped[TransactionType]
    value: Mapped[float]
    description: Mapped[str]

    wallet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('wallets.id')
    )
    wallet: Mapped[User] = relationship(
        init=False, back_populates='transaction'
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
