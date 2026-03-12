MesVoisins

Application web Django d'échange de compétences entre utilisateurs.

Fonctionnalités

- Consultation des compétences et des services acceptés (visiteur)
- Gestion de ses compétences (ajout/suppression)
- Création de demandes de service (créneau + activité + compétence recherchée)
- Consultation et postulation aux demandes correspondant à ses compétences
- Système d'échange réciproque : mise en relation d'utilisateurs dont les compétences et besoins se complètent
- Catégories de compétences avec code couleur

Installation

pip install -r requirements.txt,
python manage.py migrate,
python manage.py runserver

Stack
- Python / Django
- SQLite
- Bootstrap 5
