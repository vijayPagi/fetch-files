FROM python:slim

MAINTAINER VIJAY

env pythonunbuffered 1

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "FetchData.py", "https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt"]