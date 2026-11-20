FROM python:3.12-slim

WORKDIR /app

# Install MongoDB database tools (for mongodump/mongorestore)
# Using tarball for cross-architecture support (ARM64 and x86_64)
# Version 100.20.1 - tested and working on both architectures (100.9.0 shipped Go 1.20.10, affected by CVE-2023-45288, CVE-2024-24790 and CVE-2025-68121; 100.20.1 is built with Go 1.27.3, above the 1.26.9 threshold)
RUN apt-get update && apt-get install -y wget ca-certificates libgssapi-krb5-2 && \
    ARCH=$(dpkg --print-architecture) && \
    echo "Detected architecture: $ARCH" && \
    if [ "$ARCH" = "arm64" ]; then \
        MONGO_TOOLS_URL="https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2004-arm64-100.20.1.tgz"; \
    elif [ "$ARCH" = "amd64" ]; then \
        MONGO_TOOLS_URL="https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2004-x86_64-100.20.1.tgz"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    echo "Downloading MongoDB tools from: $MONGO_TOOLS_URL" && \
    wget -O /tmp/mongodb-tools.tgz "$MONGO_TOOLS_URL" && \
    tar -xzf /tmp/mongodb-tools.tgz -C /tmp && \
    cp /tmp/mongodb-database-tools-*/bin/* /usr/local/bin/ && \
    rm -rf /tmp/mongodb-tools.tgz /tmp/mongodb-database-tools-* && \
    which mongodump && mongodump --version && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create backups directory
RUN mkdir -p /app/backups && chmod 755 /app/backups

# Run the application with hot-reload
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

