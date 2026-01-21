# Imagem base com Python
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos da aplicação
COPY app.py cpu_stress.py ./  
COPY templates ./templates

# Instala dependências
RUN pip install flask psutil requests

# Expõe a porta 8080
EXPOSE 80

# Comando para iniciar o Flask
CMD ["python", "app.py"]