from typing import Optional

from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import Oficina, Persona


# ------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------
def crear_oficina(nombre: str, direccion: str) -> int:
    with Session(engine) as session:
        oficina = Oficina(nombre=nombre, direccion=direccion)
        session.add(oficina)
        session.commit()
        session.refresh(oficina)
        print(f"Oficina creada: id={oficina.id} nombre={oficina.nombre!r}")
        return oficina.id


def crear_persona(
    nombre: str,
    oficina_id: int,
    edad: Optional[int] = None,
    puesto: Optional[str] = None,
) -> Optional[int]:
    with Session(engine) as session:
        oficina = session.get(Oficina, oficina_id)
        if not oficina:
            print(f"No existe una oficina con id={oficina_id}")
            return None

        persona = Persona(nombre=nombre, edad=edad, puesto=puesto)
        # Asociación mediante el atributo de relación (NO se asigna
        # persona.oficina_id a mano): SQLModel/SQLAlchemy se encarga
        # de completar la clave foránea al hacer commit.
        persona.oficina = oficina

        session.add(persona)
        session.commit()
        session.refresh(persona)
        print(
            f"Persona creada: id={persona.id} nombre={persona.nombre!r} "
            f"-> oficina={persona.oficina.nombre!r}"
        )
        return persona.id


# ------------------------------------------------------------------
# READ
# ------------------------------------------------------------------
def listar_personas_de_oficina(oficina_id: int) -> None:
    with Session(engine) as session:
        oficina = session.get(Oficina, oficina_id)
        if not oficina:
            print(f"No existe una oficina con id={oficina_id}")
            return

        print(f"Personas de la oficina {oficina.nombre!r}:")
        # Navegación de la relación uno a muchos: oficina.personas
        if not oficina.personas:
            print("  (sin personas asignadas)")
        for persona in oficina.personas:
            print(f"  - id={persona.id} {persona.nombre} ({persona.puesto})")


def listar_personas_con_join() -> None:
    """Consulta con JOIN explícito entre Persona y Oficina."""
    with Session(engine) as session:
        statement = select(Persona, Oficina).join(Oficina)
        resultados = session.exec(statement).all()

        print("Personas y su oficina (JOIN):")
        for persona, oficina in resultados:
            print(f"  - {persona.nombre} trabaja en {oficina.nombre} ({oficina.direccion})")


def buscar_personas_por_nombre(texto: str) -> None:
    """Filtro (WHERE) por nombre, usando coincidencia parcial."""
    with Session(engine) as session:
        statement = select(Persona).where(Persona.nombre.contains(texto))
        resultados = session.exec(statement).all()

        print(f"Personas cuyo nombre contiene {texto!r}:")
        if not resultados:
            print("  (sin resultados)")
        for persona in resultados:
            print(f"  - id={persona.id} {persona.nombre}")


# ------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------
def reasignar_persona(persona_id: int, nueva_oficina_id: int) -> None:
    with Session(engine) as session:
        persona = session.get(Persona, persona_id)
        nueva_oficina = session.get(Oficina, nueva_oficina_id)

        if not persona:
            print(f"No existe una persona con id={persona_id}")
            return
        if not nueva_oficina:
            print(f"No existe una oficina con id={nueva_oficina_id}")
            return

        oficina_anterior = persona.oficina.nombre if persona.oficina else "sin oficina"
        persona.oficina = nueva_oficina  # se reasigna vía relationship, no vía FK a mano
        session.add(persona)
        session.commit()
        session.refresh(persona)

        print(
            f"{persona.nombre} reasignada: {oficina_anterior!r} -> "
            f"{persona.oficina.nombre!r}"
        )


# ------------------------------------------------------------------
# DELETE
# ------------------------------------------------------------------
def eliminar_persona(persona_id: int) -> None:
    with Session(engine) as session:
        persona = session.get(Persona, persona_id)
        if not persona:
            print(f"No existe una persona con id={persona_id}")
            return
        nombre = persona.nombre
        session.delete(persona)
        session.commit()
        print(f"Persona eliminada: {nombre} (id={persona_id})")


def eliminar_oficina(oficina_id: int) -> None:
    """Elimina una oficina, siempre que no tenga personas asociadas.

    Nota (ver informe): SQLite/SQLModel, por defecto, NO impone la
    restricción de clave foránea a nivel de motor (no se ejecuta
    'PRAGMA foreign_keys=ON'), por lo que borrar una oficina con
    personas asociadas no lanzaría un error automáticamente: dejaría
    a esas personas con un oficina_id que ya no existe en la base
    (referencia "huérfana"). Para evitar ese estado inconsistente,
    la aplicación verifica explícitamente antes de borrar.
    """
    with Session(engine) as session:
        oficina = session.get(Oficina, oficina_id)
        if not oficina:
            print(f"No existe una oficina con id={oficina_id}")
            return

        if oficina.personas:
            print(
                f"No se puede eliminar la oficina {oficina.nombre!r}: "
                f"tiene {len(oficina.personas)} persona(s) asociada(s). "
                "Reasigná o eliminá esas personas primero."
            )
            return

        session.delete(oficina)
        session.commit()
        print(f"Oficina eliminada: {oficina.nombre} (id={oficina_id})")


# ------------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------------
def main() -> None:
    create_db_and_tables()

    print("=== CREATE ===")
    id_desarrollo = crear_oficina("Desarrollo", "Av. Colón 1234")
    id_rrhh = crear_oficina("Recursos Humanos", "Bv. San Juan 500")

    id_ana = crear_persona("Ana Gómez", id_desarrollo, edad=29, puesto="Backend Developer")
    id_luis = crear_persona("Luis Pérez", id_desarrollo, edad=34, puesto="Frontend Developer")
    id_marta = crear_persona("Marta Díaz", id_rrhh, edad=41, puesto="Analista de RRHH")

    print("\n=== READ ===")
    listar_personas_de_oficina(id_desarrollo)
    print()
    listar_personas_con_join()
    print()
    buscar_personas_por_nombre("Pérez")

    print("\n=== UPDATE ===")
    reasignar_persona(id_luis, id_rrhh)
    listar_personas_de_oficina(id_desarrollo)
    listar_personas_de_oficina(id_rrhh)

    print("\n=== DELETE ===")
    eliminar_persona(id_marta)
    eliminar_oficina(id_rrhh)   # todavía tiene a Luis -> debe rechazar el borrado
    eliminar_persona(id_luis)
    eliminar_oficina(id_rrhh)   # ahora sin personas -> se elimina sin problemas


if __name__ == "__main__":
    main()
