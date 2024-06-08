class PostgreSQL:
    def __init__(self, database_user: str,
                 database_password: str,
                 database_host: str,
                 database_name: str):
        self.database_user = database_user
        self.database_password = database_password
        self.database_host = database_host
        self.database_name = database_name
