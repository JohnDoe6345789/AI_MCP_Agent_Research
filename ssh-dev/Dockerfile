FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# SSH, git, GitHub CLI, and basics
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      openssh-server \
      git \
      curl \
      ca-certificates \
      sudo \
      gnupg && \
    rm -rf /var/lib/apt/lists/*

# Install GitHub CLI (gh) from official repo :contentReference[oaicite:3]{index=3}
RUN mkdir -p -m 755 /etc/apt/keyrings && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg >/dev/null && \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) \
      signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] \
      https://cli.github.com/packages stable main" \
      | tee /etc/apt/sources.list.d/github-cli.list >/dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends gh && \
    rm -rf /var/lib/apt/lists/*

# Create non-root dev user
ARG DEV_USER=dev
ARG DEV_UID=1000
ARG DEV_GID=1000

RUN groupadd -g ${DEV_GID} ${DEV_USER} && \
    useradd -m -s /bin/bash -u ${DEV_UID} -g ${DEV_GID} ${DEV_USER} && \
    echo "${DEV_USER}:${DEV_USER}" | chpasswd && \
    usermod -aG sudo ${DEV_USER} && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-dev-nopasswd && \
    chmod 440 /etc/sudoers.d/99-dev-nopasswd

# SSHD setup
RUN mkdir -p /var/run/sshd && \
    mkdir -p /home/${DEV_USER}/.ssh && \
    chown -R ${DEV_USER}:${DEV_USER} /home/${DEV_USER}/.ssh && \
    chmod 700 /home/${DEV_USER}/.ssh

# Local-only: allow password auth for convenience
RUN sed -ri 's/^#?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -ri 's/^#?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config

# Shared workspace mount
RUN mkdir -p /workspace && chown ${DEV_USER}:${DEV_USER} /workspace

WORKDIR /workspace

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
