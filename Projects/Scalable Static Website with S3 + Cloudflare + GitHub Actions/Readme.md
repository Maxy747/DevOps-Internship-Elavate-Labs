# DevOps Internship - Project 6: Scalable Static Website

This project implements **Project: Scalable Static Website with S3 + Cloudflare + GitHub Actions** from the Elevate Labs internship.

The goal is to build a fully automated CI/CD pipeline that deploys a static website from a GitHub repository to a scalable cloud hosting solution.

### 🔴 Live Website URL

The live website is hosted on AWS S3 and is available here:

**[http://static-website-devops-project.s3-website.eu-north-1.amazonaws.com](http://static-website-devops-project.s3-website.eu-north-1.amazonaws.com)**

---

## Project Architecture

This project uses a serverless, event-driven architecture:

1. **Code:** A developer pushes a change to the `main` branch of this GitHub repository. The website's source code (`index.html`, `style.css`) is located in a subfolder: `Projects/Scalable Static Website with S3 + Cloudflare + GitHub Actions`.
2. **CI/CD Pipeline (GitHub Actions):** A GitHub Actions workflow (`.github/workflows/deployS3.yml`) automatically triggers on the push.
3. **Deploy:** The workflow job authenticates with AWS and uses the `aws s3 sync` command to copy *only* the contents of the project subfolder to the root of the S3 bucket. The `--delete` flag ensures the bucket stays in perfect sync.
4. **Host (AWS S3):** The S3 bucket (`static-website-devops-project`) is configured for static website hosting, making the files publicly accessible via its website endpoint.

---

## Technology Stack

* **AWS S3:** Used for serverless hosting of the static website files.
* **GitHub Actions:** Used as the CI/CD platform to automate the deployment process.
* **AWS IAM:** Used to create a secure user and manage programmatic access (via `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) for GitHub Actions.
* **HTML/CSS:** The content of the static website.

---

## Implementation Details

### 1. AWS S3 Bucket Configuration

The `static-website-devops-project` bucket was configured with the following key settings:

* **Static website hosting:** Enabled, with `index.html` as the index document.
* **Public Access:** The "Block all public access" setting was **disabled**.
* **Bucket Policy:** A policy was applied to allow public `s3:GetObject` permissions for all objects in the bucket:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::static-website-devops-project/*"
        }
    ]
}
```

### 2. GitHub Actions CI/CD Workflow

The following workflow (`.github/workflows/deployS3.yml`) was created to automate deployment. AWS credentials were stored as GitHub secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) to ensure security.

The workflow correctly syncs *only* the project subfolder (`Projects/Scalable Static Website...`) to the S3 bucket.

```yaml
name: Deploy Static Website to S3

on:
  push:
    branches:
      - main
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: eu-north-1

    - name: Deploy to S3
      run: |
        aws s3 sync "Projects/Scalable Static Website with S3 + Cloudflare + GitHub Actions" s3://static-website-devops-project --delete
```

---

## Future Steps (Completing Project)

The original project scope also includes Cloudflare integration. This part has been skipped for now. The next steps would be:

1. **Get a Domain:** Acquire a free domain from a provider like `EU.org`.
2. **Integrate Cloudflare:** Add the domain to a free Cloudflare account and update the nameservers.
3. **Set DNS:** Create a `CNAME` record in Cloudflare pointing to the S3 website endpoint.
4. **Enable HTTPS:** Set the Cloudflare SSL/TLS mode to **"Flexible"** to enable free HTTPS for the site.

---

## Getting Started

To replicate this project:

1. Clone this repository
2. Create an S3 bucket with static website hosting enabled
3. Configure the bucket policy for public access
4. Set up AWS IAM credentials
5. Add AWS credentials as GitHub secrets
6. Push to the `main` branch to trigger automatic deployment

---

## License

This project is part of the Elevate Labs DevOps internship program.
-Mazin
