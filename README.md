# Cloud Run Parallel Task Processor

### Overview

This repository demonstrates how to process large datasets in parallel using Cloud Run Jobs and Google BigQuery. It provides a scalable and cost-effective solution for data processing tasks by splitting the workload into smaller batches and processing them concurrently.

We will have interaction with the following GCP components:

*   **Cloud Run Job:** A containerized application that we can leverage on for parallel processing tasks
*   **Google BigQuery:** A fully-managed, serverless data warehouse used for storing and querying the data.
*   **Container Registry:** A Docker image registry for storing the container image.

### Prerequisites

Before you begin, ensure you have the following:

*   A Google Cloud Platform (GCP) project.
*   The Google Cloud SDK (gcloud) installed and configured.
*   Docker installed.
*   Enabled the Cloud Run, Container Registry, and BigQuery APIs.
*   Created a repository under Container Registry to house the docker image pushed

### Step by step instruction

**Configure GCP Project**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**Build the Docker Image**
```bash
docker build -t parallel-processor . # replace with the name you want
```

**Tag the image for Google Cloud Container Registry**

```bash
# Replace LOCATION with your desired GCP region (e.g., us-central1).
# Replace PROJECT_ID with your GCP project ID.
# Replace REPOSITORY with your desired repository name (e.g., parallel-processor).
docker tag parallel-processor LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/parallel-processor:latest
```

**Push the image to Container Registry**
```bash
docker push LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/parallel-processor:latest
```

**Create a Cloud Run job**
```bash
gcloud run jobs create parallel-bq-processor \
    --image LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/parallel-processor:latest \
    --region LOCATION
```

**Trigger the Cloud Run Job**
```bash
gcloud run jobs execute parallel-bq-processor
```
