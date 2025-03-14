"""Sql Alchemy wrapper around a database"""
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
class SqlDatabase:
    """Sql Alchemy wrapper around a database"""
    
    def __init__(self, database_engine: Engine):
        self._engine = database_engine
        
    @classmethod
    def from_uri(cls, uri: str)->"SqlDatabase":
        return cls(create_engine(uri))
        
    @property
    def dialect(self)-> str:
        return self._engine.dialect.name
    
    @property
    def table_info(self) ->str:
        """Information about tables in database."""
        template = "The {table_name} has columns {columns_str}"
        inspector = inspect(self._engine)
        tables = []
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name=table_name):
                columns.append(column)
            columns_str = ",".join(columns)
            table_str = template.format(table_name = table_name, columns_str=columns_str)
            tables.append(table_str)
        return "\n".join(tables)

    def run(self, command: str)->str:
        """Execute a SQL command and return the results"""
        result = self._engine.execute(command).fetch_all()
        return str(result)