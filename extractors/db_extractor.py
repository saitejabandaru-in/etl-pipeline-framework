import pandas as pd
from sqlalchemy import create_engine, text


class DBExtractor:
    def __init__(self, connection_url: str, query: str) -> None:
        self.connection_url = connection_url
        self.query = query

    def extract(self) -> pd.DataFrame:
        engine = create_engine(self.connection_url)
        with engine.connect() as connection:
            return pd.read_sql_query(text(self.query), connection)
