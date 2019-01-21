FROM python:3.7

COPY requirements.txt /root
RUN pip install -r /root/requirements.txt
RUN useradd -m user
USER user
WORKDIR /home/user

