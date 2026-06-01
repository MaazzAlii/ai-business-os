# AI Business OS - Architecture

## System Overview

The AI Business OS is a modular business automation platform combining workflow automation, AI capabilities, and data management.

## Architecture Components

### 1. Automation Layer (n8n)
- **Purpose**: Workflow orchestration and business process automation
- **Responsibilities**:
  - Invoice processing triggers
  - Data synchronization
  - Email/notification automation
  - Third-party API integrations
- **Location**: `/n8n-workflows`

### 2. Backend API (FastAPI)
- **Purpose**: Core business logic and data management
- **Responsibilities**:
  - RESTful API endpoints
  - Business logic implementation
  - Database operations
  - Authentication and authorization
- **Location**: `/backend`
- **Key Components**:
  - Invoice processing service
  - Customer management
  - Supplier management
  - Inventory tracking
  - RAG knowledge base integration

### 3. Frontend (Streamlit/React)
- **Purpose**: User interface for business users
- **Responsibilities**:
  - Dashboard visualization
  - Data entry forms
  - Report generation
  - Analytics display
- **Location**: `/frontend`

### 4. Data Layer (PostgreSQL + ChromaDB)
- **Purpose**: Data persistence and knowledge management
- **PostgreSQL**: Structured business data
  - Invoices
  - Customers
  - Suppliers
  - Inventory
- **ChromaDB**: Vector embeddings for RAG
  - Document storage
  - Semantic search
- **Location**: `/database`

### 5. AI Integration (Mistral)
- **Purpose**: Natural language processing and business intelligence
- **Capabilities**:
  - Document understanding (invoices)
  - Business insights generation
  - Customer queries handling
  - Knowledge base generation

## Data Flow

```
n8n (Trigger) → FastAPI (Process) → PostgreSQL (Store)
                    ↓
                ChromaDB (Index)
                    ↓
              Mistral AI (Analyze)
                    ↓
              Streamlit (Display)
```

## Deployment Architecture

- Docker containerization
- PostgreSQL database server
- n8n automation server
- FastAPI backend service
- Streamlit frontend
- ChromaDB service for embeddings

## Security Considerations

- Environment variable-based configuration
- Authentication tokens
- Rate limiting on API endpoints
- Database encryption
- Secure credential storage
