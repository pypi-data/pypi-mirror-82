# -*- coding: utf-8 -*-

import aiomysql
from mysql.connector.pooling import MySQLConnectionPool
from typing import Optional, Union, AsyncGenerator

__all__ = (
    'SQLParams',
    'SQLResult',
    'SQLPoolWrapper',
    'AsyncSQLPoolWrapper'
)

SQLParams = tuple[Union[int, float, str]]
SQLResult = dict[str, Union[int, float, str]]

class SQLPoolWrapper:
    __slots__ = ('conn',)

    def __init__(self, **kwargs):
        self.conn = MySQLConnectionPool(autocommit = True, **kwargs)

    def execute(self, query: str, params: SQLParams) -> int:
        if not (cnx := self.conn.get_connection()):
            raise Exception('MySQL: Failed to retrieve a worker.')

        cursor = cnx.cursor()
        cursor.execute(query, params)
        cursor.fetchmany()

        # Since we are executing a command, we
        # simply return the last row affected's id.
        res = cursor.lastrowid

        [x.close() for x in (cursor, cnx)]
        return res

    def fetch(self, query: str, params: SQLParams = (), _all: bool = False,
              _dict: bool = True) -> Optional[Union[tuple[SQLResult], SQLResult]]:
        if not (cnx := self.conn.get_connection()):
            raise Exception('MySQL: Failed to retrieve a worker.')

        cursor = cnx.cursor(dictionary = _dict, buffered = True)
        cursor.execute(query, params)

        # We are fetching data.
        res = (cursor.fetchall if _all else cursor.fetchone)()

        [x.close() for x in (cursor, cnx)]
        return res

    def fetchall(self, query: str, params: SQLParams = (), _dict: bool = True
                ) -> Optional[Union[tuple[SQLResult], SQLResult]]:
        return self.fetch(query, params, _all = True, _dict = _dict)

# Should work, just disabled since
# there's no async server yet xd.
class AsyncSQLPoolWrapper:
    __slots__ = ('pool',)

    def __init__(self):
        self.pool: Optional[aiomysql.Pool] = None

    async def connect(self, **config):
        self.pool = await aiomysql.create_pool(**config)

    async def execute(self, query: str,
                      params: SQLParams) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                await conn.commit()

                lastrowid = cur.lastrowid

        return lastrowid

    async def fetch(self, query: str,
                    params: Optional[SQLParams] = None,
                    _all: bool = False, _dict: bool = True
                   ) -> Optional[Union[tuple[SQLResult], SQLResult]]:
        cursor_type = aiomysql.DictCursor if _dict \
              else aiomysql.Cursor

        async with self.pool.acquire() as conn:
            async with conn.cursor(cursor_type) as cur:
                await cur.execute(query, params)
                res = await (cur.fetchall if _all else cur.fetchone)()

        return res

    async def fetchall(self, query: str,
                       params: Optional[SQLParams] = None,
                       _dict: bool = True
                       ) -> Optional[Union[tuple[SQLResult], SQLResult]]:
        return await self.fetch(query, params, _all = True, _dict = _dict)

    async def iterall(self, query: str, params: Optional[SQLParams] = None,
                      _dict: bool = True) -> AsyncGenerator[SQLResult, None]:
        cursor_type = aiomysql.DictCursor if _dict \
                 else aiomysql.Cursor

        async with self.pool.acquire() as conn:
            async with conn.cursor(cursor_type) as cur:
                await cur.execute(query, params)

                async for row in cur:
                    yield row
