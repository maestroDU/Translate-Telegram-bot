from typing import Dict, List, Optional
from contextlib import suppress

from sqlalchemy import select, update, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from bot.db.models import HistoryEntry

# get data

async def get_history(session: AsyncSession, telegram_id: int) -> List[HistoryEntry]:
    request = await session.execute(
        select(HistoryEntry).where(HistoryEntry.telegram_id == telegram_id).limit(10)
    )
    
    return request.scalars().all()

# modify data

async def add_history(session: AsyncSession, telegram_id: int, translate_from: str, translate_to: str) -> None:
    entry = HistoryEntry()
    entry.telegram_id = telegram_id
    entry.translate_from = translate_from
    entry.translate_to = translate_to
    session.add(entry)
    await session.commit()