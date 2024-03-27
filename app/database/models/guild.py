# TODO: finish documentation

# Standard modules
from __future__ import annotations

# Third party modules
from datetime import datetime

from arrow import now
from arrow.arrow import Arrow
from dateutil.tz import gettz
from sqlalchemy import ARRAY, BigInteger, DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Internal modules
from app.database.models import Base


class Guild(Base):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    last_activity: Mapped[str] = mapped_column(String, server_default="None")
    last_active_channel: Mapped[int] = mapped_column(BigInteger, default=0)
    last_active_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=Arrow(1970, 1, 1, 0, 0, tzinfo=gettz("US/Central")).datetime.isoformat(),
        default=Arrow(1970, 1, 1, 0, 0, tzinfo=gettz("US/Central")).datetime)
    idle_times: Mapped[int] = mapped_column(ARRAY(Integer), default=[])
    average_idle_time: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    recent_averages: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
    status: Mapped[str] = mapped_column(String, nullable=False, server_default="new")
    settings: Mapped[dict] = mapped_column(JSON, default={})
    members = relationship(
        "MemberShard",
        lazy="joined",
        cascade="all,delete",
    )
    date_added: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=now(gettz('US/Central')).datetime.isoformat(),
        default=now(gettz("US/Central")).datetime,
    )

    def __repr__(self):
        return (
            f"<Guild (id = {self.id}, guild_id = {self.guild_id},  name = {self.name}, "
            f"last_activity = {self.last_activity}, last_active_channel = "
            f"{self.last_active_channel}, last_active_ts = {self.last_active_timestamp}, idle_times = "
            f"{self.idle_times} average_idle_time = {self.average_idle_time}, recent_averages = "
            f"{self.recent_averages}, status = {self.status}, settings = {self.settings}, members = "
            f"{self.members}, date_added = {self.date_added})>"
        )

    def as_dict(self):
        guild_dict = {
            c.name: getattr(self, c.name) for c in self.__table__.columns.values()
        }
        guild_dict["members"] = []

        for member in self.members:
            member_dict = member.as_dict()
            guild_dict["members"].append(member_dict)

        return guild_dict
