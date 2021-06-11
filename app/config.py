import os


class Config:
    """
    docstring
    """
    class MySql:
        DATABASE_SERVER = os.getenv('RDS_SERVER')
        DATABASE_USER = os.getenv('RDS_USER')
        DATABASE_PASS = os.getenv('RDS_PASS')
        DATABASE_NAME = os.getenv('RDS_DBZ', "my_social")
