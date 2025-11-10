# Google Artifact Registry - Google Cloud Image Registry

## 📦 What is Google Artifact Registry?

**Google Artifact Registry** is Google Cloud Platform's (GCP) artifact registry service. It allows you to store, manage, and secure Docker container images, language packages (npm, Maven, Python), and other build artifacts.

### Why use Artifact Registry instead of DockerHub?

| Feature | Artifact Registry | DockerHub |
|---------|-------------------|-----------|
| **GCP Integration** | ✅ Native and optimized | ⚠️ Requires additional configuration |
| **Performance** | ✅ Faster (same infrastructure) | ⚠️ Depends on location |
| **Security** | ✅ Native Google IAM | ⚠️ Separate permission system |
| **Cost** | ✅ 0.5GB free/month | ✅ Free (limited) |
| **Privacy** | ✅ Private by default | ⚠️ Requires paid plan for private |
| **Vulnerability analysis** | ✅ Integrated | ⚠️ Only in paid plans |

## 🚀 Complete Step-by-Step Guide

### Prerequisites

1. Google Cloud Platform account
2. gcloud CLI installed and configured
3. Docker installed
4. GCP project created

### Step 1: Configure gcloud CLI

```powershell
# Login
gcloud auth login

# List available projects
gcloud projects list

# Set the project (replace with your PROJECT_ID)
gcloud config set project YOUR-PROJECT-ID

# Verify configuration
gcloud config get-value project
```

### Step 2: Enable Artifact Registry API

```powershell
# Enable the API
gcloud services enable artifactregistry.googleapis.com

# Verify it was enabled
gcloud services list --enabled | Select-String "artifactregistry"
```

### Step 3: Create a Repository in Artifact Registry

Artifact Registry organizes images into **repositories**. You need to create one before pushing images.

```powershell
# Create repository
gcloud artifacts repositories create fastapi-repo `
  --repository-format=docker `
  --location=us-central1 `
  --description="Repository for FastAPI images"
```

**Parameters explained:**
- `fastapi-repo`: Your repository name (you can choose another)
- `--repository-format=docker`: Artifact type (docker, npm, maven, etc.)
- `--location=us-central1`: Region where the repository will be located (choose the closest one)
- `--description`: Optional description

**Available regions in Brazil and South America:**
- `southamerica-east1` (São Paulo) - **Recommended for Brazil**
- `southamerica-west1` (Santiago, Chile)

```powershell
# Example for Brazil
gcloud artifacts repositories create fastapi-repo `
  --repository-format=docker `
  --location=southamerica-east1 `
  --description="Repository for FastAPI images"
```

### Step 4: List and Verify Repositories

```powershell
# List all repositories
gcloud artifacts repositories list

# See details of a specific repository
gcloud artifacts repositories describe fastapi-repo --location=southamerica-east1
```

### Step 5: Configure Docker Authentication

To push images, you need to authenticate Docker with Artifact Registry:

```powershell
# Configure authentication (recommended method)
gcloud auth configure-docker southamerica-east1-docker.pkg.dev

# Answer 'Y' when prompted
```

This adds credentials to Docker's configuration file (`~/.docker/config.json`).

### Step 6: Build the Docker Image

```powershell
# Navigate to project folder
cd c:\Users\gabri\Documents\gcloud-run

# Build image with correct tag for Artifact Registry
# Format: REGION-docker.pkg.dev/PROJECT-ID/REPOSITORY-NAME/IMAGE-NAME:TAG
docker build -t southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1 .
```

**Tag structure explained:**
```
southamerica-east1-docker.pkg.dev / YOUR-PROJECT-ID / fastapi-repo / fastapi-app : v1
        ↓                                  ↓                ↓             ↓        ↓
    Region                            GCP Project      Repository     Name     Version
```

**Real example:**
```powershell
docker build -t southamerica-east1-docker.pkg.dev/my-project-123/fastapi-repo/fastapi-app:v1 .
```

### Step 7: Push the Image

```powershell
# Push image to Artifact Registry
docker push southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1
```

You'll see the upload progress:
```
The push refers to repository [southamerica-east1-docker.pkg.dev/my-project-123/fastapi-repo/fastapi-app]
abc123def456: Pushed
def456ghi789: Pushed
v1: digest: sha256:... size: 1234
```

### Step 8: Verify the Image in Artifact Registry

```powershell
# List images in repository
gcloud artifacts docker images list southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo

# See details of a specific image
gcloud artifacts docker images describe `
  southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1
```

**Via Web Console:**
1. Go to: https://console.cloud.google.com/artifacts
2. Select your repository (`fastapi-repo`)
3. You'll see all available images and tags

## 🚢 Deploy to Cloud Run using Artifact Registry

### Method 1: Via gcloud CLI

```powershell
gcloud run deploy fastapi-app `
  --image southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1 `
  --platform managed `
  --region southamerica-east1 `
  --allow-unauthenticated `
  --port 8000
```

**Advantages:**
- ✅ Much faster (image in same region)
- ✅ No external transfer costs
- ✅ Automatic permission integration

### Method 2: Via Web Console

1. Go to: https://console.cloud.google.com/run
2. Click **CREATE SERVICE**
3. In "Container image URL", click **SELECT**
4. Navigate: **Artifact Registry** → `fastapi-repo` → `fastapi-app` → Select tag `v1`
5. Configure the service and click **CREATE**

## 🔄 Complete Workflow

```powershell
# 1. Make code changes
# ... edit files ...

# 2. Build new version
docker build -t southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v2 .

# 3. Push new version
docker push southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v2

# 4. Update Cloud Run with new version
gcloud run deploy fastapi-app `
  --image southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v2 `
  --region southamerica-east1
```

## 🏷️ Versioning Best Practices

### Tag Strategy

```powershell
# Tag with specific version
docker tag my-image REGISTRY/IMAGE:v1.0.0

# Latest tag (latest version)
docker tag my-image REGISTRY/IMAGE:latest

# Tag with commit identifier
docker tag my-image REGISTRY/IMAGE:abc123

# Tag with environment
docker tag my-image REGISTRY/IMAGE:production
docker tag my-image REGISTRY/IMAGE:staging
```

### Complete Example with Multiple Tags

```powershell
# Build image
docker build -t fastapi-local .

# Create multiple tags
$REGISTRY = "southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app"

docker tag fastapi-local ${REGISTRY}:v1.0.0
docker tag fastapi-local ${REGISTRY}:latest
docker tag fastapi-local ${REGISTRY}:production

# Push all tags
docker push ${REGISTRY}:v1.0.0
docker push ${REGISTRY}:latest
docker push ${REGISTRY}:production
```

## 🛡️ Permission Management

### Grant Access to Specific Users

```powershell
# Give read permission (pull)
gcloud artifacts repositories add-iam-policy-binding fastapi-repo `
  --location=southamerica-east1 `
  --member=user:email@example.com `
  --role=roles/artifactregistry.reader

# Give write permission (push)
gcloud artifacts repositories add-iam-policy-binding fastapi-repo `
  --location=southamerica-east1 `
  --member=user:email@example.com `
  --role=roles/artifactregistry.writer
```

### Allow Cloud Run to access the repository

By default, Cloud Run already has access, but if there are issues:

```powershell
# Get Cloud Run service account
gcloud run services describe fastapi-app --region=southamerica-east1 --format="value(spec.template.spec.serviceAccountName)"

# Grant access
gcloud artifacts repositories add-iam-policy-binding fastapi-repo `
  --location=southamerica-east1 `
  --member=serviceAccount:SERVICE_ACCOUNT_EMAIL `
  --role=roles/artifactregistry.reader
```

## 🧹 Cleanup and Management

### Delete Old Images

```powershell
# Delete a specific tag
gcloud artifacts docker images delete `
  southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1 `
  --delete-tags

# List and delete unused images
gcloud artifacts docker images list southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo `
  --filter="NOT tags:*" `
  --format="get(IMAGE)"
```

### Configure Automatic Cleanup Policy

Keep only the last 10 versions:

```powershell
# Create policy file (cleanup-policy.json)
# File content:
{
  "name": "keep-recent-versions",
  "action": "DELETE",
  "condition": {
    "tagState": "TAGGED",
    "olderThan": "2592000s",
    "tagPrefixes": ["v"]
  },
  "mostRecentVersions": {
    "keepCount": 10
  }
}

# Apply policy
gcloud artifacts repositories set-cleanup-policies fastapi-repo `
  --location=southamerica-east1 `
  --policy=cleanup-policy.json
```

## 💰 Costs and Limits

### Pricing (approximate values)

- **Storage**: $0.10 per GB/month
- **Network traffic**:
  - Same region: Free
  - Between regions: $0.01 per GB
  - To internet: Varies by region

### Free Tier

- **0.5 GB** of free storage per month
- Traffic within same region: Free

### Calculate your usage

```powershell
# See image sizes
docker images southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app
```

## 🔍 Monitoring and Logs

### View Artifact Registry logs

```powershell
# Access logs
gcloud logging read "resource.type=artifact_registry" --limit 50 --format json

# Logs from a specific repository
gcloud logging read "resource.type=artifact_registry AND resource.labels.repository_id=fastapi-repo" --limit 20
```

### Check for vulnerabilities

```powershell
# Scan image for vulnerabilities
gcloud artifacts docker images scan `
  southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1

# View scan results
gcloud artifacts docker images list-vulnerabilities `
  southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1
```

## 🆚 Comparison: Artifact Registry vs DockerHub vs GitHub Container Registry

| Feature | Artifact Registry | DockerHub | GitHub Container Registry |
|---------|-------------------|-----------|---------------------------|
| **GCP Integration** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Cost** | $0.10/GB/month | Free (limited) | Free (limited) |
| **Performance on GCP** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Security** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Ease of use** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Vulnerability scanning** | ✅ Included | 💰 Paid | ✅ Included |

## 🔧 Troubleshooting

### Error: "Permission denied"

```powershell
# Reconfigure authentication
gcloud auth login
gcloud auth configure-docker southamerica-east1-docker.pkg.dev
```

### Error: "Repository not found"

```powershell
# Check if repository exists
gcloud artifacts repositories list --location=southamerica-east1

# Create if necessary
gcloud artifacts repositories create fastapi-repo `
  --repository-format=docker `
  --location=southamerica-east1
```

### Error: "API not enabled"

```powershell
# Enable Artifact Registry API
gcloud services enable artifactregistry.googleapis.com

# Wait a few seconds and try again
```

### Push too slow

```powershell
# Check image size
docker images | Select-String "fastapi-app"

# Optimize image (use multi-stage build in Dockerfile)
# Choose closest region
# Check internet connection
```

## 📚 Additional Resources

- [Official Documentation - Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- [Quickstart - Docker in Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/quickstart)
- [Artifact Registry Pricing](https://cloud.google.com/artifact-registry/pricing)
- [Best Practices](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images)
- [Vulnerability Analysis](https://cloud.google.com/artifact-registry/docs/analysis)

## 📝 Command Summary

```powershell
# Initial setup
gcloud auth login
gcloud config set project YOUR-PROJECT-ID
gcloud services enable artifactregistry.googleapis.com

# Create repository
gcloud artifacts repositories create fastapi-repo `
  --repository-format=docker `
  --location=southamerica-east1

# Configure Docker
gcloud auth configure-docker southamerica-east1-docker.pkg.dev

# Build and Push
docker build -t southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1 .
docker push southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1

# Deploy to Cloud Run
gcloud run deploy fastapi-app `
  --image southamerica-east1-docker.pkg.dev/YOUR-PROJECT-ID/fastapi-repo/fastapi-app:v1 `
  --region southamerica-east1 `
  --allow-unauthenticated `
  --port 8000
```

---

**💡 Final Tip**: Use Artifact Registry for professional and production projects on GCP. The native integration, security, and performance compensate for the small storage cost!
