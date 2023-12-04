from .settings import DEBUG
if DEBUG:
    import pymysql
    pymysql.install_as_MySQLdb()