from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Oficina(SQLModel, table=True):
    """Una oficina puede tener varias personas (relación uno a muchos)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    direccion: str

    # Lado "uno" de la relación: lista de personas que pertenecen a esta oficina.
    personas: List["Persona"] = Relationship(back_populates="oficina")


class Persona(SQLModel, table=True):
    """Cada persona pertenece a una única oficina."""

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    edad: Optional[int] = None
    puesto: Optional[str] = None

    # Clave foránea explícita (necesaria para la tabla), pero la asociación
    # entre objetos se maneja siempre a través del atributo "oficina" de abajo,
    # nunca asignando oficina_id a mano.
    oficina_id: Optional[int] = Field(default=None, foreign_key="oficina.id")

    # Lado "muchos" de la relación: la oficina a la que pertenece esta persona.
    oficina: Optional[Oficina] = Relationship(back_populates="personas")
