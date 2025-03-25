from typing import Annotated

from sqlalchemy import DECIMAL, UniqueConstraint, CheckConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)


fk_int = Annotated[int, mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))]


class CurrencyModel(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(
        String(3), index=True, unique=True, nullable=False
    )
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    sign: Mapped[str] = mapped_column(String(1), nullable=False)

    base_rate: Mapped[list["ExchangeRateModel"]] = relationship(
        foreign_keys="ExchangeRateModel.base_currency_id",
        lazy="selectin",
        back_populates="base_currency",
        cascade="all, delete-orphan",
    )
    target_rate: Mapped[list["ExchangeRateModel"]] = relationship(
        foreign_keys="ExchangeRateModel.target_currency_id",
        lazy="selectin",
        back_populates="target_currency",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"CurrencyModels(id='{self.id}', code='{self.code}', fullname='{self.fullname}', sign='{self.sign}')"


class ExchangeRateModel(Base):
    __tablename__ = "exchange_rates"

    base_currency_id: Mapped[fk_int] = mapped_column()
    target_currency_id: Mapped[fk_int] = mapped_column()
    rate: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=9, scale=6))

    __table_args__ = (
        UniqueConstraint(
            "base_currency_id", "target_currency_id", name="unique_currency_pair"
        ),
        CheckConstraint("rate > 0", name="check_rate_positive"),
    )

    base_currency: Mapped["CurrencyModel"] = relationship(
        foreign_keys="ExchangeRateModel.base_currency_id",
        lazy="joined",
        back_populates="base_rate",
    )
    target_currency: Mapped["CurrencyModel"] = relationship(
        foreign_keys="ExchangeRateModel.target_currency_id",
        lazy="joined",
        back_populates="target_rate",
    )

    def __repr__(self):
        return f"ExchangeRateModel(id='{self.id}', base_currency_id='{self.base_currency_id}', target_currency_id='{self.target_currency_id}', rate='{self.rate}')"
