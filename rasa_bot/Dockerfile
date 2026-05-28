FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias usando uv
RUN uv sync --frozen --no-dev

# Copiar los archivos de Rasa
COPY . .

# Exponer el puerto de Rasa
EXPOSE 5005

# Comando para ejecutar Rasa habilitando la API
CMD ["uv", "run", "rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
