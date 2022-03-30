import aiomysql
import os
import asyncio

from typing import Tuple, Any

loop = asyncio.get_event_loop()

async def the_database() -> Tuple[Any, Any]:
    """ Gets the database's connection. """

    pool = await aiomysql.create_pool(
        host=os.getenv('SLOTH_DB_HOST'),
        user=os.getenv('SLOTH_DB_USER'),
        password=os.getenv('SLOTH_DB_PASSWORD'),
        db=os.getenv('SLOTH_DB_NAME'),
        loop=loop
    )

    db = await pool.acquire()
    mycursor = await db.cursor()
    return mycursor, db