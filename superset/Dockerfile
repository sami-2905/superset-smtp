# Use the official Apache Superset image
FROM apache/superset:latest

# Install Redis, PostgreSQL client, and Python (if not already included) and other dependencies
USER root
RUN apt-get update && \
    apt-get install -y python3 postgresql-client wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Copy the Superset configuration
COPY ./superset_config.py /app/pythonpath/superset_config.py

# Generate a SECRET_KEY and append it to the configuration file before running upgrade
RUN echo "SECRET_KEY = '$(python3 -c "import os; print(os.urandom(24).hex())")'" >> /app/pythonpath/superset_config.py

# Install Python packages for Google Sheets integration
RUN pip install gspread oauth2client

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
COPY start.sh /start.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /start.sh

# Install headless Chrome browser
RUN apt-get update && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb && \
    rm -f google-chrome-stable_current_amd64.deb

RUN export CHROMEDRIVER_VERSION=$(curl --silent https://chromedriver.storage.googleapis.com/LATEST_RELEASE_102) && \
    wget -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin && \
    chmod 755 /usr/bin/chromedriver && \
    rm -f chromedriver_linux64.zip

RUN sh -c "echo 'LC_ALL=en_US.UTF-8\nLANG=en_US.UTF-8' >> /etc/environment"

# Set the web driver type to Chrome
ENV WEBDRIVER_TYPE=chrome

# Switch back to superset user and initialize Superset
USER superset

# Expose the port Superset is running on
EXPOSE 8088

# Start Superset using the custom start script
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]

