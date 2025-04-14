# Use the official Python image as the base image
FROM python:3.10

# Installeer de benodigde systeemafhankelijkheden voor ODBC en wget
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    wget \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Download de MySQL ODBC 9.2 driver via een directe URL en installeer
RUN wget https://dev.mysql.com/get/Downloads/Connector-ODBC/9.2/mysql-connector-odbc_9.2.0-1debian12_amd64.deb \
    && dpkg -i mysql-connector-odbc_9.2.0-1debian12_amd64.deb \
    && apt-get install -f -y \
    && rm -rf mysql-connector-odbc_9.2.0-1debian12_amd64.deb

# Stel de werkmap in voor de container
WORKDIR /app

# Kopieer de huidige map (waar de Dockerfile is) naar de container
COPY . /app

# Installeer de Python-afhankelijkheden
RUN pip install --no-cache-dir -r requirements.txt

# Exposeer de poort waarop de Flask app draait
EXPOSE 3000

# Commando om de app te draaien
CMD ["python", "form.py"]


