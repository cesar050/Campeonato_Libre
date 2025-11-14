# ⚽ Sistema Web de Gestión de Campeonatos Barriales

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![JWT](https://img.shields.io/badge/JWT-Auth-black.svg)](https://jwt.io/)

---
# Sistema Web de Gestión de Campeonatos Barriales

## Descripción del Proyecto

Sistema web desarrollado para digitalizar y automatizar la gestión de torneos de fútbol comunitarios. La plataforma transforma procesos manuales en una solución tecnológica que facilita la administración de campeonatos, mejora la experiencia de participantes y proporciona transparencia en el desarrollo de los torneos.

### Problemática Identificada

La organización de campeonatos deportivos en comunidades enfrenta desafíos por la gestión manual:
- Registro de equipos en documentos físicos susceptibles a pérdida
- Elaboración manual de calendarios con alta probabilidad de errores
- Registro informal de resultados y estadísticas
- Falta de comunicación efectiva con participantes
- Ausencia de control de acceso y seguridad de información

### Solución Implementada

Sistema web con:
- Registro digital de equipos, jugadores y documentación
- Generación automática de calendarios y fixtures
- Cálculo automático de tablas de posiciones y estadísticas
- Sistema de autenticación JWT con control de acceso por roles
- API REST documentada para integración con frontend

## Arquitectura del Sistema

### Patrón Arquitectónico

API REST Monolítica con arquitectura en capas:

```
┌─────────────────────────────────────────┐
│     CAPA DE PRESENTACIÓN (Routes)       │
├─────────────────────────────────────────┤
│   CAPA DE LÓGICA DE NEGOCIO (Models)    │
├─────────────────────────────────────────┤
│      CAPA DE PERSISTENCIA (MySQL)       │
└─────────────────────────────────────────┘
```

### Stack Tecnológico

**Backend:**
- Flask 3.0+ (Framework web Python)
- SQLAlchemy 2.0 (ORM)
- MySQL 8.0+ (Base de datos relacional)

**Seguridad:**
- Flask-JWT-Extended (Autenticación JWT)
- Bcrypt (Hash de contraseñas)
- Flask-CORS (Control de acceso)
- Flask-Limiter (Rate limiting)

**Validación:**
- Marshmallow (Schemas de validación)
- SQLAlchemy Validators

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py              # Factory pattern - Inicialización
│   ├── config.py                # Configuraciones por entorno
│   ├── extensions.py            # Extensiones Flask
│   │
│   ├── models/                  # Modelos de Base de Datos
│   │   ├── usuario.py           # Gestión de usuarios y roles
│   │   ├── equipo.py            # Información de equipos
│   │   ├── jugador.py           # Registro de jugadores
│   │   ├── campeonato.py        # Datos del campeonato
│   │   ├── partido.py           # Programación de partidos
│   │   ├── gol.py               # Registro de goles
│   │   ├── tarjeta.py           # Tarjetas amarillas/rojas
│   │   ├── alineacion.py        # Alineaciones por partido
│   │   ├── notificacion.py      # Sistema de notificaciones
│   │
│   ├── routes/                  # Endpoints REST API
│   │   ├── auth_routes.py       # Autenticación (login, register, logout)
│   │   ├── equipo_routes.py     # CRUD Equipos
│   │   ├── jugador_routes.py    # CRUD Jugadores
│   │   ├── campeonato_routes.py # CRUD Campeonatos
│   │   ├── partido_routes.py    # CRUD Partidos
│   │   ├── gol_routes.py        # Registro de goles
│   │   ├── tarjeta_routes.py    # Registro de tarjetas
│   │   └── estadistica_routes.py # Estadísticas y tablas
│   │
│   ├── middlewares/             # Middlewares personalizados
│   │   ├── auth.py              # Decoradores de autenticación
│   │   └── error_handler.py     # Manejo de errores
│   │
│   ├── security/                # Módulos de seguridad
│   │   ├── jwt_handler.py       # Gestión de JWT
│   │   ├── password.py          # Hash y validación
│   │   └── validators.py        # Validadores de entrada
│   │
│   └── utils/                   # Utilidades
│       ├── responses.py         # Respuestas estandarizadas
│       └── helpers.py           # Funciones auxiliares
│
├── uploads/                     # Archivos subidos
│   ├── documentos/              # PDFs de jugadores
│   └── logos/                   # Logos de equipos
│
├── .env.example                 # Template de variables
├── requirements.txt             # Dependencias Python
└── run.py                       # Entry point

├──  alineaciones-service/        # Microservicio
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── .env.example
│   ├── requirements.txt
│   ├── run.py
│   └── README.md

database/
└── campeonato.sql               # Schema completo

docs/
├── architecture/                # Diagramas C4
│   ├── context-diagram.png
│   ├── container-diagram.png
│   ├── component-diagram.png
│   └── code-diagram.png
├── api-collection.postman.json  # Colección Postman
└── informe-seguridad.pdf        # Reporte de seguridad
```

## Roles de Usuario

### Administrador
- Gestión completa de campeonatos
- Aprobación de equipos
- Creación y modificación de partidos
- Registro de resultados y eventos
- Gestión de usuarios

### Líder de Equipo
- Registro de su equipo
- Gestión de jugadores del equipo
- Definición de alineaciones
- Visualización de calendario y resultados

### Espectador
- Visualización de partidos y resultados
- Consulta de tablas de posiciones
- Acceso a estadísticas de jugadores
- Información pública del campeonato

## Seguridad

### Autenticación JWT
- Access tokens (15 minutos)
- Refresh tokens (30 días)
- Blacklist de tokens revocados
- Claims personalizados para roles

### Protecciones Implementadas
- Hash de contraseñas con Bcrypt (factor 12)
- Control de acceso basado en roles (RBAC)
- Rate limiting por IP y usuario
- Validación de entrada y sanitización
- Protección contra SQL Injection
- CORS configurado
- Logs de seguridad y auditoría

### Cumplimiento OWASP Top 10
- A01: Control de acceso implementado
- A02: Cifrado de contraseñas
- A03: Validación de entrada
- A04: Configuración segura
- A05: Autenticación robusta
- A07: Logs y monitoreo

## Instalación

### Prerequisitos
- Python 3.9+
- MySQL 8.0+
- pip
- virtualenv

### Configuración

1. Clonar el repositorio
```bash
git clone <repository-url>
cd campeonato-barrial
```

2. Crear entorno virtual
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con configuraciones locales
```

5. Crear base de datos
```bash
mysql -u root -p
CREATE DATABASE gestion_campeonato;
exit
```

6. Importar schema
```bash
mysql -u root -p gestion_campeonato < database/campeonato.sql
```

7. Iniciar servidor
```bash
python run.py
```

API disponible en: `http://localhost:5000`

## Endpoints Principales

### Autenticación
- POST `/api/auth/register` - Registro de usuario
- POST `/api/auth/login` - Inicio de sesión
- POST `/api/auth/refresh` - Renovar token
- POST `/api/auth/logout` - Cerrar sesión

### Equipos
- GET `/api/equipos` - Listar equipos
- POST `/api/equipos` - Crear equipo
- GET `/api/equipos/<id>` - Detalle de equipo
- PUT `/api/equipos/<id>` - Actualizar equipo
- DELETE `/api/equipos/<id>` - Eliminar equipo

### Partidos
- GET `/api/partidos` - Listar partidos
- POST `/api/partidos` - Crear partido
- GET `/api/partidos/<id>` - Detalle de partido
- PUT `/api/partidos/<id>` - Actualizar partido

### Estadísticas
- GET `/api/estadisticas/tabla` - Tabla de posiciones
- GET `/api/estadisticas/goleadores` - Tabla de goleadores

Documentación completa en: `/docs/api-collection.postman.json`

## Control de Versiones

### GitFlow
- `main`: Producción estable
- `develop`: Desarrollo integrado
- `feature/*`: Nuevas funcionalidades


## Autor

Cesar Ramos - Desarrollo basado en plataformas 

