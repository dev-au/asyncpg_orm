import time

from asyncpg import Connection
import asyncpg
import logging
from asyncpg.pool import Pool
from .connector import PostgreSQL


class Database:
    pool: Pool
    echo: False

    def __init__(self, database_options: PostgreSQL, echo=False):
        self.database_options = database_options
        self.echo = echo

    async def start_session(self):
        self.pool = await asyncpg.create_pool(
            user=self.database_options.database_user,
            password=self.database_options.database_password,
            host=self.database_options.database_host,
            database=self.database_options.database_name
        )
        logging.warn("PostgreSQL session is running...")
        time.sleep(1)

    async def __cursor__(self, command, *args,
                         fetch: bool = False,
                         fetchrow: bool = False,
                         execute: bool = False
                         ):
        if self.echo:
            print_command = command
            for i in range(1, print_command.count("$") + 1):
                print_command = print_command.replace(f"${i}", f"{list(args)[i - 1]}")
            print(print_command)
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            if self.echo:
                if fetch:
                    if len(result) == 0:
                        print("    ")
                        return result
                    print_result = []
                    maxs = []
                    c_names = []
                    for result_name in result[0].keys():
                        maxs.append(len(result_name))
                        c_names.append(result_name)
                    for result_one in result:
                        row = []
                        i = 0
                        for value in result_one.values():
                            row.append(value)
                            if maxs[i] < len(str(value)):
                                maxs[i] = len(str(value))
                            i += 1
                        print_result.append(row)
                    i = 0
                    line = 0
                    print("  |", end="")
                    for c_name in c_names:
                        pstr = f"  {c_name}{(maxs[i] - len(c_name)) * ' '}"
                        print(pstr, end="|")
                        line += len(pstr) + 1
                        i += 1
                    print()
                    print("  ", "~" * line)

                    for row_one in print_result:
                        print("  |", end="")
                        i = 0
                        line = 0
                        for c_name in row_one:
                            pstr = f"  {c_name}{(maxs[i] - len(str(c_name))) * ' '}"
                            print(pstr, end="|")
                            line += len(pstr) + 1
                            i += 1
                        print()
                        print("  ", "-" * line)
                elif execute:
                    print("   ", result)
                elif fetchrow:
                    try:
                        maxs = []
                        c_names = []

                        for result_name in result.keys():
                            maxs.append(len(result_name))
                            c_names.append(result_name)
                        row = []
                        i = 0
                        for value in result.values():
                            row.append(value)
                            if maxs[i] < len(str(value)):
                                maxs[i] = len(str(value))
                            i += 1
                        i = 0
                        line = 0
                        print("  |", end="")
                        for c_name in c_names:
                            pstr = f"  {c_name}{(maxs[i] - len(c_name)) * ' '}"
                            print(pstr, end="|")
                            line += len(pstr) + 1
                            i += 1
                        print()
                        print("  ", "~" * line)
                        i = 0
                        print("  |", end="")
                        for c_name in row:
                            pstr = f"  {c_name}{(maxs[i] - len(str(c_name))) * ' '}"
                            print(pstr, end="|")
                            line += len(pstr) + 1
                            i += 1
                        print()
                    except AttributeError:
                        print("   ", None)

            return result

    async def stop_session(self):
        await self.pool.close()
        logging.warn("PostgreSQL session was stopped.")
