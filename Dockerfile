FROM jenkins/jenkins:lts

# Switch to root to install packages
USER root

# Install CA certificates and update package lists
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to Jenkins user
USER jenkins