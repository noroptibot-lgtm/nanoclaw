# Software Architecture (Senior Architect)

## Overview

The Software Architecture skill provides comprehensive frameworks and patterns for designing scalable, maintainable, and resilient software systems. This skill enables architects to create system designs, evaluate architectural patterns, define technical standards, and ensure alignment between business requirements and technical solutions. It combines architectural patterns, system design principles, technology evaluation, and documentation with deep expertise in distributed systems, microservices, and cloud architectures.

## Who Should Use This Skill

- **Software Architects** designing system architectures
- **Senior Engineers** making architectural decisions
- **Tech Leads** establishing technical direction
- **Principal Engineers** defining architecture standards
- **Solution Architects** designing end-to-end solutions
- **Enterprise Architects** aligning technology strategy
- **Engineering Managers** evaluating architectural tradeoffs
- **CTO/VPs** making strategic technology decisions

## Purpose and Use Cases

Use this skill when you need to:
- Design system architectures from scratch
- Evaluate and select architectural patterns
- Create architecture decision records (ADRs)
- Design microservices architectures
- Implement event-driven architectures
- Design distributed systems
- Create API and integration strategies
- Evaluate technology stacks
- Design for scalability and performance
- Implement security architectures
- Create disaster recovery strategies
- Document system architectures

**Keywords that trigger this skill:** architecture, system design, microservices, distributed systems, scalability, design patterns, architectural patterns, API design, event-driven, CQRS, saga pattern, architecture decision

## What's Included

### Architecture Pattern Library

**Architectural Patterns:**
- **Monolithic Architecture** - Single deployable unit
- **Microservices Architecture** - Distributed independent services
- **Event-Driven Architecture** - Asynchronous event communication
- **Layered Architecture** - Separation of concerns by layers
- **Hexagonal Architecture** - Ports and adapters pattern
- **CQRS** - Command Query Responsibility Segregation
- **Event Sourcing** - Event-based state management
- **Serverless Architecture** - Function-as-a-Service pattern
- **Service Mesh** - Infrastructure layer for service communication
- **API Gateway Pattern** - Single entry point for APIs

**Pattern Documentation:**
```yaml
# Architecture Pattern: Microservices

name: Microservices Architecture
category: Distributed Systems
complexity: High
maturity: Mature

description: |
  Architectural style that structures an application as a collection of
  loosely coupled, independently deployable services. Each service is
  responsible for a specific business capability.

characteristics:
  - Independent deployment
  - Technology heterogeneity
  - Organized around business capabilities
  - Decentralized data management
  - Infrastructure automation

when_to_use:
  - Large, complex applications
  - Need for independent scalability
  - Multiple teams working in parallel
  - Different technology requirements per service
  - Frequent deployments required

when_not_to_use:
  - Small applications
  - Limited team size
  - Simple domain
  - Tight coupling between components required
  - Limited operational maturity

benefits:
  - Independent scalability
  - Technology flexibility
  - Fault isolation
  - Faster development cycles
  - Easy to understand and maintain individual services

drawbacks:
  - Distributed system complexity
  - Network latency
  - Data consistency challenges
  - Testing complexity
  - Operational overhead
  - Requires DevOps maturity

implementation_considerations:
  - Service discovery mechanism
  - API gateway for client communication
  - Distributed tracing and monitoring
  - Centralized logging
  - Configuration management
  - Circuit breakers for resilience
  - Database per service pattern

related_patterns:
  - API Gateway
  - Service Registry
  - Circuit Breaker
  - Event-Driven Architecture
  - CQRS

example_technologies:
  - Container orchestration: Kubernetes, Docker Swarm
  - Service mesh: Istio, Linkerd
  - API gateway: Kong, AWS API Gateway
  - Service discovery: Consul, Eureka
  - Messaging: Kafka, RabbitMQ
```

### System Design Generator

**Design Templates:**
- **E-commerce Platform** - Scalable online shopping system
- **Social Media Platform** - High-traffic user-generated content
- **Streaming Service** - Video/audio content delivery
- **Financial System** - High-consistency transactional system
- **IoT Platform** - Real-time device data processing
- **Analytics Platform** - Big data processing and visualization
- **SaaS Application** - Multi-tenant cloud application
- **Gaming Platform** - Real-time multiplayer system

**Generation Features:**
```bash
# Generate architecture design
python scripts/architecture_generator.py design e-commerce \
  --scale high \
  --users 10M \
  --regions multi \
  --with-diagrams \
  --format c4-model

# Generate ADR (Architecture Decision Record)
python scripts/architecture_generator.py adr \
  --title "Database selection for order service" \
  --context "Need ACID compliance and high write throughput" \
  --options postgres,mongodb,dynamodb \
  --decision postgres

# Generate system diagram
python scripts/architecture_generator.py diagram \
  --type component \
  --system e-commerce \
  --format mermaid

# Evaluate architecture
python scripts/architecture_generator.py evaluate \
  --design architecture.yaml \
  --criteria scalability,security,cost,maintainability
```

**Generated Architecture Design:**
```yaml
# architecture/e-commerce-platform.yaml

system:
  name: E-Commerce Platform
  description: Scalable online shopping platform
  scale:
    users: 10M
    requests_per_second: 50000
    data_volume: 100TB
    regions: multi-region

quality_attributes:
  availability: 99.99%
  latency_p95: 200ms
  throughput: 50000 req/s
  scalability: horizontal
  consistency: eventual (with strong where needed)

components:
  # Frontend
  - name: Web Application
    type: SPA
    technology: React, Next.js
    deployment: CDN, Edge Computing
    scaling: Global CDN

  - name: Mobile Apps
    type: Native
    technology: React Native
    features:
      - Offline support
      - Push notifications

  # API Layer
  - name: API Gateway
    type: Gateway
    technology: Kong, AWS API Gateway
    responsibilities:
      - Request routing
      - Authentication
      - Rate limiting
      - Request/response transformation
    scaling: Auto-scaling

  # Services (Microservices)
  - name: User Service
    type: Microservice
    responsibilities:
      - User registration/authentication
      - Profile management
      - User preferences
    technology: Node.js, Express
    database: PostgreSQL (user data)
    caching: Redis (sessions, profiles)
    scaling: Horizontal
    instances_min: 3
    instances_max: 20

  - name: Product Catalog Service
    type: Microservice
    responsibilities:
      - Product information
      - Search and filtering
      - Recommendations
    technology: Java, Spring Boot
    database: MongoDB (product catalog)
    search: Elasticsearch
    caching: Redis (hot products)
    scaling: Horizontal
    instances_min: 5
    instances_max: 30

  - name: Order Service
    type: Microservice
    responsibilities:
      - Order creation
      - Order management
      - Order history
    technology: Go
    database: PostgreSQL (orders)
    messaging: Kafka (order events)
    pattern: Event Sourcing
    scaling: Horizontal
    instances_min: 5
    instances_max: 40

  - name: Payment Service
    type: Microservice
    responsibilities:
      - Payment processing
      - Payment gateway integration
      - Transaction management
    technology: Java, Spring Boot
    database: PostgreSQL (transactions)
    consistency: Strong (ACID)
    security:
      - PCI DSS compliance
      - Encryption at rest/transit
    scaling: Horizontal
    instances_min: 3
    instances_max: 15

  - name: Inventory Service
    type: Microservice
    responsibilities:
      - Stock management
      - Availability checking
      - Reservation system
    technology: Python, FastAPI
    database: PostgreSQL (inventory)
    caching: Redis (stock levels)
    scaling: Horizontal
    instances_min: 3
    instances_max: 20

  - name: Notification Service
    type: Microservice
    responsibilities:
      - Email notifications
      - SMS notifications
      - Push notifications
    technology: Node.js
    messaging: RabbitMQ (notification queue)
    integrations:
      - SendGrid (email)
      - Twilio (SMS)
      - FCM (push)
    scaling: Horizontal

  # Data Layer
  - name: Primary Databases
    type: Database Cluster
    technology: PostgreSQL
    configuration:
      - Master-slave replication
      - Read replicas per region
      - Automated backups
      - Point-in-time recovery

  - name: Document Store
    type: NoSQL Database
    technology: MongoDB
    configuration:
      - Sharded cluster
      - Replica sets
      - Geographic distribution

  - name: Cache Layer
    type: Cache
    technology: Redis Cluster
    use_cases:
      - Session storage
      - Product catalog cache
      - API response cache
    eviction_policy: LRU

  - name: Search Engine
    type: Search
    technology: Elasticsearch
    use_cases:
      - Product search
      - Auto-complete
      - Faceted search
    scaling: Cluster with multiple nodes

  # Messaging
  - name: Event Bus
    type: Message Broker
    technology: Apache Kafka
    topics:
      - order.created
      - order.completed
      - payment.processed
      - inventory.updated
    partitions: 10 per topic
    replication: 3

  # Storage
  - name: Object Storage
    type: Object Store
    technology: AWS S3, CloudFront CDN
    use_cases:
      - Product images
      - User uploads
      - Static assets

  # Observability
  - name: Logging
    type: Centralized Logging
    technology: ELK Stack (Elasticsearch, Logstash, Kibana)

  - name: Monitoring
    type: Metrics and Monitoring
    technology: Prometheus, Grafana
    metrics:
      - Application metrics
      - Infrastructure metrics
      - Business metrics

  - name: Tracing
    type: Distributed Tracing
    technology: Jaeger, OpenTelemetry
    sampling_rate: 10%

integration_patterns:
  - pattern: API Gateway
    purpose: Single entry point for clients

  - pattern: Service Discovery
    technology: Consul
    purpose: Dynamic service location

  - pattern: Circuit Breaker
    technology: Hystrix, Resilience4j
    purpose: Fault tolerance

  - pattern: Saga Pattern
    use_case: Distributed transactions (order processing)
    implementation: Choreography with Kafka

  - pattern: CQRS
    use_case: Product catalog (read-heavy)
    implementation: Separate read/write models

data_management:
  - pattern: Database per Service
    rationale: Service autonomy and independence

  - pattern: Event Sourcing
    services: [Order Service]
    rationale: Audit trail and state reconstruction

  - pattern: CQRS
    services: [Product Catalog Service]
    rationale: Optimize read and write separately

  - consistency: Eventual Consistency
    rationale: High availability and scalability
    exceptions: [Payment Service] # Strong consistency

security:
  - Authentication: OAuth 2.0, JWT
  - Authorization: RBAC (Role-Based Access Control)
  - API Security: Rate limiting, API keys
  - Data Encryption: TLS 1.3, AES-256
  - Secrets Management: AWS Secrets Manager, Vault
  - Network Security: VPC, Security Groups, WAF
  - Compliance: PCI DSS (payment), GDPR (user data)

deployment:
  - platform: Kubernetes (EKS, GKE, AKS)
  - ci_cd: GitLab CI, GitHub Actions
  - infrastructure_as_code: Terraform
  - configuration: Kubernetes ConfigMaps, Secrets
  - service_mesh: Istio (traffic management, security)

disaster_recovery:
  - rpo: 15 minutes (Recovery Point Objective)
  - rto: 1 hour (Recovery Time Objective)
  - backup_strategy: Automated daily backups, continuous replication
  - multi_region: Active-active in primary regions, passive in DR region
  - failover: Automated DNS failover

cost_optimization:
  - Auto-scaling based on demand
  - Reserved instances for baseline capacity
  - Spot instances for batch workloads
  - CDN for static content
  - Cache to reduce database load
  - Right-sizing of resources

scalability_strategy:
  - horizontal_scaling: All services
  - database_scaling: Read replicas, sharding
  - cache_scaling: Redis cluster
  - cdn: Global edge locations
  - load_balancing: ALB/NLB with health checks
```

### Architecture Decision Records (ADR)

**ADR Template:**
```markdown
# ADR-001: Database Selection for Order Service

## Status
Accepted

## Context
The order service requires a database solution that can handle:
- High write throughput (10,000 orders/minute at peak)
- ACID transactions for order consistency
- Complex queries for order history and analytics
- Strong consistency for order state
- Support for event sourcing pattern

Options Considered:
1. PostgreSQL
2. MongoDB
3. DynamoDB

## Decision
We will use PostgreSQL as the primary database for the Order Service.

## Rationale

### PostgreSQL (Selected)
**Pros:**
- Full ACID compliance for transactional consistency
- Mature and stable with extensive community support
- Strong support for complex queries and joins
- Excellent JSON support for flexible schemas
- Built-in replication and high availability
- Proven scalability for write-heavy workloads
- Open source with no vendor lock-in

**Cons:**
- Requires more operational expertise than managed NoSQL
- Horizontal scaling more complex than DynamoDB
- License: PostgreSQL (permissive)

### MongoDB
**Pros:**
- Flexible schema design
- Good horizontal scalability
- Strong developer ecosystem

**Cons:**
- Limited ACID transaction support across documents
- Eventual consistency model not suitable for orders
- Higher operational complexity for consistency guarantees

### DynamoDB
**Pros:**
- Fully managed with automatic scaling
- Very low latency
- Good fit for simple key-value access

**Cons:**
- Vendor lock-in (AWS only)
- Complex pricing model
- Limited query flexibility
- Difficult to implement complex event sourcing patterns
- Higher costs for transactional consistency

## Consequences

### Positive
- Strong consistency guarantees for order integrity
- Mature tooling and ecosystem
- Team expertise in PostgreSQL
- Flexible query capabilities for analytics
- Support for event sourcing with JSONB

### Negative
- Need to implement sharding strategy for long-term scalability
- Requires dedicated DBA expertise
- More complex backup/recovery compared to managed services

### Neutral
- Standard SQL knowledge applies
- Well-documented migration paths if needed

## Implementation Details
- Use PostgreSQL 15+ for latest features
- Implement read replicas for read scalability
- Use connection pooling (PgBouncer)
- Partition tables by date for order history
- Implement automated backups with point-in-time recovery
- Monitor query performance with pg_stat_statements

## References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Event Sourcing with PostgreSQL](https://example.com)
- Internal benchmark results: `docs/benchmarks/order-db.md`

## Review History
- 2024-01-15: Proposed by @architect
- 2024-01-18: Reviewed by engineering team
- 2024-01-20: Accepted by tech leadership
```

### Architecture Evaluation Framework

**Evaluation Criteria:**
```python
# architecture_evaluator.py
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class QualityAttribute(Enum):
    SCALABILITY = "scalability"
    PERFORMANCE = "performance"
    AVAILABILITY = "availability"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    COST = "cost"
    RELIABILITY = "reliability"
    TESTABILITY = "testability"

@dataclass
class EvaluationCriteria:
    attribute: QualityAttribute
    weight: float  # 0.0 to 1.0
    threshold: float  # Minimum acceptable score

@dataclass
class ArchitectureEvaluation:
    architecture_name: str
    scores: Dict[QualityAttribute, float]
    weighted_score: float
    passed: bool
    recommendations: List[str]

class ArchitectureEvaluator:
    """Evaluate architecture against quality attributes"""

    def __init__(self, criteria: List[EvaluationCriteria]):
        self.criteria = criteria

    def evaluate(self, architecture: Dict) -> ArchitectureEvaluation:
        """Evaluate architecture design"""

        scores = {}

        # Evaluate each quality attribute
        scores[QualityAttribute.SCALABILITY] = self._evaluate_scalability(architecture)
        scores[QualityAttribute.PERFORMANCE] = self._evaluate_performance(architecture)
        scores[QualityAttribute.AVAILABILITY] = self._evaluate_availability(architecture)
        scores[QualityAttribute.SECURITY] = self._evaluate_security(architecture)
        scores[QualityAttribute.MAINTAINABILITY] = self._evaluate_maintainability(architecture)
        scores[QualityAttribute.COST] = self._evaluate_cost(architecture)

        # Calculate weighted score
        weighted_score = self._calculate_weighted_score(scores)

        # Check if all thresholds are met
        passed = self._check_thresholds(scores)

        # Generate recommendations
        recommendations = self._generate_recommendations(scores, architecture)

        return ArchitectureEvaluation(
            architecture_name=architecture['system']['name'],
            scores=scores,
            weighted_score=weighted_score,
            passed=passed,
            recommendations=recommendations
        )

    def _evaluate_scalability(self, architecture: Dict) -> float:
        """Evaluate scalability (0.0 to 1.0)"""
        score = 0.0

        # Check horizontal scaling
        if any('horizontal' in str(c.get('scaling', '')).lower()
               for c in architecture.get('components', [])):
            score += 0.3

        # Check auto-scaling
        if any('auto-scaling' in str(c).lower()
               for c in architecture.get('components', [])):
            score += 0.2

        # Check database scaling strategy
        if 'read replicas' in str(architecture.get('data_management', '')).lower():
            score += 0.2

        # Check caching
        if any('cache' in str(c.get('type', '')).lower()
               for c in architecture.get('components', [])):
            score += 0.15

        # Check load balancing
        if 'load_balancing' in architecture.get('scalability_strategy', {}):
            score += 0.15

        return min(score, 1.0)

    def _evaluate_performance(self, architecture: Dict) -> float:
        """Evaluate performance characteristics"""
        score = 0.0

        quality_attrs = architecture.get('quality_attributes', {})

        # Check latency target
        latency = quality_attrs.get('latency_p95', '1000ms')
        if '200ms' in latency:
            score += 0.3
        elif '500ms' in latency:
            score += 0.2

        # Check CDN usage
        if any('cdn' in str(c).lower() for c in architecture.get('components', [])):
            score += 0.2

        # Check caching strategy
        cache_components = [c for c in architecture.get('components', [])
                           if 'cache' in str(c.get('type', '')).lower()]
        if len(cache_components) > 0:
            score += 0.2

        # Check async processing
        if any('kafka' in str(c).lower() or 'rabbitmq' in str(c).lower()
               for c in architecture.get('components', [])):
            score += 0.15

        # Check database optimization
        if 'index' in str(architecture.get('data_management', '')).lower():
            score += 0.15

        return min(score, 1.0)

    def _evaluate_availability(self, architecture: Dict) -> float:
        """Evaluate availability and resilience"""
        score = 0.0

        quality_attrs = architecture.get('quality_attributes', {})

        # Check availability target
        availability = quality_attrs.get('availability', '0')
        if '99.99' in availability or '99.999' in availability:
            score += 0.3
        elif '99.9' in availability:
            score += 0.2

        # Check multi-region deployment
        if architecture.get('system', {}).get('scale', {}).get('regions') == 'multi-region':
            score += 0.2

        # Check disaster recovery
        if 'disaster_recovery' in architecture:
            score += 0.2

        # Check circuit breaker pattern
        patterns = architecture.get('integration_patterns', [])
        if any('circuit breaker' in str(p).lower() for p in patterns):
            score += 0.15

        # Check health checks and monitoring
        if any('monitoring' in str(c.get('name', '')).lower()
               for c in architecture.get('components', [])):
            score += 0.15

        return min(score, 1.0)

    def _evaluate_security(self, architecture: Dict) -> float:
        """Evaluate security measures"""
        score = 0.0

        security = architecture.get('security', {})

        # Check authentication
        if 'Authentication' in security or 'authentication' in str(security).lower():
            score += 0.2

        # Check authorization
        if 'Authorization' in security or 'rbac' in str(security).lower():
            score += 0.2

        # Check encryption
        if 'encryption' in str(security).lower():
            score += 0.2

        # Check API security
        if 'api security' in str(security).lower() or 'rate limiting' in str(security).lower():
            score += 0.15

        # Check compliance
        if 'compliance' in str(security).lower():
            score += 0.15

        # Check secrets management
        if 'secrets' in str(security).lower():
            score += 0.1

        return min(score, 1.0)

    def _evaluate_maintainability(self, architecture: Dict) -> float:
        """Evaluate maintainability"""
        score = 0.0

        # Check microservices architecture
        if any('microservice' in str(c.get('type', '')).lower()
               for c in architecture.get('components', [])):
            score += 0.25

        # Check observability (logging, monitoring, tracing)
        observability_components = [
            c for c in architecture.get('components', [])
            if any(term in str(c.get('name', '')).lower()
                  for term in ['logging', 'monitoring', 'tracing'])
        ]
        if len(observability_components) >= 3:
            score += 0.3
        elif len(observability_components) >= 2:
            score += 0.2

        # Check CI/CD
        if 'ci_cd' in architecture.get('deployment', {}):
            score += 0.2

        # Check IaC (Infrastructure as Code)
        if 'infrastructure_as_code' in architecture.get('deployment', {}):
            score += 0.15

        # Check documentation
        if architecture.get('system', {}).get('description'):
            score += 0.1

        return min(score, 1.0)

    def _evaluate_cost(self, architecture: Dict) -> float:
        """Evaluate cost optimization"""
        score = 0.5  # Baseline

        cost_opt = architecture.get('cost_optimization', {})

        if not cost_opt:
            return 0.5

        # Check auto-scaling (cost optimization)
        if 'auto-scaling' in str(cost_opt).lower():
            score += 0.15

        # Check caching (reduces compute/DB costs)
        if 'cache' in str(cost_opt).lower():
            score += 0.1

        # Check CDN usage
        if 'cdn' in str(cost_opt).lower():
            score += 0.1

        # Check reserved instances
        if 'reserved' in str(cost_opt).lower():
            score += 0.1

        # Check right-sizing
        if 'right-sizing' in str(cost_opt).lower():
            score += 0.05

        return min(score, 1.0)

    def _calculate_weighted_score(self, scores: Dict[QualityAttribute, float]) -> float:
        """Calculate weighted average score"""
        total_weight = sum(c.weight for c in self.criteria)
        weighted_sum = sum(
            scores.get(c.attribute, 0.0) * c.weight
            for c in self.criteria
        )
        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _check_thresholds(self, scores: Dict[QualityAttribute, float]) -> bool:
        """Check if all thresholds are met"""
        for criteria in self.criteria:
            if scores.get(criteria.attribute, 0.0) < criteria.threshold:
                return False
        return True

    def _generate_recommendations(
        self,
        scores: Dict[QualityAttribute, float],
        architecture: Dict
    ) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []

        for criteria in self.criteria:
            score = scores.get(criteria.attribute, 0.0)
            if score < criteria.threshold:
                recommendations.append(
                    f"Improve {criteria.attribute.value}: "
                    f"Current score {score:.2f} is below threshold {criteria.threshold:.2f}"
                )

        # Specific recommendations based on scores
        if scores.get(QualityAttribute.SCALABILITY, 1.0) < 0.7:
            recommendations.append(
                "Consider implementing horizontal scaling and caching strategies"
            )

        if scores.get(QualityAttribute.SECURITY, 1.0) < 0.7:
            recommendations.append(
                "Enhance security with encryption, authentication, and authorization"
            )

        if scores.get(QualityAttribute.AVAILABILITY, 1.0) < 0.7:
            recommendations.append(
                "Improve availability with multi-region deployment and circuit breakers"
            )

        return recommendations
```

## Technical Details

### Architectural Patterns

**Microservices Communication:**
- Synchronous: REST, gRPC
- Asynchronous: Message queues, Event streams
- Service mesh for advanced traffic management

**Data Management Patterns:**
- Database per service
- Shared database (anti-pattern, but sometimes necessary)
- Saga pattern for distributed transactions
- Event sourcing for audit and state management
- CQRS for read/write optimization

**Resilience Patterns:**
- Circuit breaker
- Retry with exponential backoff
- Bulkhead
- Timeout
- Fallback

## Best Practices

**Do:**
- Document architectural decisions (ADRs)
- Consider non-functional requirements early
- Design for failure
- Implement observability from the start
- Use proven patterns and avoid over-engineering
- Consider team structure (Conway's Law)
- Plan for evolution and change
- Evaluate tradeoffs explicitly

**Don't:**
- Copy architectures without understanding context
- Ignore operational complexity
- Over-engineer for hypothetical scale
- Neglect security until later
- Forget about cost implications
- Skip proof-of-concepts for critical decisions
- Ignore team capabilities and learning curve

## Integration Points

This skill integrates with:
- **Diagramming:** C4 Model, UML, ArchiMate, Mermaid
- **Documentation:** Confluence, Notion, Architecture Decision Records
- **Modeling:** Enterprise Architect, Sparx, draw.io, Lucidchart
- **Cloud Platforms:** AWS, GCP, Azure, Kubernetes
- **Evaluation:** ArchUnit, Fitness Functions
- **Standards:** ISO 25010, TOGAF, Zachman Framework

## Common Challenges and Solutions

### Challenge: Choosing Between Monolith and Microservices
**Solution:** Start with modular monolith, evaluate team size and operational maturity, consider domain complexity, plan migration path if needed, use strangler fig pattern for gradual migration

### Challenge: Ensuring Data Consistency in Distributed Systems
**Solution:** Use saga pattern for orchestration, implement event sourcing where appropriate, accept eventual consistency where possible, use strong consistency only where necessary (payments, inventory)

### Challenge: Managing Architectural Complexity
**Solution:** Document decisions with ADRs, use C4 model for visualization, implement observability, maintain architecture diagrams, conduct regular architecture reviews, enforce boundaries with fitness functions

### Challenge: Balancing Quality Attributes
**Solution:** Explicitly identify quality attribute priorities, use architecture tradeoff analysis, create quality attribute scenarios, implement fitness functions, measure and monitor continuously

### Challenge: Technology Selection
**Solution:** Evaluate against specific criteria, conduct proof-of-concepts, consider total cost of ownership, assess team expertise, check community and vendor support, plan for migration if needed

### Challenge: Scalability Planning
**Solution:** Identify bottlenecks early, implement horizontal scaling, use caching strategically, implement async processing, plan for database scaling, load test regularly, monitor performance metrics
