FROM python

RUN mkdir /root/.torrench/
COPY ./** /root/.torrench/
RUN pip install -r /root/.torrench/data/requirements.txt \
chmod u+x /root/.torrench/data/torrench.py \
&& mkdir /root/.torrench/bin \
&& ln -s /root/.torrench/bin/torrench /root/.torrench/data/torrench.py \
&& echo 'export PATH=/root/.torrench/bin/:$PATH' >> /root/.bashrc

WORKDIR /root/

CMD ['echo', 'Torrench']