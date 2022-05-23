FROM python

RUN mkdir /root/.torrench/
COPY . /root/.torrench/
RUN python -m pip install --upgrade pip
WORKDIR /root/.torrench/
RUN python -m pip install -r /root/.torrench/data/requirements.txt
RUN chmod 755 /root/.torrench/data/torrench.py \
&& mkdir /root/.torrench/bin \
&& ln -s /root/.torrench/data/torrench.py /root/.torrench/bin/torrench  \
&& echo 'export PATH=/root/.torrench/bin/:$PATH' >> /root/.bashrc

WORKDIR /root/

CMD ["tail", "-f", "/dev/null"]