import pandas as pd
from sqlalchemy import create_engine


class WarehouseLoader:
    def __init__(self, connection_url: str, table: str) -> None:
        self.connection_url = connection_url
        self.table = table

    def load(self, frame: pd.DataFrame) -> None:
        engine = create_engine(self.connection_url)
        with engine.begin() as connection:
            frame.to_sql(self.table, connection, if_exists="replace", index=False)
