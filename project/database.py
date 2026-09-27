from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False es necesario para SQLite cuando la app puede
# acceder a la conexión desde más de un hilo (por ejemplo, en un futuro
# servidor web con FastAPI).
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    """Crea el archivo de base de datos y todas las tablas declaradas
    en los modelos (Oficina, Persona), si todavía no existen."""
    SQLModel.metadata.create_all(engine)
