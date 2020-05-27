from gameserver import GameServer
from db import DbConnection


if __name__ == "__main__":
    DbConnection()
    GameServer().run()
