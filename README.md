# CloudCart — Python E-Commerce Application for Google Cloud

## Stack
- Python 3.12 + Flask
- Google Cloud Run
- Google Firestore
- Docker
- Cloud Build
- Git/GitHub ready

## Features
- Product catalog
- Product search
- Product details
- Session-based shopping cart
- Quantity updates
- Checkout/order creation
- Firestore product and order storage
- Health endpoint
- Local demo mode without GCP

## 1. Run locally

Windows PowerShell:

```powershell
cd gcp-ecommerce-app
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:USE_FIRESTORE="false"
python app.py
```

Open http://localhost:8080

## 2. Install Google Cloud CLI

Install Google Cloud CLI, then:

```powershell
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

## 3. Enable GCP APIs

```powershell
gcloud services enable run.googleapis.com cloudbuild.googleapis.com firestore.googleapis.com artifactregistry.googleapis.com
```

## 4. Create Firestore

Choose Native mode:

```powershell
gcloud firestore databases create --location=asia-south1
```

If your project/CLI does not accept that location, create the Firestore database from Google Cloud Console using a supported nearby location.

## 5. Seed products

```powershell
$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
python seed_firestore.py
```

## 6. Build and deploy to Cloud Run

```powershell
gcloud builds submit --config cloudbuild.yaml
```

The Cloud Build pipeline:
1. Builds the Docker image
2. Pushes it to Container Registry
3. Deploys it to Cloud Run
4. Enables Firestore mode

## 7. Direct deployment alternative

```powershell
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ecommerce-app
gcloud run deploy ecommerce-app `
  --image gcr.io/YOUR_PROJECT_ID/ecommerce-app `
  --region asia-south1 `
  --allow-unauthenticated `
  --set-env-vars USE_FIRESTORE=true
```

## 8. Architecture

Browser
   |
   v
Cloud Run (Flask + Gunicorn)
   |
   +---- Firestore: products/orders
   |
   +---- Cloud Build: CI/CD
   |
   +---- Container Registry: Docker image

## Important production improvements

This starter is intentionally focused on learning and deployment. For a production system, add:
- Identity Platform / OAuth authentication
- Cloud SQL or a stronger transactional data model if required
- Cloud Storage for product images
- Secret Manager for secrets
- Cloud Logging and Monitoring
- Cloud Armor
- Pub/Sub for asynchronous order events
- payment gateway integration
- inventory/stock management
- automated tests
- GitHub Actions or Cloud Build triggers
- Terraform infrastructure as code
- HTTPS/custom domain
- rate limiting and security headers

## Cost note

Google Cloud pricing changes. Cloud Run and several other GCP services have free tiers/quotas, but usage outside applicable free allowances can incur charges. Set a billing budget alert before experimenting.

## CI/CD

CloudCart is automatically tested, containerized, and deployed
to Google Cloud Run using Cloud Build.
