FROM ubuntu:20.04

# Evitar preguntas interactivas
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python y herramientas básicas
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Agregar repositorio de Microsoft para Ubuntu 20.04
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instalar Driver ODBC y herramientas
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Instalar librerías de Python
RUN pip3 install flask pyodbc

# Copiar archivos
COPY . /app
WORKDIR /app

EXPOSE 5000
# Usar python3 explícitamente
CMD ["python3", "app.py"]
