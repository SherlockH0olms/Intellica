# Intellica - System Architecture

## Table of Contents
1. [Overview](#overview)
2. [System Components](#system-components)
3. [Data Flow](#data-flow)
4. [Technology Stack](#technology-stack)
5. [Deployment Architecture](#deployment-architecture)

---

## Overview

Intelica is a microservices-based platform designed for real-time industrial equipment monitoring, predictive maintenance, and AI-driven optimization.

### Architecture Diagram

```
┌──────────────────────────────────────────────────┐
│                PRESENTATION LAYER                      │
│  ┌──────────────┐  ┌──────────────┐              │
│  │  Web Dashboard  │  │  Mobile App   │              │
│  │  (React + TS)   │  │ (React Native)│              │
│  └──────────────┘  └──────────────┘              │
└────────────────────────┬─────────────────────────┘
                         │ REST API + WebSocket
                         │
┌────────────────────────┴─────────────────────────┐
│                APPLICATION LAYER                       │
│  ┌─────────────────────────────────────┐         │
│  │        FastAPI Backend             │         │
│  │  - REST API Endpoints              │         │
│  │  - WebSocket Server                │         │
│  │  - Business Logic                  │         │
│  │  - Authentication & Authorization  │         │
│  └─────────────────────────────────────┘         │
└────────────────────────┬─────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────┐
│                   AI/ML LAYER                          │
│  ┌─────────────────────────────────────┐         │
│  │  - Anomaly Detection (Isolation F.) │         │
│  │  - Predictive Maintenance (RF)      │         │
│  │  - Config Optimization (Bayesian)   │         │
│  │  - Defect Detection (MobileNetV2)   │         │
│  └─────────────────────────────────────┘         │
└────────────────────────┬─────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────┐
│                   DATA LAYER                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────┐  │
│  │ TimescaleDB │ │ PostgreSQL  │ │  Redis  │  │
│  │(Time-series)│ │ (Relational)│ │ (Cache) │  │
│  └─────────────┘ └─────────────┘ └─────────┘  │
└────────────────────────┬─────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────┐
│              INTEGRATION LAYER                        │
│  ┌────────┐ ┌────────┐ ┌───────────┐      │
│  │  MQTT  │ │ OPC-UA │ │ Modbus TCP │      │
│  └────────┘ └────────┘ └───────────┘      │
└────────────────────────┬─────────────────────────┘
                         │ Sensor Data
┌────────────────────────┴─────────────────────────┐
│                PHYSICAL LAYER                          │
│  ┌─────────┐ ┌─────────┐ ┌──────────┐     │
│  │   CNC   │ │Injection│ │ Conveyor  │     │
│  │ Machine │ │ Molding │ │   System  │     │
│  └─────────┘ └─────────┘ └──────────┘     │
└──────────────────────────────────────────────────┘
```

---

## System Components

### 1. Frontend (Presentation Layer)
**Technology**: React 18 + TypeScript + Vite

**Components**:
- Factory Overview Dashboard
- Machine Detail Pages
- Defect Detection Interface
- Analytics & Reports
- Real-time Alerts Feed

**Key Features**:
- WebSocket connection for real-time updates
- SVG-based factory floor visualization
- Interactive charts (Chart.js, Recharts)
- Material-UI components

### 2. Backend (Application Layer)
**Technology**: FastAPI (Python 3.11)

**Modules**:
- **API v1**: RESTful endpoints
  - `/machines` - Machine management
  - `/sensors` - Sensor data ingestion
  - `/recommendations` - AI recommendations
  - `/defects` - Defect detection
  - `/analytics` - Analytics data
  
- **WebSocket Server**: Real-time data streaming

- **Authentication**: JWT-based auth

### 3. AI/ML Layer
**Models**:

#### Anomaly Detection
- **Algorithm**: Isolation Forest
- **Accuracy**: 96%
- **Input**: Multi-dimensional sensor data
- **Output**: Anomaly score + classification

#### Predictive Maintenance
- **Algorithm**: Random Forest Classifier
- **F1-Score**: 0.84
- **Prediction Window**: 7 days
- **Features**: Temperature, vibration, torque, tool wear

#### Configuration Optimization
- **Algorithm**: Bayesian Optimization
- **Objective**: Multi-objective (defect rate, energy, cycle time)

#### Defect Detection
- **Model**: MobileNetV2 (Transfer Learning)
- **Accuracy**: 94%
- **Classes**: normal, crack, scratch, deformation, contamination

### 4. Data Layer

#### TimescaleDB
- **Purpose**: Time-series sensor data
- **Features**:
  - Hypertables for automatic partitioning
  - Continuous aggregates (5-min, 1-hour)
  - Compression (70-90% size reduction)
  - Retention policies

#### PostgreSQL
- **Purpose**: Relational data
- **Tables**: machines, alerts, defects, config_history, users

#### Redis
- **Purpose**: Caching + Real-time data
- **Use Cases**:
  - Latest sensor readings (TTL: 5 min)
  - Active alerts (sorted set)
  - Session management

### 5. Integration Layer

#### MQTT (RabbitMQ)
- **Topic Structure**: `factory/{machine_type}/{machine_id}/sensors`
- **QoS**: 1 (At least once)

#### OPC-UA
- **Library**: asyncua
- **Use Case**: Injection Molding machines

#### Modbus TCP
- **Library**: pymodbus
- **Use Case**: PLCs, Conveyors

---

## Data Flow

### 1. Sensor Data Ingestion
```
Machine Sensors → Protocol Gateway (MQTT/OPC-UA/Modbus) → 
RabbitMQ → Backend Consumer → TimescaleDB + Redis
```

### 2. Real-time Monitoring
```
TimescaleDB → Backend API → WebSocket → Frontend Dashboard
```

### 3. AI Processing
```
Sensor Data → ML Service → Anomaly/Prediction → Alert → 
Dashboard + Notification
```

### 4. Human-in-the-Loop
```
AI Recommendation → Dashboard Display → Operator Approval → 
Config Change → Machine Update
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|--------|
| **Frontend** | React 18 + TypeScript | UI framework |
| | Redux Toolkit | State management |
| | Material-UI | Component library |
| | Chart.js / Recharts | Data visualization |
| | Socket.IO | Real-time communication |
| **Backend** | FastAPI | Web framework |
| | Uvicorn | ASGI server |
| | SQLAlchemy | ORM |
| | Alembic | Database migrations |
| | Pydantic | Data validation |
| **ML/AI** | scikit-learn | Traditional ML |
| | TensorFlow | Deep learning |
| | NumPy / Pandas | Data processing |
| | OpenCV | Computer vision |
| **Database** | TimescaleDB | Time-series data |
| | PostgreSQL | Relational data |
| | Redis | Caching |
| **Messaging** | RabbitMQ | Message broker |
| | MQTT | IoT protocol |
| **DevOps** | Docker | Containerization |
| | Docker Compose | Orchestration |
| | GitHub Actions | CI/CD |

---

## Deployment Architecture

### Docker Compose (Development)
```yaml
Services:
  - timescaledb: Database (port 5432)
  - redis: Cache (port 6379)
  - rabbitmq: Message broker (ports 5672, 1883, 15672)
  - backend: FastAPI app (port 8000)
  - frontend: React app (port 3000)
  - simulator: Data generator
```

### Production Considerations
1. **Load Balancing**: Nginx + multiple backend instances
2. **High Availability**: Database replication
3. **Monitoring**: Prometheus + Grafana
4. **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
5. **Security**: TLS/SSL, API rate limiting, authentication

---

## Security

### Authentication & Authorization
- JWT tokens (15-min expiry + refresh tokens)
- Role-based access control (Admin, Operator, Viewer)

### Data Security
- TLS 1.3 for in-transit encryption
- PostgreSQL encryption at rest
- API input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)

### Network Security
- CORS whitelisting
- API rate limiting (100 req/min per user)
- Firewall rules

---

## Performance Optimization

### Database
- TimescaleDB hypertables + continuous aggregates
- PostgreSQL indexes on frequently queried columns
- Redis caching (30s TTL for real-time data)

### API
- Async/await for I/O operations
- Connection pooling
- Pagination for large datasets

### ML Models
- Model quantization (TensorFlow Lite)
- Batch inference
- Caching of model predictions

---

## Scalability

### Horizontal Scaling
- Stateless backend services
- Load balancer distribution
- Database read replicas

### Vertical Scaling
- Increase container resources
- Optimize queries
- Model optimization

---

## Monitoring & Observability

### Metrics
- API response times
- Database query performance
- ML model inference latency
- Error rates

### Logging
- Structured logs (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized log aggregation

### Alerting
- System health checks
- Database connection failures
- ML model performance degradation

---

For implementation details, see the codebase in `/backend` and `/frontend` directories.