
from pydantic import BaseModel, Field, field_validator
import ipaddress


# ==================================================
# EQUIPEMENTS
# ==================================================

class EquipementCreate(BaseModel):
    nom: str = Field(min_length=2, max_length=100)
    adresse_ip: str
    type_equipement: str = "routeur"

    @field_validator("adresse_ip")
    @classmethod
    def validate_ip(cls, value: str) -> str:
        try:
            ipaddress.ip_address(value)
        except ValueError:
            raise ValueError("Adresse IP invalide")
        return value


class EquipementUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=2, max_length=100)
    adresse_ip: str | None = None
    type_equipement: str | None = None
    actif: bool | None = None

    @field_validator("adresse_ip")
    @classmethod
    def validate_ip(cls, value: str | None) -> str | None:
        if value is not None:
            try:
                ipaddress.ip_address(value)
            except ValueError:
                raise ValueError("Adresse IP invalide")
        return value


class EquipementResponse(BaseModel):
    id: int
    nom: str
    adresse_ip: str
    type_equipement: str
    actif: bool

    model_config = {
        "from_attributes": True
    }


# ==================================================
# UTILISATEURS
# ==================================================

class UtilisateurCreate(BaseModel):
    nom_utilisateur: str = Field(min_length=3, max_length=50)
    mot_de_passe: str = Field(min_length=6, max_length=100)
    role: str = "lecteur"


class UtilisateurResponse(BaseModel):
    id: int
    nom_utilisateur: str
    role: str

    model_config = {
        "from_attributes": True
    }


# ==================================================
# INTERFACES
# ==================================================

class InterfaceCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=50)
    statut: str = "down"
    vlan: int | None = None
    equipement_id: int


class InterfaceUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=1, max_length=50)
    statut: str | None = None
    vlan: int | None = None
    equipement_id: int | None = None


class InterfaceResponse(BaseModel):
    id: int
    nom: str
    statut: str
    vlan: int | None
    equipement_id: int

    model_config = {
        "from_attributes": True
    }

