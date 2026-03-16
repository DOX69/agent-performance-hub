---
name: cost-optimization
description: Expert patterns and strategies for optimizing cloud costs and resource management. Use when analyzing cloud spend, rightsizing instances, implementing spot instances, or designing cost-effective architectures.
version: "1.0.0"
tags:
  - cost-optimization
  - cloud
  - aws
  - azure
  - gcp
  - finops
---

# Cost Optimization

## Overview

This skill provides FinOps best practices and architectural patterns for cloud cost optimization. It helps AI agents analyze infrastructure configurations and propose changes that significantly reduce monthly spend without sacrificing performance or reliability.

## Core Capabilities

### 1. Compute Optimization
- **Rightsizing**: Analyze metrics to match instance types/sizes to actual workload requirements.
- **Spot Instances**: Identify stateless, fault-tolerant workloads suitable for Spot pricing (up to 90% savings).
- **Graviton/ARM Adoption**: Migrate compatible workloads to ARM-based processors for better price-performance.

### 2. Storage Lifecycle Management
- **Tiering**: Implement automated transition rules (e.g., S3 Standard → Infrequent Access → Glacier).
- **Cleanup**: Identify and remove unattached EBS volumes, outdated snapshots, and orphaned IPs.

### 3. Architectural Efficiency
- **Serverless**: Evaluate migrating low-utilization containers/VMs to serverless functions to scale to zero.
- **Caching**: Implement CDN or database caching (Redis/Memcached) to reduce expensive backend compute and database read operations.

## Decision Tree: Cost Analysis Workflow

```
User task → Does it involve existing infrastructure?
    ├─ Yes (Audit) → Identify the highest spend category
    │    ├─ Compute → Propose rightsizing, savings plans, or Spot instances
    │    ├─ Storage → Propose lifecycle policies and volume cleanup
    │    └─ Network → Propose NAT Gateway optimization or CDN caching
    │
    └─ No (New Architecture) → Design for cost-efficiency from day one
         ├─ Unpredictable load → Recommend Serverless/Auto-scaling
         └─ Predictable load → Recommend Reserved Instances/Savings Plans
```

## Best Practices
- **Tagging**: Always recommend comprehensive tagging strategies to enable accurate cost allocation.
- **Metrics-Driven**: Never suggest downgrading resources without confirming utilization metrics.
- **Trade-offs**: Always articulate the trade-offs between cost savings and operational overhead or risk.
