FROM python:3.11-slim

WORKDIR /sql_bp_auth

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD sh -c "pwd && python app.py"

