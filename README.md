# AWS Serverless Automated Image Processing Pipeline

An end-to-end, event-driven serverless architecture built on AWS that automates image uploads, validates file types, performs asynchronous processing (resizing and watermarking), extracts metadata, and delivers optimized assets globally via CDN.

---

## 🏗️ Architecture Overview

![Architecture Diagram](./serverless-diagram.drawio.png)

The system processes images through an asynchronous event-driven workflow:

1. **Client Request:** The client sends a `GET /uploads` request to **Amazon API Gateway**.
2. **Presigned URL Generation:** API Gateway triggers the `Img-PresignedUrl` **AWS Lambda** function to generate and return a secure Amazon S3 presigned URL.
3. **Direct S3 Upload:** The client uploads the raw image directly to the **Source S3 Bucket** (`my-image-uploads-src-2026`) via the presigned URL.
4. **Event Notification & Queueing:** An `s3:ObjectCreated` event sends a notification to an **Amazon SQS** queue to decouple storage and execution.
5. **Workflow Orchestration:** SQS triggers the **AWS Step Functions** state machine, which sequentially executes:
   * **`Img-Validate`**: Verifies file extensions (`.jpg`, `.png`, etc.) and payload structure.
   * **`Img-ResizeAndWatermark`**: Resizes the image and applies a custom text watermark using a custom Lambda Layer (Pillow), saving the processed asset into the **Destination S3 Bucket** (`my-image-uploads-dest-2026`).
   * **`Img-ExtractAndSaveMetadata`**: Extracts image dimensions, format, and timestamp, saving the record to **Amazon DynamoDB** (`ImageMetadata`).
6. **Error Handling:** If any execution step fails, Step Functions catches the error and triggers an **Amazon SNS** topic to send an email notification.
7. **Global Content Delivery:** Processed images are securely cached and delivered to users globally via **Amazon CloudFront** using Origin Access Control (OAC).

---

## 🛠️ AWS Services & Tech Stack

* **API & Compute:** Amazon API Gateway, AWS Lambda (Python 3.x), AWS Lambda Layers (Pillow library)
* **Storage & Caching:** Amazon S3 (Source & Destination Buckets), Amazon CloudFront (CDN with OAC)
* **Orchestration & Integration:** AWS Step Functions (ASL), Amazon SQS, Amazon SNS
* **Database:** Amazon DynamoDB

## 🚀 API Endpoint & Usage

### 1. Request Presigned Upload URL

**Endpoint:** `GET /uploads`

curl -X GET "https://<YOUR-API-ID>[.execute-api.eu-west-1.amazonaws.com/uploads?filename=test-image.jpg](https://.execute-api.eu-west-1.amazonaws.com/uploads?filename=test-image.jpg)"

**Sample Response:**
{
  "uploadUrl": "[https://my-image-uploads-src-2026.s3.amazonaws.com/test-image.jpg?AWSAccessKeyId=...&Signature=](https://my-image-uploads-src-2026.s3.amazonaws.com/test-image.jpg?AWSAccessKeyId=...&Signature=)...",
  "key": "test-image.jpg"
}

### 2. Upload Image Direct to S3

Send a `PUT` request with binary image data to the retrieved `uploadUrl`:

curl -X PUT \
  -H "Content-Type: image/jpeg" \
  --data-binary "@test-image.jpg" \
  "<YOUR_UPLOAD_URL>"

### 3. Fetch Processed Asset via CDN

Access the processed asset via CloudFront domain:

https://<YOUR-CLOUDFRONT-DOMAIN>.cloudfront.net/processed/test-image.jpg

---

## 📝 Deployment Note

The core AWS cloud infrastructure components (S3 buckets, SQS queues, DynamoDB table, CloudFront distribution, SNS topic, and IAM execution roles) were provisioned and configured using the **AWS Management Console**. Source code for all AWS Lambda functions and the Step Functions state machine definition are version-controlled within this repository.
