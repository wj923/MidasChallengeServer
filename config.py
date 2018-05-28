DB_HOST="172.17.140.251"
DB_USERNAME="root"
DB_PASSWORD="codms218"
DB_NAME="cafemidas"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USERNAME,
                                                                   DB_PASSWORD,
                                                                   DB_HOST,
                                                                   DB_NAME)
