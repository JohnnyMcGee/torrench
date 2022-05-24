FROM python

# Install & Configure Torrench
RUN mkdir /root/.torrench/
COPY . /root/.torrench/
WORKDIR /root/.torrench/
RUN pip install -r data/requirements.txt
RUN chmod 755 /root/.torrench/data/torrench.py \
&& echo 'alias torrench="python3 ~/.torrench/data/torrench.py"' >> /root/.bashrc

# Install & Configure rtorrent
RUN apt-get update && apt-get install -y rtorrent
WORKDIR /root/
RUN mkdir rtorrent_Downloads rtorrent_Watch rtorrent_Session
COPY rtorrent.rc /root/.rtorrent.rc

WORKDIR /root/rtorrent_Downloads
VOLUME [/root/rtorrent_Downloads]

CMD ["tail", "-f", "/dev/null"]