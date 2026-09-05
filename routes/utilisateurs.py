
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from databases import get_db
from models import Utilisateur
from schemas import (
    UtilisateurCreate,
    UtilisateurResponse,
)


router = APIRouter(
    prefix="/utilisateurs",
    tags=["Utilisateurs"]
)

password_hash = PasswordHash.recommended()


# ==================================================
# CREATE
# ==================================================

@router.post(
    "",
    response_model=UtilisateurResponse,
    status_code=status.HTTP_201_CREATED
)
def create_utilisateur(
    utilisateur: UtilisateurCreate,
    db: Session = Depends(get_db)
):

    # Vérifier si le nom d'utilisateur existe déjà
    existing = (
        db.query(Utilisateur)
        .filter(
            Utilisateur.nom_utilisateur == utilisateur.nom_utilisateur
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Ce nom d'utilisateur existe déjà"
        )

    # Hacher automatiquement le mot de passe
    mot_de_passe_hache = password_hash.hash(
        utilisateur.mot_de_passe
    )

    # Créer l'utilisateur
    new_utilisateur = Utilisateur(
        nom_utilisateur=utilisateur.nom_utilisateur,
        mot_de_passe_hache=mot_de_passe_hache,
        role=utilisateur.role
    )

    db.add(new_utilisateur)
    db.commit()
    db.refresh(new_utilisateur)

    return new_utilisateur


# ==================================================
# READ ALL
# ==================================================

@router.get(
    "",
    response_model=list[UtilisateurResponse]
)
def get_utilisateurs(
    db: Session = Depends(get_db)
):

    return db.query(Utilisateur).all()

