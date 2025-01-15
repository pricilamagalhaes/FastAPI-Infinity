from config.database import table_registry
from sqlalchemy.orm import Mapped, mapped_column

@table_registry.mapped_as_dataclass()
class User:
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, init=False)
  username: Mapped[str] = mapped_column(init=True)
