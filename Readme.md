# 🚀 siembro-user-notes-service

Microservicio en **Python/FastAPI** que permite a usuarios internos crear y consultar notas asociadas a su usuario, autenticados mediante **Auth0**.  
Diseñado para integrarse en una arquitectura moderna de microservicios (GCP, Kubernetes, Auth0, Postgres).

---

## 📦 Tecnologías utilizadas

- Python 3.11  
- FastAPI  
- Uvicorn  
- SQLAlchemy 2.x  
- PostgreSQL 16  
- Auth0 (JWT + JWKS RS256)  
- Docker + docker-compose  
- Alembic (migraciones) (Opcional No agregado) 
- Pytest (suite completa de tests)  

---

## ⚙️ Configuración de entorno

Crear un archivo `.env` en la raíz del proyecto con:

```env
DATABASE_URL=postgresql+psycopg://siembro:siembro@db:5432/siembro_user_notes

AUTH0_DOMAIN=dev-xxxxx.us.auth0.com
AUTH0_AUDIENCE=https://siembro-user-notes-api
AUTH0_ALGORITHMS=RS256

DEBUG=true
AUTH0_INSECURE_SKIP_TLS_VERIFY=false
```

## ▶️ Ejecutar en desarrollo (sin Docker)
1. Crear entorno virtual
```shell

python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias
```shell
  pip install -r requirements.txt
```

3. Exportar variables o configurar .env
```shell
  export DATABASE_URL=postgresql+psycopg://siembro:siembro@localhost:5432/siembro_user_notes
```

4. Inicializar la base de datos
```shell
  python -m app.db.init_db
```

5. Levantar el servidor
```shell
  uvicorn app.main:app --reload
```

La API queda disponible en:


http://localhost:8000/docs

http://localhost:8000/health



## 🐳 Ejecutar con Docker / docker-compose
1. Crear .env
(usar el ejemplo de arriba)
2. Levantar los servicios
```shell
  docker compose up --build
```

Esto levanta:


API en http://localhost:8000


PostgreSQL en el puerto 5432



## 🔐 Autenticación con Auth0
Este servicio solo acepta JWTs válidos de Auth0 (RS256).
Flujo de validación


El cliente obtiene un token desde Auth0:
POST https://{tenant}.auth0.com/oauth/token



Llama a la API con:
Authorization: Bearer <access_token>



El servicio:


Descarga el JWKS desde
https://{AUTH0_DOMAIN}/.well-known/jwks.json


Valida firma, issuer, audiencia.


Extrae claims y asegura que exista un usuario correspondiente.


## 🧪 Testing
El proyecto incluye una suite completa en tests/:


DB SQLite en memoria


Mock de autenticación Auth0


Tests para:


/health


/me


/notes (listar y crear)



## ▶️ Correr tests localmente

Con el entorno virtual activado:
```shell
  pytest -q
```

## 🐳 Correr tests dentro de Docker

Ejecutar toda la suite:
```shell
  docker compose run --rm api pytest -q
```



## 🧭 Curl rápido
curl http://localhost:8000/health



## ⚙️ Decisiones técnicas

Framework elegido – FastAPI
Elegí FastAPI porque es rápido, simple y no te hace pelearte con nada. Te deja armar un microservicio limpio, con tipado fuerte, validación automática y la API queda prolija sin overengineering. Perfecto para microservicios chicos pero sólidos.

Validación de JWT / Auth0
La integración con Auth0 la armé siguiendo el flujo estándar: descargo el JWKS del tenant, valido la firma RS256, verifico iss, aud y después levanto los claims del token. De ahí saco el sub, y con eso creo o actualizo el usuario en la base. Todo encapsulado en una dependencia de FastAPI para que quede prolijo y reusable.

Estructura de la base de datos
Modelo simple y directo: users y notes. El usuario está indexado por auth0_sub para lookup rápido. Metadata del usuario la guardo como JSON para poder extender sin romper el esquema. Las notas tienen FK al usuario y timestamps automáticos.