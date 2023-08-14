FROM docker.iranrepo.ir/python:3.11.4

WORKDIR /app

COPY . /app/

RUN pip install pipenv && pipenv install --system

EXPOSE 8000:8000

WORKDIR /app/src

# Install cron
RUN apt-get update && apt-get -y install cron

# Copy file to the cron.d directory
COPY crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

# Apply cron job
RUN crontab /etc/cron.d/crontab

RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log