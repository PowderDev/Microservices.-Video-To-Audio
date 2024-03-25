import mariadb, os


def create_connection_pool():
    pool = mariadb.ConnectionPool(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("AUTH_DB_USER"),
        password=os.environ.get("AUTH_DB_PASSWORD"),
        database=os.environ.get("AUTH_DB_NAME"),
        port=3306,
        pool_name="auth-connection-pool",
        pool_size=3,
        pool_validation_interval=250,
    )

    return pool


def get_connection_from_pool(pool):
    pconn = pool.get_connection()
    cur = pconn.cursor()

    return cur
