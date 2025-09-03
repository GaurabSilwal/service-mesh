Here’s a comprehensive **README** you can use for your Service Mesh project with Istio and microservices:

---

# Service Mesh Demo with Istio

This project demonstrates a **service mesh implementation using Istio** on Kubernetes. It showcases **traffic management (canary deployments), observability, and secure service-to-service communication** between microservices.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Microservices](#microservices)
* [Infrastructure Setup](#infrastructure-setup)
* [Service Mesh Setup](#service-mesh-setup)
* [Traffic Management](#traffic-management)
* [Observability](#observability)
* [Security](#security)
* [Verification](#verification)
* [CI/CD Integration](#cicd-integration)

---

## Project Overview

The project demonstrates how a **DevOps/Platform engineer** can deploy microservices in Kubernetes with a **service mesh (Istio)** to handle:

1. **Dynamic routing of traffic** (canary and blue-green deployments)
2. **Metrics collection and observability** (Prometheus, Grafana, Kiali)
3. **Secure service communication** (mTLS, policies)

The goal is to show how **traffic between versions of a service can be controlled without changing the application code**, and how to **monitor and secure microservices** in a production-like Kubernetes environment.

---

## Microservices

The project includes the following microservices:

| Service Name      | Description           | Version Info |
| ----------------- | --------------------- | ------------ |
| `user-service`    | Provides user data    | v1 / v2      |
| `order-service`   | Provides order data   | v1           |
| `payment-service` | Provides payment data | v1           |

Each service exposes a **REST API** and returns JSON data including its `version` for routing verification.

Example response from `user-service v1`:

```json
{"users":["Alice","Bob"],"version":"v1"}
```

---

## Infrastructure Setup

1. **Kubernetes Cluster:**

   * Can use **Minikube, kind, k3s, or cloud-managed clusters (EKS/GKE/AKS)**.
   * Namespaces are created for each service:

     ```bash
     kubectl create namespace user
     kubectl create namespace order
     kubectl create namespace payment
     ```

2. **Deploy Microservices:**

   * Each microservice has a Deployment and Service YAML.
   * Example for `user-service v1`:

     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: user-deployment-v1
       namespace: user
     spec:
       replicas: 3
       template:
         spec:
           containers:
           - name: user
             image: user-service:v1
     ```
   * Apply the YAMLs:

     ```bash
     kubectl apply -f k8s/deployments/user-deployment-v1.yaml
     kubectl apply -f k8s/deployments/user-deployment-v2.yaml
     ```

---

## Service Mesh Setup

1. **Install Istio** on the cluster:

   ```bash
   istioctl install --set profile=demo -y
   ```

2. **Enable automatic sidecar injection** in service namespaces:

   ```bash
   kubectl label namespace user istio-injection=enabled
   kubectl label namespace order istio-injection=enabled
   kubectl label namespace payment istio-injection=enabled
   ```

3. **Verify Istio pods**:

   ```bash
   kubectl get pods -n istio-system
   ```

---

## Traffic Management

**VirtualService** is used to implement canary routing:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-canary
  namespace: user
spec:
  hosts:
  - user-service
  http:
  - route:
    - destination:
        host: user-service
        subset: v1
      weight: 90
    - destination:
        host: user-service
        subset: v2
      weight: 10
```

* **Canary Deployment:** 10% traffic routed to v2, 90% to v1
* **Verification:**

  ```bash
  seq 1 100 | xargs -P20 -n1 sh -c 'curl -s http://user-service.user.svc.cluster.local:80/users' | tee /tmp/responses.txt
  echo "v1=$(grep -c '\"version\":\"v1\"' /tmp/responses.txt), v2=$(grep -c '\"version\":\"v2\"' /tmp/responses.txt)"
  ```

  * Sample Output:

    ```
    v1=91, v2=9
    ```

---

## Observability

Istio provides **monitoring and tracing**:

* **Prometheus:** metrics collection

  ```bash
  istioctl dashboard prometheus
  ```
* **Grafana:** visualize metrics and dashboards

  ```bash
  istioctl dashboard grafana
  ```
* **Kiali:** view service mesh topology

  ```bash
  istioctl dashboard kiali
  ```
* **Jaeger:** distributed tracing

  ```bash
  istioctl dashboard jaeger
  ```

---

## Security

1. **Mutual TLS** is enabled by Istio between services:

   * Encrypts traffic between microservices automatically.
2. **Authorization policies** can be applied to allow/deny traffic:

   ```yaml
   apiVersion: security.istio.io/v1beta1
   kind: AuthorizationPolicy
   metadata:
     name: user-policy
     namespace: user
   spec:
     rules:
     - from:
       - source:
           principals: ["cluster.local/ns/order/sa/default"]
   ```

---

## CI/CD Integration

* Docker images for each service version are built and pushed to a container registry.
* Kubernetes manifests are deployed automatically using **GitHub Actions or Jenkins pipelines**.
* Istio configurations (VirtualService, DestinationRule) can also be applied via CI/CD to automate canary and blue-green deployments.

---

## Verification Workflow

1. **Check service responses:**

   ```bash
   kubectl exec -it <pod-name> -n user -- curl -s http://user-service.user.svc.cluster.local:80/users
   ```
2. **Verify canary traffic split** using multiple concurrent curl requests and `grep` (as shown above).
3. **Monitor traffic, latency, and errors** using Grafana/Kiali dashboards.

---

## Goal Achieved

This project demonstrates:

* How **Istio sidecars handle service-to-service traffic**
* How **canary routing works without modifying service code**
* How to **collect metrics, traces, and visualize traffic flow**
* How **secure policies and mTLS** protect service communication

---

This README can be included in your repo and shared as the **documentation for your service mesh project**.

---
