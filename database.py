from config import (DATABASE_USER as user, DATABASE_PASSWORD as password, DATABASE_HOST as host,
                    DATABASE_PORT as port, DATABASE_NAME as db)

dsn = f"postgresql://{user}:{password}@{host}:{port}/{db}"
