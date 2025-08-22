# Smart Public Transport Tracker & Alert System

## **Overview**

A cloud-native microservices system for tracking public transport vehicles in real-time and sending alerts to users. The system includes:

- **User Service**: Handles user authentication and profiles.  
- **Alert Service**: Manages notifications and alert creation.  
- **Bus Service**: Tracks buses in real-time.  
- **Frontend Service**: Web interface for interacting with the system.  
- **Database**: PostgreSQL for persisting service data.  
- **Messaging**: Kafka for asynchronous communication between services.  
- **Deployment**: Kubernetes cluster (Minikube for local testing, AWS EKS for cloud deployment).  

---

## **Prerequisites**

- Docker  
- Python 3.10+  
- Node.js 18+ (for frontend)  
- FastAPI
- PostgresQL
- kubectl  
- minikube (for local testing)  
- AWS CLI & `eksctl` (for cloud deployment)  

---

## **Project Structure**

```
smart-transport-tracker/
│
├── services/
│ ├── user-service/
│ ├── alert-service/
│ ├── bus-service/
│ └── docker-compose.yml
│
├── frontend/
│
├── k8s/
│ ├── user-service.yaml
│ ├── alert-service.yaml
│ ├── bus-service.yaml
│ ├── user-db.yaml
│ ├── alert-db.yaml
│ ├── bus-db.yaml
│ ├── frontend-configmap.yaml
│ ├── frontend-deployment.yaml
│ ├── frontend-service.yaml
│ ├── kafka.yaml
│ └── zookeeper.yaml
│
└── README.md
```
Get the frontend from ```https://github.com/pabasara-samarakoon-4176/smart-route-dash.git```

## **Local Testing (Minikube)**

1. Start Minikube
```
minikube start
```

2. Build and push docker images to the DockerHub.
```
docker build --platform linux/amd64 -t <your-dockerhub-username>/user-service:latest .
docker push <your-dockerhub-username>/user-service:latest
```
Repeat this to all of micro services.

3. Apply k8s manifests
```
kubectl apply -f k8s/user-db.yaml
kubectl apply -f k8s/alert-db.yaml
kubectl apply -f k8s/bus-db.yaml
kubectl apply -f k8s/zookeeper.yaml
kubectl apply -f k8s/kafka.yaml
kubectl apply -f k8s/user-service.yaml
kubectl apply -f k8s/alert-service.yaml
kubectl apply -f k8s/bus-service.yaml
kubectl apply -f k8s/frontend-configmap.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

4. Port-forward services for local access
```
kubectl port-forward svc/user-service 9002:9002
kubectl port-forward svc/alert-service 9003:9003
kubectl port-forward svc/bus-service 9004:9004
kubectl port-forward svc/frontend 8081:80
```

5. Access the frontend
```
http://localhost:8081
```

## **Cloud Deployment (AWS EKS)**

1. Configure AWS CLI
```
aws configure
```
It will ask for:
```
AWS Access Key ID [None]: <your-access-key-id>
AWS Secret Access Key [None]: <your-secret-access-key>
Default region name [None]: us-east-1
Default output format [None]: json
```

1. Create EKS Cluster
```
eksctl create cluster \
  --name smart-transport-tracker \
  --region us-east-1 \
  --version 1.30 \
  --nodegroup-name linux-nodes \
  --node-type t3.small \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 4 \
  --managed
```
Specify the k8s version to avoid AWS extended support.

2. Attach EBS CSI driver
```
eksctl create addon \
  --name aws-ebs-csi-driver \
  --cluster smart-transport-tracker \
  --region us-east-1 \
  --force
```

3. Attach IAM policies to node role
Ensure node IAM role has these policies:
- AmazonEKSWorkerNodePolicy
- AmazonEKS_CSI_Driver_Policy
- AmazonEC2FullAccess

4. Deploy Kubernetes manifests
```
kubectl apply -f k8s/user-db.yaml
kubectl apply -f k8s/alert-db.yaml
kubectl apply -f k8s/bus-db.yaml
kubectl apply -f k8s/zookeeper.yaml
kubectl apply -f k8s/kafka.yaml
kubectl apply -f k8s/user-service.yaml
kubectl apply -f k8s/alert-service.yaml
kubectl apply -f k8s/bus-service.yaml
kubectl apply -f k8s/frontend-configmap.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

5. Expose service using NodePort or LoadBalancer.

Forward the service port to local machine:
```
kubectl port-forward svc/user-service 9002:9002
kubectl port-forward svc/alert-service 9003:9003
kubectl port-forward svc/bus-service 9004:9004
kubectl port-forward svc/frontend 8081:80
```
OR
Exposure using Load Balancer:
```
kubectl patch svc user-service -p '{"spec": {"type": "LoadBalancer"}}'
kubectl patch svc bus-service -p '{"spec": {"type": "LoadBalancer"}}'
kubectl patch svc alert-service -p '{"spec": {"type": "LoadBalancer"}}'
kubectl patch svc frontend -p '{"spec": {"type": "LoadBalancer"}}'
```

6. Access the frontend