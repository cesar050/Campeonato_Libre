# ⚽ Sistema Web de Gestión de Campeonatos Barriales

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![JWT](https://img.shields.io/badge/JWT-Auth-black.svg)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Descripción del Proyecto

El **Sistema Web de Gestión de Campeonatos Barriales** es una plataforma integral desarrollada para digitalizar y automatizar la organización completa de torneos de fútbol comunitarios. Este sistema transforma procesos tradicionalmente manuales y propensos a errores en una solución tecnológica robusta, escalable y segura que facilita la gestión administrativa, mejora la experiencia de los participantes y proporciona transparencia total en el desarrollo de los campeonatos.

### 🎯 Contexto y Problemática

En la mayoría de comunidades y barrios de Ecuador y Latinoamérica, la organización de campeonatos deportivos enfrenta desafíos significativos derivados de la gestión manual de información:

#### Problemas Identificados:

**Gestión de Equipos e Inscripciones:**
- Los equipos se registran en hojas de papel que pueden extraviarse o dañarse
- No existe un control centralizado de la información de los equipos
- La validación de documentos de jugadores es manual y susceptible a fraudes
- No hay trazabilidad del proceso de aprobación de equipos

**Programación de Partidos:**
- Los calendarios se elaboran manualmente, lo que consume tiempo y genera errores
- Las modificaciones de horarios no se comunican eficientemente
- No existe un registro histórico confiable de los encuentros

**Registro de Resultados:**
- Los resultados se anotan en cuadernos físicos que pueden perderse
- Las estadísticas de jugadores (goles, tarjetas, asistencias) son difíciles de rastrear
- Las tablas de posiciones se actualizan manualmente con alto riesgo de errores de cálculo

**Comunicación y Transparencia:**
- Los jugadores y aficionados no tienen acceso inmediato a información actualizada
- Las notificaciones de cambios se realizan de manera informal (llamadas, mensajes)
- No existe un canal oficial para consultar estadísticas y clasificaciones

**Seguridad de la Información:**
- Los datos personales de jugadores no están protegidos adecuadamente
- No hay respaldos de información crítica
- El acceso a la información no está controlado por roles

### 💡 Solución Tecnológica Implementada

Este sistema web proporciona una solución integral que aborda cada uno de los problemas identificados mediante:

**Digitalización Completa:**
- Registro electrónico de equipos, jugadores y documentación
- Almacenamiento seguro en base de datos MySQL con respaldos automáticos
- Validación automatizada de datos de entrada
- Gestión de documentos digitales (PDFs, imágenes)

**Automatización de Procesos:**
- Generación automática de calendarios mediante algoritmos todos-contra-todos
- Cálculo automático de tablas de posiciones, estadísticas y clasificaciones
- Actualización en tiempo real de resultados y métricas
- Sistema automatizado de notificaciones

**Seguridad Robusta:**
- Autenticación mediante JSON Web Tokens (JWT)
- Encriptación de contraseñas con Bcrypt (factor de coste 12)
- Control de acceso basado en roles (RBAC)
- Protección contra ataques comunes (SQL Injection, XSS, CSRF)
- Rate limiting para prevenir ataques de fuerza bruta
- Sistema de blacklist de tokens revocados
- Auditoría completa de eventos de seguridad

**Accesibilidad y Transparencia:**
- Interfaz web accesible desde cualquier dispositivo con navegador
- Acceso público a información de partidos, estadísticas y clasificaciones
- Panel administrativo para gestión centralizada
- Dashboard personalizado para líderes de equipo

---

## 🏗️ Arquitectura del Sistema

### Patrón Arquitectónico: API REST Monolítica

El sistema implementa una **arquitectura API REST monolítica** que sigue el patrón cliente-servidor con separación clara de responsabilidades. Esta decisión arquitectónica se fundamenta en:

**Justificación de la Arquitectura Monolítica:**

1. **Simplicidad Operativa:** Para un proyecto de alcance académico y comunitario, una arquitectura monolítica reduce significativamente la complejidad operacional. No requiere orquestación de servicios distribuidos, lo que facilita el despliegue, el debugging y el mantenimiento.

2. **Consistencia de Datos:** Al utilizar una única base de datos relacional (MySQL), se garantiza la consistencia transaccional ACID. Los campeonatos deportivos requieren integridad referencial estricta entre equipos, jugadores, partidos y resultados.

3. **Performance Adecuada:** Para el volumen esperado de usuarios (comunidades barriales con cientos de usuarios concurrentes máximo), una arquitectura monolítica ofrece latencias muy bajas al evitar llamadas de red entre servicios.

4. **Desarrollo Ágil:** Permite iteraciones rápidas, refactorizaciones sencillas y un equipo de desarrollo pequeño (o individual) más eficiente.

5. **Despliegue Simplificado:** Un solo artefacto deployable reduce la superficie de error y facilita el hosting en servicios económicos.

### Arquitectura en Capas

El backend Flask está organizado en una arquitectura limpia de 4 capas:

```
┌─────────────────────────────────────────┐
│     CAPA DE PRESENTACIÓN (Routes)       │  ← Endpoints REST API
├─────────────────────────────────────────┤
│   CAPA DE LÓGICA DE NEGOCIO (Services)  │  ← Reglas de negocio
├─────────────────────────────────────────┤
│    CAPA DE ACCESO A DATOS (Models)      │  ← ORM SQLAlchemy
├─────────────────────────────────────────┤
│      CAPA DE PERSISTENCIA (MySQL)       │  ← Base de datos
└─────────────────────────────────────────┘
```

**Ventajas de esta Separación:**
- **Alta cohesión:** Cada capa tiene responsabilidades bien definidas
- **Bajo acoplamiento:** Los cambios en una capa no afectan a las demás
- **Testabilidad:** Cada capa puede probarse independientemente
- **Mantenibilidad:** Código organizado y fácil de entender
- **Escalabilidad vertical:** Se puede optimizar cada capa individualmente

### Stack Tecnológico Detallado

#### Backend (API REST)

**Framework Principal: Flask 3.0+**
- Framework web ligero y flexible de Python
- Ideal para APIs REST por su minimalismo y extensibilidad
- Excelente ecosistema de extensiones
- Documentación extensa y comunidad activa

**ORM: SQLAlchemy 2.0**
- Object-Relational Mapping para abstracción de base de datos
- Soporte completo para MySQL con relaciones complejas
- Migraciones de esquema con Flask-Migrate
- Query building seguro que previene SQL Injection

**Autenticación y Seguridad:**
- **Flask-JWT-Extended:** Gestión completa de JSON Web Tokens
  - Access tokens (15 minutos de vigencia)
  - Refresh tokens (30 días de vigencia)
  - Blacklist de tokens revocados
  - Claims personalizados para roles
  
- **Bcrypt:** Hash de contraseñas con factor de coste 12
  - Protección contra rainbow tables
  - Resistente a ataques de fuerza bruta
  - Salting automático

- **Flask-CORS:** Control de Cross-Origin Resource Sharing
  - Configuración de orígenes permitidos
  - Headers de seguridad HTTP
  
- **Flask-Limiter:** Rate limiting por IP y usuario
  - Protección contra ataques DDoS
  - Límites configurables por endpoint
  - Backend en memoria para desarrollo

**Validación y Serialización:**
- **Marshmallow:** Schemas de validación para entrada/salida
- **SQLAlchemy Validators:** Validación a nivel de modelo

**Gestión de Archivos:**
- **Werkzeug:** Utilidades seguras para upload de archivos
- Validación de extensiones permitidas (PDF, JPG, PNG)
- Límite de tamaño de archivo (16MB)
- Almacenamiento organizado por tipo

#### Base de Datos: MySQL 8.0+

**Características Aprovechadas:**
- **InnoDB Engine:** Soporte ACID, transacciones, foreign keys
- **Índices optimizados:** B-trees para búsquedas rápidas
- **Vistas materializadas:** Cálculos pre-computados (tabla de posiciones)
- **Triggers:** Automatización de lógica (auditoría)
- **JSON datatype:** Almacenamiento de datos semiestructurados
- **Full-text search:** Búsquedas eficientes en texto

**Modelo de Datos Normalizado:**
- Tercera Forma Normal (3FN)
- Integridad referencial estricta
- Constraints de validación
- Índices estratégicos para performance

#### Infraestructura y DevOps

**Control de Versiones:**
- **Git:** Sistema de control de versiones distribuido
- **Conventional Commits:** Estándar para mensajes de commit
- **.gitignore:** Exclusión de archivos sensibles

**Gestión de Dependencias:**
- **pip:** Gestor de paquetes de Python
- **requirements.txt:** Archivo de dependencias versionadas
- **Virtual Environment:** Aislamiento de dependencias

**Variables de Entorno:**
- **python-dotenv:** Carga de configuración desde .env
- **Separación de configuraciones:** Development, Production, Testing

**Logging y Monitoreo:**
- **Python logging:** Logs estructurados por nivel
- **Security logs en BD:** Auditoría persistente de eventos críticos

---

## 📦 Estructura del Proyecto

```
Campeonato/
│
├── backend/                           # Aplicación Flask (API REST)
│   │
│   ├── app/                          # Núcleo de la aplicación
│   │   │
│   │   ├── __init__.py              # Factory pattern - Creación de app Flask
│   │   │                             # Inicialización de extensiones
│   │   │                             # Registro de blueprints
│   │   │                             # Configuración de CORS
│   │   │
│   │   ├── config.py                # Configuraciones por entorno
│   │   │                             # - DevelopmentConfig
│   │   │                             # - ProductionConfig  
│   │   │                             # - TestingConfig
│   │   │                             # Configuración de JWT, BD, uploads
│   │   │
│   │   ├── extensions.py            # Instancias de extensiones Flask
│   │   │                             # - SQLAlchemy (db)
│   │   │                             # - JWTManager (jwt)
│   │   │                             # - CORS (cors)
│   │   │                             # - Bcrypt (bcrypt)
│   │   │                             # - Limiter (limiter)
│   │   │
│   │   ├── models/                  # Modelos de Base de Datos (ORM)
│   │   │   ├── __init__.py          # Importación centralizada de modelos
│   │   │   │
│   │   │   ├── usuario.py           # Modelo Usuario
│   │   │   │                         # - Roles: admin, lider, espectador
│   │   │   │                         # - Password hashing
│   │   │   │                         # - Email validation
│   │   │   │
│   │   │   ├── equipo.py            # Modelo Equipo
│   │   │   │                         # - Estados: pendiente, aprobado, rechazado
│   │   │   │                         # - Relación con Usuario (líder)
│   │   │   │                         # - Logo upload
│   │   │   │
│   │   │   ├── jugador.py           # Modelo Jugador
│   │   │   │                         # - Validación de documento único
│   │   │   │                         # - Posiciones: portero, defensa, etc
│   │   │   │                         # - Dorsal único por equipo
│   │   │   │                         # - Upload de documento PDF
│   │   │   │
│   │   │   ├── campeonato.py        # Modelo Campeonato
│   │   │   │                         # - Estados: planificacion, en_curso, finalizado
│   │   │   │                         # - Fechas de inicio/fin
│   │   │   │
│   │   │   ├── partido.py           # Modelo Partido
│   │   │   │                         # - Estados: programado, en_juego, finalizado
│   │   │   │                         # - Jornadas
│   │   │   │                         # - Goles local/visitante
│   │   │   │                         # - Check: equipo_local != equipo_visitante
│   │   │   │
│   │   │   ├── gol.py               # Modelo Gol
│   │   │   │                         # - Tipos: normal, penal, autogol, tiro_libre
│   │   │   │                         # - Minuto del gol
│   │   │   │
│   │   │   ├── tarjeta.py           # Modelo Tarjeta
│   │   │   │                         # - Tipos: amarilla, roja
│   │   │   │                         # - Motivo
│   │   │   │
│   │   │   ├── alineacion.py        # Modelo Alineación
│   │   │   │                         # - Titulares y suplentes
│   │   │   │                         # - Minutos de entrada/salida
│   │   │   │
│   │   │   ├── notificacion.py      # Modelo Notificación
│   │   │   │                         # - Tipos: info, warning, success, error
│   │   │   │                         # - Estado leída/no leída
│   │   │   │
│   │   │   ├── solicitud_equipo.py  # Modelo Solicitud de Equipo
│   │   │   │                         # - Workflow de aprobación
│   │   │   │
│   │   │   ├── refresh_token.py     # Modelo Refresh Token
│   │   │   │                         # - Tokens de actualización JWT
│   │   │   │                         # - Expiración configurable
│   │   │   │
│   │   │   ├── token_blacklist.py   # Modelo Token Blacklist
│   │   │   │                         # - Tokens revocados
│   │   │   │                         # - JTI (JWT ID)
│   │   │   │
│   │   │   ├── login_attempt.py     # Modelo Intento de Login
│   │   │   │                         # - IP, User-Agent
│   │   │   │                         # - Success/Failure
│   │   │   │
│   │   │   ├── account_lockout.py   # Modelo Bloqueo de Cuenta
│   │   │   │                         # - Bloqueos temporales
│   │   │   │                         # - Código de desbloqueo
│   │   │   │
│   │   │   └── security_log.py      # Modelo Log de Seguridad
│   │   │                             # - Eventos: login, logout, cambios
│   │   │                             # - Detalles en JSON
│   │   │
│   │   ├── routes/                  # Endpoints de la API REST
│   │   │   ├── __init__.py          # Registro de todos los blueprints
│   │   │   │
│   │   │   ├── auth_routes.py       # Autenticación
│   │   │   │                         # POST /api/auth/register
│   │   │   │                         # POST /api/auth/login
│   │   │   │                         # POST /api/auth/refresh
│   │   │   │                         # POST /api/auth/logout
│   │   │   │                         # POST /api/auth/verify-email
│   │   │   │
│   │   │   ├── equipo_routes.py     # CRUD Equipos
│   │   │   │                         # GET    /api/equipos
│   │   │   │                         # POST   /api/equipos
│   │   │   │                         # GET    /api/equipos/<id>
│   │   │   │                         # PUT    /api/equipos/<id>
│   │   │   │                         # DELETE /api/equipos/<id>
│   │   │   │                         # POST   /api/equipos/<id>/aprobar
│   │   │   │
│   │   │   ├── jugador_routes.py    # CRUD Jugadores
│   │   │   ├── campeonato_routes.py # CRUD Campeonatos
│   │   │   ├── partido_routes.py    # CRUD Partidos
│   │   │   ├── gol_routes.py        # CRUD Goles
│   │   │   ├── tarjeta_routes.py    # CRUD Tarjetas
│   │   │   ├── alineacion_routes.py # CRUD Alineaciones
│   │   │   ├── notificacion_routes.py # CRUD Notificaciones
│   │   │   └── solicitud_equipo_routes.py # Solicitudes
│   │   │
│   │   ├── middlewares/             # Middlewares personalizados
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── auth.py              # Decoradores de autenticación
│   │   │   │                         # - @jwt_required_with_blacklist
│   │   │   │                         # - @admin_required
│   │   │   │                         # - @lider_required
│   │   │   │
│   │   │   ├── rate_limit.py        # Rate limiting personalizado
│   │   │   │                         # - Límites por endpoint
│   │   │   │                         # - Límites por usuario/IP
│   │   │   │
│   │   │   └── error_handler.py     # Manejo centralizado de errores
│   │   │                             # - Errores HTTP estandarizados
│   │   │                             # - Logging de excepciones
│   │   │
│   │   ├── security/                # Módulos de seguridad
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── jwt_handler.py       # Gestión avanzada de JWT
│   │   │   │                         # - Generación de tokens
│   │   │   │                         # - Verificación de blacklist
│   │   │   │                         # - Revocación de tokens
│   │   │   │
│   │   │   ├── password.py          # Utilidades de contraseñas
│   │   │   │                         # - Hashing con bcrypt
│   │   │   │                         # - Validación de fortaleza
│   │   │   │                         # - Generación de tokens reset
│   │   │   │
│   │   │   └── validators.py        # Validadores de seguridad
│   │   │                             # - Validación de email
│   │   │                             # - Sanitización de entrada
│   │   │                             # - Validación de archivos
│   │   │
│   │   └── utils/                   # Utilidades generales
│   │       ├── __init__.py
│   │       │
│   │       ├── responses.py         # Respuestas API estandarizadas
│   │       │                         # - success_response()
│   │       │                         # - error_response()
│   │       │                         # - paginated_response()
│   │       │
│   │       ├── validators.py        # Validadores de negocio
│   │       │                         # - Validación de fechas
│   │       │                         # - Validación de dorsales
│   │       │
│   │       └── helpers.py           # Funciones auxiliares
│   │                                 # - Generación de fixtures
│   │                                 # - Cálculos de estadísticas
│   │
│   ├── uploads/                     # Archivos subidos
│   │   ├── documentos/              # PDFs de jugadores
│   │   └── logos/                   # Logos de equipos
│   │
│   ├── .env                         # Variables de entorno (NO en Git)
│   ├── .env.example                 # Template de variables
│   ├── .gitignore                   # Archivos ignorados por Git
│   ├── requirements.txt             # Dependencias Python
│   └── run.py                       # Entry point de la aplicación
│
├── database/                        # Scripts de base de datos
│   ├── campeonato.sql               # Schema completo con datos
│   ├── backup_YYYYMMDD.sql          # Respaldos periódicos
│   └── migrations/                  # Migraciones de esquema
│
├── docs/                            # Documentación del proyecto
│   ├── architecture/                # Documentación arquitectónica
│   │   ├── C4_CONTEXT.md            # Diagrama de contexto C4
│   │   ├── C4_CONTAINERS.md         # Diagrama de contenedores C4
│   │   ├── C4_COMPONENTS.md         # Diagrama de componentes C4
│   │   ├── C4_CODE.md               # Diagrama de código C4
│   │   └── ARCHITECTURE_DECISIONS.md # ADRs
│   │
│   ├── api/                         # Documentación de API
│   │   ├── API_REFERENCE.md         # Referencia completa
│   │   ├── AUTHENTICATION.md        # Flujos de autenticación
│   │   └── EXAMPLES.md              # Ejemplos de uso
│   │
│   ├── database/                    # Documentación de BD
│   │   ├── ER_DIAGRAM.md            # Diagrama entidad-relación
│   │   ├── SCHEMA.md                # Documentación de tablas
│   │   └── QUERIES.md               # Queries comunes
│   │
│   └── security/                    # Documentación de seguridad
│       ├── SECURITY_OVERVIEW.md     # Visión general
│       ├── OWASP_COMPLIANCE.md      # Cumplimiento OWASP
│       └── THREAT_MODEL.md          # Modelo de amenazas
│
└── README.md                        # Este archivo

```

---

## 🚀 Instalación y Configuración

### Prerequisitos del Sistema

Antes de comenzar con la instalación, asegúrate de tener instalados los siguientes componentes en tu sistema operativo:

**Software Requerido:**
- **Python 3.9 o superior:** Lenguaje de programación principal
- **pip:** Gestor de paquetes de Python (incluido con Python)
- **MySQL 8.0 o superior:** Sistema de gestión de base de datos
- **Git:** Sistema de control de versiones
- **virtualenv o venv:** Para crear entornos virtuales aislados

**Software Opcional (Recomendado):**
- **MySQL Workbench:** Interfaz gráfica para gestión de MySQL
- **Postman o Thunder Client:** Para probar endpoints de la API
- **Visual Studio Code:** Editor de código con soporte para Python

### Paso 1: Clonar el Repositorio

```bash
# Clonar el repositorio desde GitHub
git clone https://github.com/tu-usuario/campeonato-barrial.git

# Navegar al directorio del proyecto
cd campeonato-barrial
```

### Paso 2: Configuración del Backend

#### 2.1. Crear y Activar Entorno Virtual

Es una **buena práctica crítica** trabajar con entornos virtuales para aislar las dependencias del proyecto:

```bash
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate

# Verificar que el entorno virtual está activo
# El prompt debe mostrar (venv) al inicio
```

#### 2.2. Instalar Dependencias de Python

```bash
# Actualizar pip a la última versión
python -m pip install --upgrade pip

# Instalar todas las dependencias del proyecto
pip install -r requirements.txt

# Verificar instalación
pip list
```

**Dependencias Principales Instaladas:**
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-JWT-Extended==4.6.0
- Flask-CORS==4.0.0
- Flask-Limiter==3.5.0
- PyMySQL==1.1.0
- bcrypt==4.1.2
- python-dotenv==1.0.0
- marshmallow==3.20.2

#### 2.3. Configurar Variables de Entorno

Las variables de entorno son fundamentales para la seguridad del sistema. **NUNCA** se deben hardcodear credenciales en el código.

```bash
# Copiar el template de ejemplo
cp .env.example .env

# Editar el archivo .env con tus configuraciones
nano .env  # o usar cualquier editor de texto
```

**Contenido del archivo `.env`:**

```env
# ============================================
# CONFIGURACIÓN FLASK
# ============================================
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_muy_segura_minimo_32_caracteres_aleatorios

# ============================================
# CONFIGURACIÓN DE BASE DE DATOS MYSQL
# ============================================
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gestion_campeonato
DB_USER=root
DB_PASSWORD=tu_password_mysql_seguro

# URL completa de conexión (alternativa)
DATABASE_URL=mysql+pymysql://root:tu_password@localhost/gestion_campeonato

# ============================================
# CONFIGURACIÓN JWT (JSON WEB TOKENS)
# ============================================
JWT_SECRET_KEY=tu_jwt_secret_key_diferente_muy_segura_minimo_32_chars
JWT_ACCESS_TOKEN_EXPIRES=900       # 15 minutos (900 segundos)
JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 días (2592000 segundos)

# ============================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================
BCRYPT_LOG_ROUNDS=12               # Factor de coste para hashing
MAX_LOGIN_ATTEMPTS=5               # Intentos antes de bloqueo
LOCKOUT_DURATION=900               # 15 minutos de bloqueo (segundos)
RATE_LIMIT_PER_MINUTE=60           # Peticiones por minuto

# ============================================
# CONFIGURACIÓN CORS
# ============================================
CORS_ORIGINS=http://localhost:4200,http://localhost:3000
CORS_ALLOW_CREDENTIALS=true

# ============================================
# CONFIGURACIÓN DE UPLOADS
# ============================================
MAX_CONTENT_LENGTH=16777216        # 16MB en bytes
UPLOAD_FOLDER=uploads/
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png
ALLOWED_LOGO_EXTENSIONS=jpg,jpeg,png
MAX_LOGO_SIZE=2097152              # 2MB en bytes

# ============================================
# CONFIGURACIÓN DE EMAIL (futuro)
# ============================================
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_password_app_gmail

# ============================================
# CONFIGURACIÓN DE LOGGING
# ============================================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

**Notas Importantes de Seguridad:**
- Genera claves secretas aleatorias usando: `python -c "import secrets; print(secrets.token_hex(32))"`
- **NUNCA** compartas tu archivo `.env` públicamente
- En producción, usa variables de entorno del sistema operativo o servicios secretos

### Paso 3: Configuración de la Base de Datos MySQL

#### 3.1. Crear la Base de Datos

```bash
# Conectar a MySQL como root
mysql -u root -p

# Se te pedirá tu contraseña de MySQL
```

**Dentro del prompt de MySQL:**

```sql
-- Crear la base de datos
CREATE DATABASE gestion_campeonato CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar que se creó correctamente
SHOW DATABASES;

-- Salir del prompt
EXIT;
```

#### 3.2. Importar el Schema Completo

```bash
# Importar el archivo SQL con todas las tablas, vistas y datos iniciales
mysql -u root -p gestion_campeonato < database/campeonato.sql

# Verificar que se importó correctamente
mysql -u root -p gestion_campeonato -e "SHOW TABLES;"
```

**Tablas Creadas:**
- 17 tablas principales de negocio
- 6 tablas de seguridad y auditoría
- 2 vistas optimizadas (tabla_posiciones, goleadores)
- Índices estratégicos para performance
- Foreign keys con integridad referencial

#### 3.3. Verificar la Configuración

```bash
# Conectar a la base de datos
mysql -u root -p gestion_campeonato

# Verificar estructura de una tabla importante
DESCRIBE usuarios;

# Verificar que existen las vistas
SHOW FULL TABLES WHERE Table_type = 'VIEW';

# Salir
EXIT;
```

### Paso 4: Iniciar el Servidor Backend

```bash
# Asegurarte de estar en la carpeta backend con el entorno virtual activo
cd backend
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate      # Windows

# Iniciar el servidor Flask en modo desarrollo
python run.py
```

**Salida Esperada:**

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

El servidor backend estará disponible en: **http://localhost:5000**

#### 4.1. Verificar que la API está funcionando

Abre tu navegador o usa curl/Postman para verificar:

```bash
# Health check endpoint
curl http://localhost:5000/api/health

# Respuesta esperada:
{
  "status": "ok",
  "message": "API funcionando correctamente"
}
```

---

## 👥 Roles de Usuario y Responsabilidades

El sistema implementa un modelo de **Control de Acceso Basado en Roles (RBAC - Role-Based Access Control)** con tres roles claramente definidos. Cada rol tiene permisos específicos que determinan qué acciones pueden realizar y qué información pueden acceder.

### 🔐 Administrador (admin)

El rol de **Administrador** es el más privilegiado del sistema y tiene responsabilidad completa sobre la gestión del campeonato. Este rol está diseñado para organizadores del torneo que necesitan control total sobre todos los aspectos del evento deportivo.

**Responsabilidades y Capacidades:**

**Gestión de Campeonatos:**
- Crear nuevos campeonatos con nombre, descripción, fechas de inicio y fin
- Modificar información de campeonatos existentes (fechas, descripción, estado)
- Cambiar el estado del campeonato (planificación → en_curso → finalizado)
- Eliminar campeonatos si es necesario
- Visualizar historial completo de todos los campeonatos

**Gestión de Equipos:**
- Visualizar todas las solicitudes de registro de equipos
- Aprobar equipos que cumplan con los requisitos del torneo
- Rechazar equipos con observaciones explicativas
- Modificar información de equipos aprobados si hay errores
- Eliminar equipos del campeonato en casos excepcionales
- Revisar documentación de jugadores asociados a cada equipo

**Gestión de Partidos:**
- Crear el calendario completo del campeonato (fixture)
- Generar automáticamente partidos con algoritmo todos-contra-todos
- Asignar fechas, horarios y lugares a cada partido
- Modificar programación de partidos (reprogramaciones)
- Registrar resultados finales (goles local y visitante)
- Cambiar el estado de partidos (programado → en_juego → finalizado)
- Cancelar partidos con observaciones justificativas

**Registro de Eventos del Partido:**
- Registrar goles de cada jugador con minuto y tipo (normal, penal, autogol, tiro libre)
- Registrar tarjetas amarillas y rojas con motivo
- Gestionar alineaciones de ambos equipos (titulares y suplentes)
- Registrar sustituciones con minutos de entrada/salida

**Gestión de Usuarios:**
- Crear usuarios administradores adicionales
- Modificar roles de usuarios existentes
- Bloquear o desbloquear cuentas de usuario
- Visualizar logs de seguridad y actividad de usuarios
- Revisar intentos de login fallidos

**Sistema de Notificaciones:**
- Enviar notificaciones masivas a todos los usuarios
- Enviar notificaciones específicas a líderes de equipos
- Crear notificaciones personalizadas (informativas, advertencias, errores)
- Programar notificaciones para fechas específicas

**Acceso a Información:**
- Visualizar todas las tablas de posiciones actualizadas en tiempo real
- Acceder a estadísticas completas de jugadores (goleadores, tarjetas)
- Exportar reportes y datos del campeonato
- Visualizar auditoría completa del sistema

**Caso de Uso Típico:**
Un organizador de un torneo barrial inicia sesión como administrador, crea un nuevo campeonato "Copa Verano 2025", revisa las 12 solicitudes de equipos recibidas, aprueba 10 equipos que cumplieron con enviar documentación completa, genera automáticamente el fixture de partidos todos-contra-todos (45 partidos), asigna fechas y horarios los sábados y domingos durante 6 semanas, y envía notificaciones automáticas a todos los líderes con el calendario completo.

### ⚽ Líder de Equipo (lider)

El rol de **Líder de Equipo** representa al capitán o representante oficial de un equipo participante. Este rol tiene permisos para gestionar completamente su propio equipo pero no puede interferir con otros equipos ni con la administración del campeonato.

**Responsabilidades y Capacidades:**

**Registro del Equipo:**
- Crear una solicitud de registro de equipo con nombre único
- Subir el logo del equipo (formato JPG/PNG, máximo 2MB)
- Proporcionar información de contacto del equipo
- Ver el estado de la solicitud (pendiente, aprobada, rechazada)
- Recibir notificaciones sobre el estado de aprobación
- Si es rechazado, corregir observaciones y re-solicitar aprobación

**Gestión de Jugadores:**
- Registrar jugadores de su equipo (nombre completo, documento de identidad)
- Asignar número de dorsal único por jugador (validación: no repetidos en el equipo)
- Definir la posición de cada jugador (portero, defensa, mediocampista, delantero)
- Subir documento de identidad de cada jugador (PDF, máximo 5MB)
- Registrar fecha de nacimiento para validar categorías (si aplica)
- Modificar información de jugadores de su equipo
- Dar de baja a jugadores (marcar como inactivo, no eliminar por trazabilidad)
- Validar que cada jugador cumpla con requisitos del torneo

**Gestión de Alineaciones:**
- Definir la alineación titular para cada partido de su equipo
- Seleccionar jugadores suplentes disponibles
- Modificar alineaciones antes del inicio del partido (deadline configurable)
- Visualizar historial de alineaciones en partidos anteriores

**Visualización de Información:**
- Ver el calendario completo de partidos de su equipo
- Consultar resultados de partidos ya jugados
- Ver estadísticas de sus jugadores (goles, tarjetas, minutos jugados)
- Consultar la posición de su equipo en la tabla general
- Ver historial de partidos (ganados, empatados, perdidos)

**Comunicación:**
- Recibir notificaciones sobre aprobación de equipo
- Recibir recordatorios de partidos próximos (24-48 horas antes)
- Recibir notificaciones de cambios en la programación
- Recibir comunicados oficiales del administrador

**Restricciones Importantes:**
- No puede ver información interna de otros equipos (documentos, datos de contacto)
- No puede modificar resultados de partidos
- No puede registrar eventos del partido (goles, tarjetas)
- No puede aprobar o rechazar su propia solicitud
- No puede eliminar su equipo una vez aprobado (debe solicitar al admin)

**Caso de Uso Típico:**
Juan es el capitán del equipo "Los Tigres". Inicia sesión, crea el registro de su equipo subiendo el logo, luego registra 15 jugadores proporcionando el documento de identidad de cada uno en PDF. Asigna dorsales del 1 al 15 y define posiciones. Una vez completa toda la información, envía la solicitud de aprobación. Al día siguiente recibe una notificación de que su equipo fue aprobado. Ahora puede ver el calendario: su primer partido es el sábado a las 10:00 AM contra "Los Leones". Define su alineación titular con su mejor formación 4-4-2 y deja 5 suplentes en banca.

### 👁️ Espectador (espectador)

El rol de **Espectador** proporciona acceso público de solo lectura a toda la información del campeonato. Este rol está diseñado para aficionados, familiares de jugadores, prensa local y cualquier persona interesada en seguir el desarrollo del torneo sin necesidad de participar directamente en su gestión.

**Responsabilidades y Capacidades:**

**Visualización de Partidos:**
- Ver calendario completo de partidos programados
- Filtrar partidos por fecha, jornada o equipo
- Ver detalles de cada partido (equipos, lugar, hora, jornada)
- Consultar resultados finales de partidos ya jugados
- Ver goles anotados con detalles (jugador, minuto, tipo)
- Ver tarjetas mostradas en cada partido

**Tablas y Clasificaciones:**
- Consultar tabla de posiciones actualizada en tiempo real
- Ver estadísticas detalladas por equipo:
  - Partidos jugados, ganados, empatados, perdidos
  - Goles a favor y en contra
  - Diferencia de goles
  - Puntos acumulados
- Filtrar tabla por campeonato específico (si hay múltiples torneos)

**Estadísticas de Jugadores:**
- Ver tabla de goleadores del campeonato
- Filtrar goleadores por equipo
- Ver detalles de goles (penales, tiros libres, goles normales)
- Consultar jugadores con más tarjetas (amarillas, rojas)
- Ver estadísticas individuales de jugadores

**Información de Equipos:**
- Ver listado de todos los equipos participantes
- Consultar plantilla de cada equipo (jugadores registrados)
- Ver logo y nombre oficial de equipos
- Consultar historial de partidos por equipo

**Información del Campeonato:**
- Ver información general del torneo (nombre, fechas, descripción)
- Consultar formato del campeonato (todos contra todos, eliminación, etc.)
- Ver estado actual del campeonato (en curso, finalizado)

**Restricciones:**
- **No puede modificar ninguna información** (solo lectura)
- No puede registrarse como líder de equipo desde este rol
- No puede acceder a documentos de identidad de jugadores
- No puede ver información de contacto privada
- No tiene acceso a panel administrativo

**Caso de Uso Típico:**
María, madre de un jugador del equipo "Los Águilas", entra al sitio web sin necesidad de crear cuenta. Navega al calendario de partidos, encuentra que el próximo partido de su hijo es el domingo a las 15:00 en la cancha municipal. Revisa la tabla de posiciones y ve que "Los Águilas" está en tercer lugar con 18 puntos. Entra a la sección de goleadores y ve que su hijo tiene 5 goles y está en el top 10 de goleadores. Comparte el enlace de la tabla con familiares por WhatsApp para que también puedan seguir el torneo.

---

## 🔐 Arquitectura de Seguridad

La seguridad es un pilar fundamental del sistema, implementando múltiples capas de protección para garantizar la confidencialidad, integridad y disponibilidad de la información. El diseño de seguridad sigue las mejores prácticas de la industria y cumple con los estándares de OWASP Top 10.

### Principios de Seguridad Aplicados

**Defensa en Profundidad (Defense in Depth):**
El sistema no depende de una única medida de seguridad, sino que implementa múltiples capas independientes. Si una capa es comprometida, las otras siguen protegiendo el sistema.

**Menor Privilegio (Least Privilege):**
Cada usuario y componente del sistema tiene únicamente los permisos mínimos necesarios para realizar su función. Los espectadores solo leen, los líderes solo gestionan su equipo, los administradores tienen control total.

**Fallo Seguro (Fail Secure):**
Cuando ocurre un error o condición inesperada, el sistema falla de manera segura: deniega acceso por defecto, registra el evento, y no expone información sensible.

**Separación de Responsabilidades:**
Las funciones críticas requieren múltiples actores. Por ejemplo, un líder registra equipos pero solo un administrador puede aprobarlos.

### Autenticación y Gestión de Sesiones

#### JSON Web Tokens (JWT)

El sistema utiliza **JWT (JSON Web Tokens)** como mecanismo principal de autenticación stateless. Esta tecnología permite verificar la identidad del usuario sin mantener sesiones en el servidor, lo que mejora la escalabilidad.

**Arquitectura de Tokens Dual:**

1. **Access Token (Token de Acceso):**
   - Duración: 15 minutos
   - Propósito: Autenticar cada petición a la API
   - Contenido (Claims):
     ```json
     {
       "sub": "user_id_123",           // Identificador único del usuario
       "email": "usuario@email.com",   // Email del usuario
       "rol": "lider",                 // Rol para autorización
       "iat": 1735678900,              // Issued at (timestamp)
       "exp": 1735679800,              // Expiration (timestamp)
       "jti": "unique-jwt-id-abc123"   // JWT ID para blacklist
     }
     ```
   - Almacenamiento cliente: localStorage o memoria
   - Renovación: Mediante refresh token

2. **Refresh Token (Token de Actualización):**
   - Duración: 30 días
   - Propósito: Obtener nuevos access tokens sin re-autenticarse
   - Almacenamiento: Base de datos (tabla `refresh_tokens`)
   - Características:
     - Asociado a IP y User-Agent para detectar robo
     - Puede ser revocado individualmente
     - Rotación automática al usar (se genera uno nuevo)

**Flujo de Autenticación:**

```
1. Usuario envía credenciales (email + password)
   POST /api/auth/login

2. Sistema valida credenciales:
   - Verifica que el email exista
   - Compara password con hash bcrypt almacenado
   - Verifica que la cuenta no esté bloqueada
   - Verifica que el email esté verificado

3. Si es válido, genera ambos tokens:
   - Access token (JWT firmado con SECRET_KEY)
   - Refresh token (UUID almacenado en BD)

4. Retorna tokens al cliente:
   {
     "access_token": "eyJhbGc...",
     "refresh_token": "8f7d6c5b...",
     "token_type": "Bearer",
     "expires_in": 900
   }

5. Cliente incluye access token en cada petición:
   Authorization: Bearer eyJhbGc...

6. Cuando el access token expira (15 min):
   - Cliente detecta error 401 Unauthorized
   - Envía refresh token a /api/auth/refresh
   - Obtiene nuevo access token
   - Continúa operando sin interrumpir al usuario

7. Si el refresh token también expira (30 días):
   - Usuario debe iniciar sesión nuevamente
```

**Ventajas de este Diseño:**
- **Seguridad:** Access tokens de corta duración minimizan ventana de ataque
- **Experiencia:** Refresh tokens permiten sesiones largas sin re-autenticación constante
- **Revocación:** Tokens pueden invalidarse individualmente (logout, cambio de password)
- **Auditoría:** Cada token está trazado a IP y dispositivo

#### Blacklist de Tokens (Token Revocation)

Para permitir el cierre de sesión (logout) y la revocación de tokens comprometidos, el sistema implementa una **blacklist de tokens** en base de datos.

**Tabla: `token_blacklist`**
```sql
CREATE TABLE token_blacklist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jti VARCHAR(255) UNIQUE NOT NULL,      -- JWT ID único
    token_type VARCHAR(20) NOT NULL,       -- 'access' o 'refresh'
    user_id INT NOT NULL,                  -- Usuario propietario
    revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,         -- Cuando expira naturalmente
    reason VARCHAR(100),                   -- Motivo de revocación
    INDEX idx_jti (jti),
    INDEX idx_expires (expires_at)
);
```

**Proceso de Validación:**
```python
def verificar_token(jwt_token):
    # 1. Verificar firma y expiración del JWT
    payload = jwt.decode(jwt_token, SECRET_KEY)
    
    # 2. Extraer JTI (JWT ID)
    jti = payload['jti']
    
    # 3. Verificar que NO esté en blacklist
    if TokenBlacklist.query.filter_by(jti=jti).first():
        raise TokenRevocadoError("Token ha sido revocado")
    
    # 4. Si pasa todas las validaciones, es válido
    return payload
```

**Casos de Revocación:**
- **Logout manual:** Usuario cierra sesión explícitamente
- **Cambio de contraseña:** Invalida todas las sesiones activas
- **Bloqueo de cuenta:** Admin o sistema bloquea cuenta
- **Actividad sospechosa:** Sistema detecta comportamiento anómalo
- **Robo de token:** Usuario reporta compromiso de cuenta

**Limpieza Automática:**
Los tokens en blacklist que ya expiraron naturalmente pueden eliminarse periódicamente mediante un job programado:

```sql
-- Job diario de limpieza
DELETE FROM token_blacklist 
WHERE expires_at < NOW() - INTERVAL 7 DAY;
```

### Cifrado y Hashing de Contraseñas

#### Bcrypt: Función de Hash Segura

El sistema utiliza **Bcrypt** para el hash de contraseñas, considerado el estándar de oro para este propósito debido a sus características de seguridad.

**Características de Bcrypt:**

1. **Slow Hashing (Hash Lento):**
   - Diseñado intencionalmente para ser computacionalmente costoso
   - Factor de coste configurable: `BCRYPT_LOG_ROUNDS = 12`
   - Con factor 12: ~0.3 segundos por hash en hardware moderno
   - Protege contra ataques de fuerza bruta masivos

2. **Salt Automático:**
   - Cada contraseña tiene un salt único aleatorio de 128 bits
   - El salt se almacena en el mismo hash (no requiere campo separado)
   - Previene ataques con rainbow tables pre-calculadas
   - Dos usuarios con la misma contraseña tendrán hashes diferentes

3. **Resistencia a GPU/ASIC:**
   - Algoritmo memory-hard que dificulta paralelización masiva
   - Costoso de implementar en hardware especializado

**Implementación en el Sistema:**

```python
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Al registrar usuario
def registrar_usuario(email, password_plano):
    # Generar hash (incluye salt automático)
    password_hash = bcrypt.generate_password_hash(
        password_plano, 
        rounds=12
    ).decode('utf-8')
    
    # Almacenar en BD (solo el hash, NUNCA la contraseña plana)
    usuario = Usuario(
        email=email,
        contrasena=password_hash  # Ejemplo: $2b$12$abc...xyz
    )
    db.session.add(usuario)
    db.session.commit()

# Al iniciar sesión
def verificar_login(email, password_plano):
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        return False
    
    # Comparar password plano con hash almacenado
    # bcrypt se encarga de extraer el salt y replicar el proceso
    return bcrypt.check_password_hash(
        usuario.contrasena, 
        password_plano
    )
```

**Formato del Hash Bcrypt:**
```
$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW
│ │  │  │                        └─ Hash (184 bits)
│ │  │  └─ Salt (128 bits en base64)
│ │  └─ Rounds (2^12 = 4096 iteraciones)
│ └─ Versión del algoritmo
└─ Identificador bcrypt
```
