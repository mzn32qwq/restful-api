# Web Service Assignment2

---
This project is a microservices architecture based on Kubernetes, consisting of two services: the authentication service (auth_server) 
and the URL shortening service (shorten_url). The authentication service is responsible for user authentication, 
while the URL shortening service provides URL shortening functionality. 
This document will explain how to deploy and run these two services, as well as provide detailed information on data consistency.

## Deploying and Running the Services
### 1. Deploying to Kubernetes Cluster

Apply the YAML files to the Kubernetes cluster by executing the following commands:
```bash
kubectl apply -f deployment_auth.yml
kubectl apply -f deployment_shorten.yml
```
### 2. Docker Image and Container Configuration
build image
```bash
 docker build -t shorten_url -f Dockerfile_shorten_url .
 docker build -t auth_server -f Dockerfile_auth .
```
after tag and push image to dockerhub, start docker compose
```BASH
docker compose up
```

## Volume Configuration and Data Consistency
* To achieve data persistence and consistency, we utilize Kubernetes Persistent Volumes (PVs) and Persistent Volume Claims (PVCs). 
We mount the directory /Users/xiongjingjing/Web_service-Assignment2 on the host to the /auth/file directory in the container to 
share and persist data when using docker compose to deploy.

* Within the Kubernetes cluster, we also employ NFS storage to provide persistent storage. NFS storage offers data sharing across
multiple pods and nodes, ensuring data consistency and reliability. We configure the NFS server's address as 145.100.135.157(which is ip of master node) 
with a mount path of /data.

* For each service, we mount the NFS storage to the /auth/file directory in the container, ensuring that the data shared 
between the authentication service and URL shortening service remains consistent.

## Considerations
* Before deployment, the Kubernetes cluster is properly configured and that necessary plugins and tools are installed.

* The NFS server's address and mount path match the values provided can be accessed correctly.
```BASH
sudo chmod -R 777 /data
```

* To ensure data security and consistency, regularly back up and monitor data storage, as well as perform routine updates and maintenance on the system.


