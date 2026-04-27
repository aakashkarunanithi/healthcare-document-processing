🏥 Healthcare Document Processing System

A cloud-based document processing system that extracts structured data from healthcare documents using AWS Bedrock Data Automation. The system automates manual data extraction through an asynchronous processing pipeline.

🚀 Features
🤖 AI-powered document extraction using AWS Bedrock
☁️ Integration with AWS S3 for document storage
⚡ FastAPI backend for API handling
🔁 Asynchronous job workflow (submit → poll → fetch)
📦 Structured JSON output extraction
🧩 Modular backend architecture

🏗️ Architecture
The system works in the following flow:

Document Upload
- Documents are stored in AWS S3

Job Submission
- API triggers a Bedrock Data Automation job

Processing
- AWS processes the document asynchronously

Polling
- System checks job status periodically

Result Retrieval
- Extracted structured data is returned

🛠️ Tech Stack
Backend: FastAPI  
Cloud: AWS Bedrock (BDA), AWS S3  
AI: Bedrock Data Automation  
Database: PostgreSQL  

📦 Project Setup

1. Clone the repository
git clone https://github.com/aakashkarunanithi/healthcare-doc-processing
cd healthcare-doc-processing

2. Install dependencies
pip install -r requirements.txt

3. Setup environment variables

Create a .env file:

AWS_ACCESS_KEY=
AWS_SECRET_KEY=
AWS_REGION=
S3_BUCKET_NAME=

4. Run the application
uvicorn main:app --reload

📂 Project Structure
src/
 ├── controllers/
 ├── services/
 ├── repositories/
 ├── utils/
 └── main.py

🔐 Security
- Credentials are stored in environment variables
- Secure access to AWS services
