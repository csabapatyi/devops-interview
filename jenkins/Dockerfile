FROM jenkins/jenkins:lts-jdk17

USER root

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y curl jq vim nano podman && \
    rm -rf /var/lib/apt/lists/*

USER jenkins