from models.database import Base, fk_int
from sqlalchemy import DECIMAL, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Currency(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str]
    sign: Mapped[str]

    base_rate: Mapped[list["ExchangeRate"]] = relationship(
        foreign_keys="ExchangeRate.base_currency_id",
        back_populates="base_currency",
        cascade="all, delete-orphan",
    )
    target_rate: Mapped[list["ExchangeRate"]] = relationship(
        foreign_keys="ExchangeRate.target_currency_id",
        back_populates="target_currency",
        cascade="all, delete-orphan",
    )


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    base_currency_id: Mapped[fk_int]
    target_currency_id: Mapped[fk_int]
    rate: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=9, scale=6))

    __table_args__ = (
        UniqueConstraint(
            "base_currency_id", "target_currency_id", name="unique_currency_pair"
        ),
        CheckConstraint("rate > 0", name="check_rate_positive"),
    )

    base_currency: Mapped["Currency"] = relationship(
        foreign_keys="base_currency_id", back_populates="base_rate"
    )
    target_currency: Mapped["Currency"] = relationship(
        foreign_keys="target_currency_id", back_populates="target_rate"
    )
