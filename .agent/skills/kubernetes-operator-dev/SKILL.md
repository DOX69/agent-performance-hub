---
name: kubernetes-operator-dev
description: Expert in building Kubernetes Operators using Python (Kopf) and Go (Kubebuilder). Covers CRD design, reconciliation loops, event handling, and production deployment patterns.
version: "1.0.0"
tags:
  - kubernetes
  - operator
  - python
  - go
  - kopf
  - kubebuilder
  - devops
---

# Kubernetes Operator Dev

## Overview

This skill provides expert guidance on designing, building, and deploying Kubernetes Operators. It focuses on the **Operator Pattern** to automate complex application lifecycle management.

**Primary Frameworks:**
- **Python**: [Kopf (Kubernetes Operator Pythonic Framework)](https://kopf.readthedocs.io/) - Best for data science, AI/ML workloads, and Python teams.
- **Go**: [Kubebuilder](https://book.kubebuilder.io/) / [Operator SDK](https://sdk.operatorframework.io/) - Best for high-performance, core infrastructure operators.

## Core Capabilities

1.  **CRD Design**: Modeling custom resources (APIs) with OpenAPI v3 schemas.
2.  **Reconciliation**: Implementing idempotent loops to bring current state to desired state.
3.  **Event Handling**: Reacting to Create/Update/Delete events on resources.
4.  **Finalizers**: Ensuring clean resource cleanup and deletion logic.
5.  **Testing**: Unit testing handlers and end-to-end testing with Kind/Minikube.

## Python Operator Workflow (Kopf)

### 1. Project Structure
```text
my-operator/
├── deploy/
│   ├── crd.yaml          # CustomResourceDefinition
│   ├── rbac.yaml         # ServiceAccount, Role, RoleBinding
│   └── operator.yaml     # Deployment
├── src/
│   └── handlers.py       # Python logic
├── Dockerfile
└── requirements.txt      # kopf, kubernetes
```

### 2. Basic Handler Pattern
```python
import kopf
import kubernetes.client as k8s

@kopf.on.create('my-group', 'v1', 'mycustomresources')
def create_fn(spec, name, namespace, logger, **kwargs):
    """
    Called when a new MyCustomResource is created.
    """
    size = spec.get('size', 1)
    logger.info(f"Creating resource {name} with size {size}")

    # Logic to create child resources (e.g., Pods, Services)
    api = k8s.CoreV1Api()
    # ... implementation ...

    return {'message': 'created', 'time': kopf.now()}
```

### 3. Idempotency & Error Handling
- **Idempotency**: Handlers must be safe to run multiple times. Check if a child resource exists before creating it.
- **Retries**: Raise `kopf.TemporaryError` for transient failures (e.g., network issues) to trigger a retry with backoff.
- **Permanent Errors**: Raise `kopf.PermanentError` to stop retries for invalid configuration.

## Best Practices

- **Status Subresource**: Always use the `status` subresource to report observation (e.g., `Ready`, `Phase`, `Conditions`). Do not update `spec`.
- **Owner References**: Set `ownerReferences` on child resources so they are garbage collected when the parent CR is deleted.
- **RBAC**: Grant only the necessary permissions (Least Privilege).
- **Structured Logging**: Use the provided `logger` to ensure logs are JSON-formatted and traceable.
- **Namespace Scoping**: Decide if your operator is namespaced or cluster-wide.

## Deployment Checklist

1.  [ ] **CRD Registered**: Apply `crd.yaml` first.
2.  [ ] **RBAC Configured**: Ensure the ServiceAccount has permissions to watch/list/update the CRs and manage child resources.
3.  [ ] **Image Built**: Build multi-arch image (amd64/arm64) for production.
4.  [ ] **Liveness/Readiness**: Configure probes in the Deployment.
5.  [ ] **Monitoring**: Expose metrics (Prometheus) if needed.

## Common Commands

- **Run locally (dev)**: `kopf run src/handlers.py --verbose`
- **Build image**: `docker build -t my-operator:v1 .`
- **Apply manifest**: `kubectl apply -f deploy/`
- **View logs**: `kubectl logs -l app=my-operator -f`
