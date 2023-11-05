from databases import Database


# Database URL for SQLite database (in-memory database for now)
database_url = "sqlite:///./database.db"

database = Database(database_url)

def get_database():
    return database

async def startup_db_connection():
    await database.connect()

async def shutdown_db_connection():
    await database.disconnect()

async def create_group_table():
    query = "CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY, name TEXT, dishes TEXT, restrictions TEXT)"
    database = get_database();

    await database.execute(query)