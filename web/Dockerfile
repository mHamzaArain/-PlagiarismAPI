FROM python:3.6
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN pip3 install ./en_core_web_sm-2.3.1.tar.gz
CMD [ "python3", "app.py" ]
