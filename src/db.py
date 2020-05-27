import sqlite3
import logging
import singleton


logger = logging.getLogger("DB")


class PlayersDB:
    def __init__(self):
        self.db = DbConnection()

    def players_password(self, player_name):
        username = player_name.decode()
        cur = self.db.execute(f"SELECT password FROM players WHERE player_name = '{username}'")
        results = cur.fetchall()
        if not results:
            return None
        return results[0][0]

    def add_wrong_login(self, player_name):
        pass


class DbConnection(metaclass=singleton.Singleton):
    def __init__(self):
        logger.info("INITING DATABASE")
        self.db = sqlite3.connect("db")
        if not self.check_tables():
            self.create_tables()

    def execute(self, cmd):
        logger.debug(f"Excuting cmd: {cmd}")
        return self.db.execute(cmd)

    def check_tables(self):
        return False

    def _create_table(self, table_name, colunms, extra):
        columns = ",".join(" ".join(col) for col in colunms)
        cmd = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns}, {extra});"
        logger.info(f"running cmd: {cmd}")
        cur = self.db.cursor()
        logger.info(f"cmd result: {cur.execute(cmd)}")
        

    def create_tables(self):
        logger.info("CREATING TABLES")
        self._create_table("players", 
                [["id", "int", "NOT NULL"],
                ["player_name", "string", "NOT NULL"],
                ["password", "string", "NOT NULL"]],
                "PRIMARY KEY ('id')")

        self._create_table("casinos",
                [["id", "int", "NOT NULL"],
                ["manager_id", "int"],
                ["total_chips", "int"],
                ["available_chips", "int"]],
                "PRIMARY KEY ('id')")

        self._create_table("chips",
                [["player_id", "int", "NOT NULL"],
                ["casino_id", "int", "NOT NULL"],
                ["amount", "int"]],
                "PRIMARY KEY ('player_id', 'casino_id')")

