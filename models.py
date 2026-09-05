from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from databases import Base

class Equipement(Base):
    __tablename__ = "equipements"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    adresse_ip = Column(String(45), unique=True, nullable=False, index=True)
    type_equipement = Column(String(50), default="routeur")
    actif = Column(Boolean, default=True)
    date_creation = Column(DateTime, default=datetime.utcnow) 
    # cascade="all, delete-orphan" : supprimer l'équipement supprime ses interfaces     
    interfaces = relationship("Interface", back_populates="equipement", cascade="all, delete-orphan")

class Interface(Base):
    __tablename__ = "interfaces"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    statut = Column(String(20), default="down")
    vlan = Column(Integer, nullable=True)
    equipement_id = Column(Integer, ForeignKey("equipements.id"), nullable=False)
    equipement = relationship("Equipement", back_populates="interfaces")

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom_utilisateur = Column(String(50), unique=True, nullable=False, index=True)
    mot_de_passe_hache = Column(String(255), nullable=False)   
    # jamais en clair     
    role = Column(String(20), default="lecteur")