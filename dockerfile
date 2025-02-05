FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Probably don't need to Copy annd set Env in the dockerfile because we are pushing and executing using authenticated service account

# COPY ${PROJECT_ID}-credentials.json /app/${PROJECT_ID}-credentials.json
# ENV GOOGLE_APPLICATION_CREDENTIALS /app/${PROJECT_ID}-credentials.json

CMD ["python",  "src/main.py"]