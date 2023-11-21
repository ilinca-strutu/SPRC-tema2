FROM python:3.8
COPY /api/requirements.txt /tmp
RUN pip install -U setuptools
RUN pip install -r /tmp/requirements.txt
COPY /api/src /app 
WORKDIR /app
EXPOSE 5000
CMD ["python3", "api.py"]