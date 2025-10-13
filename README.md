# Curso Django

Proyectos prácticos del curso de Python con Django, explorando conceptos fundamentales del framework.

## Proyectos

### Hola Mundo
Proyecto inicial con CRUD básico de artículos.
- SQLite3
- Modelos con presentación y colores
- Django Admin

### Videojuegos
Sistema de gestión con categorización y stock.
- MySQL/MariaDB
- CRUD completo con categorías
- Interfaz AdminLTE
- Docker

## Stack
Django 5.2.6 | Python 3.x | MySQL | SQLite | Docker | AdminLTE

## Uso

**Hola Mundo**
```bash
cd hola_mundo
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Videojuegos**
```bash
docker-compose up --build
docker-compose exec app bash
python3 manage.py migrate
python3 manage.py runserver 0:8000
```

Acceso: http://localhost:8000