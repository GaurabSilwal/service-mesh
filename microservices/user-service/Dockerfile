FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Build-time argument for Python file
ARG PYTHON_APP=app.py

# Copy the Python file based on the argument
COPY ${PYTHON_APP} /app/app.py

EXPOSE 5000

# Run the file (always as app.py inside container)
CMD ["python", "app.py"]
