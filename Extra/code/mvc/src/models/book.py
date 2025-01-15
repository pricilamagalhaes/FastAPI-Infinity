from config.database import table_registry
from sqlalchemy.orm import Mapped, mapped_column

@table_registry.mapped_as_dataclass()
class Book:
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(init=True)
    author: Mapped[str] = mapped_column(init=True)
    description: Mapped[str] = mapped_column(init=True)