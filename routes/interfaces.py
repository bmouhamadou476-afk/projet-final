from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from databases import get_db
from models import Interface, Equipement
from schemas import (
    InterfaceCreate,
    InterfaceUpdate,
    InterfaceResponse,
)


router = APIRouter(
    prefix="/interfaces",
    tags=["Interfaces"]
)


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "",
    response_model=InterfaceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_interface(
    interface: InterfaceCreate,
    db: Session = Depends(get_db)
):

    # Vérifier que l'équipement existe
    equipement = (
        db.query(Equipement)
        .filter(Equipement.id == interface.equipement_id)
        .first()
    )

    if not equipement:
        raise HTTPException(
            status_code=404,
            detail="Équipement introuvable"
        )

    new_interface = Interface(
        nom=interface.nom,
        statut=interface.statut,
        vlan=interface.vlan,
        equipement_id=interface.equipement_id
    )

    db.add(new_interface)
    db.commit()
    db.refresh(new_interface)

    return new_interface


# ==========================================================
# READ ALL
# ==========================================================

@router.get(
    "",
    response_model=list[InterfaceResponse]
)
def get_interfaces(
    db: Session = Depends(get_db)
):
    return db.query(Interface).all()


# ==========================================================
# READ ONE
# ==========================================================

@router.get(
    "/{interface_id}",
    response_model=InterfaceResponse
)
def get_interface(
    interface_id: int,
    db: Session = Depends(get_db)
):

    interface = (
        db.query(Interface)
        .filter(Interface.id == interface_id)
        .first()
    )

    if not interface:
        raise HTTPException(
            status_code=404,
            detail="Interface introuvable"
        )

    return interface


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{interface_id}",
    response_model=InterfaceResponse
)
def update_interface(
    interface_id: int,
    data: InterfaceUpdate,
    db: Session = Depends(get_db)
):

    interface = (
        db.query(Interface)
        .filter(Interface.id == interface_id)
        .first()
    )

    if not interface:
        raise HTTPException(
            status_code=404,
            detail="Interface introuvable"
        )

    update_data = data.model_dump(exclude_unset=True)

    # Si on change d'équipement, vérifier qu'il existe
    if "equipement_id" in update_data:
        equipement = (
            db.query(Equipement)
            .filter(
                Equipement.id == update_data["equipement_id"]
            )
            .first()
        )

        if not equipement:
            raise HTTPException(
                status_code=404,
                detail="Équipement introuvable"
            )

    for field, value in update_data.items():
        setattr(interface, field, value)

    db.commit()
    db.refresh(interface)

    return interface


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{interface_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_interface(
    interface_id: int,
    db: Session = Depends(get_db)
):

    interface = (
        db.query(Interface)
        .filter(Interface.id == interface_id)
        .first()
    )

    if not interface:
        raise HTTPException(
            status_code=404,
            detail="Interface introuvable"
        )

    db.delete(interface)
    db.commit()

    return None