Python Web Service


A simplified Python web service that is containerized, running locally through a self-signed certificate


## Prereqs that are needed


- Docker and Docker Compose
- OpenSSL— used within Mac


## How it will run


1. **Created a repo and cloned the repo**


```bash
git clone https://github.com/securepixels/cloud-task.git
cd cloud-task
```


2. **Generated a self-signed TLS certificate**


```bash
chmod +x generate-cert.sh # certificate file
./generate-cert.sh
```


After running this command, it created a certs/ directory with a cert.pem (the certificate) and a key.pem (this houses the private key). The certificate is then issued to localhost and is valid for 365 days.


3. **Building and starting the service**


```bash
docker compose up --build
```
What this command does is build the Docker with the files included


4. **The Service**


Once Docker finished building, it was time to visit it in my browser using localhost. It is created with the domain [https://localhost]. When visiting, it showed the warning about the self-signed certificate that I generated. Which was important to note because it wasn't issued by a trusted certificate authority but by my very own. After viewing this, I simply clicked continue


You can also test this by using curl


```bash
curl -k https://localhost  # the k allows the self-signing certificate to be accepted
```
5. **Stopping the service**


```bash
docker compose down
```


This command stops everything


## What It Actually Does


The service has two endpoints:
- `GET /` — Returns the service name, status, and current timestamp in JSON
- `GET /health` — Returns a simple health check response
Every request is logged with its method, path, and source IP.


## Designated Choice


**Python with Flask** — I chose Flask because it's lightweight and easy to understand. For a small service like this, it does the job without pulling in anything drastic.
**HTTPS directly in Flask** — Flask supports passing in an SSL certificate and key directly, so I used that rather than adding a separate reverse proxy. For a local demo, this keeps things simple. I used just one container to build and run. In a production setup, I'd put something like Nginx or a load balancer in front to handle TLS instead.


**Self-signed certificate** — Since this is a local demo, I wrote a small shell script that generates a self-signed cert with OpenSSL. The cert files are created on the host machine during setup and mounted as a read-only volume in the container. They're excluded from version control in the .gitignore file.
**Logging** — I added basic request logging using Python's built-in logging module. Each request gets a log line with the timestamp, method, path, and client IP. A simple way to see what's happening without adding any extra dependencies.


## Why Storing a Private SSL Key in a Repository Is Bad Practice
The private key is what allows a server to prove its identity and decrypt HTTPS traffic. If someone gets access to your private key, they could impersonate your server or read encrypted traffic meant for it. Committing a private key to a Git repository means it's stored permanently in the Git history; even if you delete the file later, it can still be recovered from previous commits. Anyone with access to the repository would have the key, and if the repo is public, that means anyone on the internet. In a real environment, private keys and other secrets should be stored using tools designed for that purpose, like AWS Secrets Manager or environment variables injected at deploy time. In this project, the certificate is generated locally, and the `certs/` directory is in .gitignore to keep it out of the repository.


## How I Would Deploy This to AWS


For an AWS deployment, I would choose **ECS with Fargate** to eliminate the need for server management.


The general steps would be to


1. **Push the Docker image to ECR** (Elastic Container Registry), which is AWS's container image storage.


2. **Create an ECS task definition** that tells ECS which image to run, how much CPU and memory to give it, and what port to expose.


3. **Set up an Application Load Balancer (ALB)** in front of the ECS service. The ALB would use a real certificate from AWS Certificate Manager (ACM) instead of a self-signed one. This way, browsers trust the connection without any warnings.


4. **Put the ECS tasks in private subnets** inside a VPC so they aren't directly exposed to the internet. Only the ALB would be public-facing.


5. **Use CloudWatch Logs** for monitoring. ECS has a built-in log driver that sends container output to CloudWatch, so you can view logs without SSHing into anything.
The main differences from the local setup would be that TLS is handled by the load balancer rather than the app, and secrets are stored in AWS Secrets Manager or SSM Parameter Store rather than on disk. I'd also create a dedicated IAM task execution role scoped with least privilege permissions — only the access the container actually needs to pull its image and write logs, nothing more.


## What I Would Improve With More Time
- Add tests for the endpoints and a GitHub Actions workflow to run them automatically on each push
- Add a /metrics endpoint using something like Prometheus client to expose request counts, latency, and error rates for monitoring and alerting
- Add an HTTP-to-HTTPS redirect so port 80 requests get forwarded to 443


## AI Tools Used
I used Claude to lay out the project structure and refine the README file, but reviewed all code and documentation on my own.



