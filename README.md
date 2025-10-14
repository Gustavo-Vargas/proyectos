# Curso Django

Proyectos prácticos de Python con Django explorando conceptos fundamentales del framework.

## Proyectos

**Hola Mundo** - CRUD básico con SQLite y Django Admin

**Videojuegos** - Gestión con categorías, stock, MySQL y AdminLTE

## Stack
Django 5.2.6 · Python 3.x · MySQL · SQLite · Docker · AdminLTE

## Comandos

**Hola Mundo**
```bash
cd hola_mundo
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver
```

**Videojuegos**
```bash
docker-compose up --build
docker-compose exec app bash
python3 manage.py migrate && python3 manage.py runserver 0:8000
```

→ http://localhost:8000