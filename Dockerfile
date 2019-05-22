FROM python:3.7-stretch

RUN mkdir /src
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
CMD ["python","__main__.py","-d"]

# FROM base as builder
# FROM base
# COPY --from=builder /install /usr/local
# COPY src /app
# WORKDIR /app
# CMD ["python "]