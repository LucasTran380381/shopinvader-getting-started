FROM python:3.11

USER root
# Install system dependencies
RUN apt-get update && apt-get install -y postgresql-client python3-pip libldap2-dev libpq-dev libsasl2-dev \
    && rm -rf /var/lib/apt/lists/*
# Install pip and upgrade it
RUN pip3 install --upgrade pip
# Install Odoo dependencies
RUN pip3 install -r https://raw.githubusercontent.com/odoo/odoo/16.0/requirements.txt
# Install Odoo (adjust the version as needed)
RUN git clone --depth 1 -b 16.0 https://github.com/odoo/odoo.git /odoo-src
RUN pip3 install -e /odoo-src

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/

# Create Odoo user and group
RUN groupadd -r odoo && useradd -r -g odoo -m -d /opt/odoo odoo
# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN chown odoo /etc/odoo/odoo.conf \
    && mkdir -p /var/lib/odoo \
    && chown odoo /var/lib/odoo \
    && mkdir -p /mnt/extra-addons \
    && chown -R odoo /mnt/extra-addons
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC=/etc/odoo/odoo.conf

COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]