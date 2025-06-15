FROM python:3.11-slim

WORKDIR /sql_inj_classic

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV VULNERABLE=1

CMD sh -c "pwd && python app.py"

