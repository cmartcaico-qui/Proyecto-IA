# Plantilla de repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

Esta es la estructura base que vas a usar como punto de partida para tu proyecto en este programa. Es la misma estructura que vas a ir ampliando bloque a bloque, hasta llegar a la aplicación completa que entregas en el Gate 3.

## Cómo empezar

Estos pasos se completan de forma progresiva a lo largo de la Unidad U1.2, no todos el mismo día:

1. Descarga este archivo comprimido (adjunto en la plataforma) y descomprímelo en tu computador. Inicializa el control de versiones sobre esa carpeta y registra tu primer commit con esta estructura base, tal como llegó, antes de modificar nada.
2. Crea tu entorno virtual de Python (por ejemplo, con `venv`) y actívalo.
3. Instala las dependencias que necesites y regístralas en `requirements.txt` (al inicio puede estar vacío o con muy pocas).
4. Copia `.env.example` a un archivo nuevo llamado `.env`, y completa ahí tus credenciales reales (llaves de API, tokens). El archivo `.env` nunca se sube al repositorio: ya está excluido en `.gitignore`.

## Estructura de carpetas

- `src/` : todo el código fuente de tu proyecto va aquí.
- `docs/` : documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas).
- `tests/` : pruebas de tu código (las vas a usar más adelante en el programa, cuando el proyecto lo requiera).
- `requirements.txt` : dependencias de Python de tu proyecto, para que cualquier otra persona pueda reconstruir tu entorno con un solo comando.
- `.env.example` : plantilla de las variables de entorno que tu proyecto necesita, sin valores reales. Tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore` : le dice a Git qué archivos y carpetas ignorar (entre ellos, tu entorno virtual y tu archivo `.env`).

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.


# ProjectPulse — Miniaplicación de seguimiento de proyectos con IA Generativa
ProjectPulse es una miniaplicación desarrollada durante la Especialización en Desarrollo con IA Generativa. Su objetivo es analizar información de seguimiento de proyectos e identificar compromisos, alertas, pendientes y estado general utilizando la API de Gemini.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/cmartcaico-qui/Proyecto-IA.git
cd Proyecto-IA
```

### 2. Crear y activar un entorno virtual

En Windows con Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar la API key de Gemini

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Luego abre `.env` y reemplaza:

```text
GEMINI_API_KEY=tu_llave_aqui
```

por tu API key real de Gemini.

La clave real no debe subirse al repositorio.

### 5. Ejecutar ProjectPulse

Desde la raíz del proyecto:

```bash
cd src
python consumir_gemini.py
```

### 6. Validar la consistencia del banco de prompts

Desde la carpeta `src`:

```bash
python consistencia.py
```

Los resultados se guardan en:

```text
src/prompts/registro_resultados.json
```

## Registro del ensayo de instalación limpia

Durante la preparación del Gate 1 se detectó que `python-dotenv` estaba instalado localmente, pero no estaba incluido inicialmente en `requirements.txt`.

También se detectó que `.env.example` utilizaba `API_KEY`, mientras que el código esperaba `GEMINI_API_KEY`.

Ambos puntos fueron corregidos antes de repetir el ensayo de instalación limpia.

- Fecha: 23/10/2026.
- Se clonó el repositorio en una carpeta nueva.
- Se creó un entorno virtual desde cero.
- Se instalaron las dependencias únicamente desde `requirements.txt`.
- Se configuró `.env` a partir de `.env.example`.
- Se ejecutó `src/consumir_gemini.py` correctamente contra la API real de Gemini.
- Se ejecutó `src/consistencia.py` correctamente, obteniendo 3/3 respuestas válidas en los tres prompts del banco.
- `git status` confirmó que `.env` no está siendo versionado.
- Durante la preparación se corrigió la ausencia de `python-dotenv` en `requirements.txt` y se ajustó `.env.example` para usar `GEMINI_API_KEY`.

Resultado final: el proyecto puede instalarse y ejecutarse desde cero siguiendo únicamente las instrucciones del repositorio.