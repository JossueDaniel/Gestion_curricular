# Gestión Curricular
Sistema web que permite gestionar y digitalizar los procesos que conlleva el syllabus de las asignaturas, de igual manera permite gestionar las asignaturas y docentes
respectivos.

## Requisitos previos
- python 3.12 o superior
- docker
- docker-compose

## Estructura del proyecto
```plaintext
Gestion_curricular/
├── Dockerfile
├── compose.yml
├── requirements.txt
└── django_project/
    ├── manage.py
    ├── accounts/
    ├── asignaturas/
    ├── contenidos/
    ├── syllabus/
    ├── static/
    ├── templates/
    └── django_project/
        └── settings.py
```

## Configuración y ejecución
### 1. Clonar el repositorio
```bash
git clone https://github.com/JossueDaniel/Gestion_curricular.git
```

```bash
cd Gestion_curricular
```

### 2. Establecer las variables de entorno
Crear un archivo .env en la raíz del proyecto
```plaintext
SECRET_KEY=clave-secreta-django
DEBUG=True
```

### 3. Construir y levantar los contenedores
```bash
docker compose up -d --build
```

### 4. Ejecutar las migraciones
```bash
docker compose exec web python manage.py migrate
```

### 5. Crear un superusuario (opcional)
```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Acceder al servidor de desarrollo
http://localhost:8000/
