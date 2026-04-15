# Backend Development (Senior Backend Developer)

## Overview

The Backend Development skill provides comprehensive tools and frameworks for building scalable, performant server-side applications using Node.js, Go, and Python. This skill enables backend engineers to create robust APIs, microservices, and distributed systems with best practices for security, performance, and maintainability. It combines API scaffolding, database design, authentication systems, and deployment automation with deep expertise in backend architectures and system design patterns.

## Who Should Use This Skill

- **Backend Engineers** building server-side applications
- **Senior Backend Developers** architecting backend systems
- **API Developers** creating RESTful and GraphQL APIs
- **Microservices Engineers** building distributed systems
- **Platform Engineers** developing internal platforms
- **Fullstack Engineers** working on the backend layer
- **DevOps Engineers** optimizing backend infrastructure
- **Tech Leads** establishing backend standards

## Purpose and Use Cases

Use this skill when you need to:
- Build RESTful APIs and GraphQL endpoints
- Create microservices architectures
- Implement authentication and authorization
- Design database schemas and queries
- Build real-time applications with WebSockets
- Implement caching and performance optimization
- Create background job processing systems
- Build event-driven architectures
- Implement API rate limiting and throttling
- Create serverless functions
- Build message queue systems
- Implement payment integrations

**Keywords that trigger this skill:** backend, API, Node.js, Go, Python, Express, FastAPI, microservices, REST, GraphQL, database, authentication, server-side, endpoints

## What's Included

### API Scaffolder

**API Templates:**
- **REST API** - Express, FastAPI, Gin, Chi
- **GraphQL API** - Apollo Server, Hasura, GraphQL-Go
- **gRPC Service** - Protocol buffers, streaming
- **WebSocket Server** - Socket.io, Gorilla WebSocket
- **Serverless Functions** - AWS Lambda, Vercel, Cloudflare Workers
- **Microservice** - Complete service with database and messaging
- **CRUD API** - Full CRUD operations with validation
- **Authentication Service** - JWT, OAuth2, session management

**Generation Features:**
```bash
# Generate REST API with Express
python scripts/api_scaffolder.py rest-api user-service \
  --language node \
  --framework express \
  --database postgres \
  --with-auth jwt \
  --with-validation \
  --with-tests

# Generate FastAPI service
python scripts/api_scaffolder.py rest-api product-service \
  --language python \
  --framework fastapi \
  --database mongodb \
  --with-cache redis \
  --with-docs

# Generate Go microservice
python scripts/api_scaffolder.py microservice order-service \
  --language go \
  --framework gin \
  --database postgres \
  --messaging rabbitmq \
  --with-metrics \
  --with-tracing

# Generate GraphQL API
python scripts/api_scaffolder.py graphql-api \
  --language node \
  --database postgres \
  --with-subscriptions \
  --with-dataloader
```

**Generated API Structure (Express):**
```javascript
// src/server.js
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import { config } from './config/config.js';
import { errorHandler } from './middleware/errorHandler.js';
import { requestLogger } from './middleware/logger.js';
import routes from './routes/index.js';
import { connectDatabase } from './config/database.js';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors(config.cors));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Compression
app.use(compression());

// Logging
app.use(requestLogger);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// API routes
app.use('/api/v1', routes);

// Error handling
app.use(errorHandler);

// Start server
const startServer = async () => {
  try {
    await connectDatabase();

    const PORT = config.port || 3000;
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
};

startServer();

// src/routes/users.js
import express from 'express';
import { authenticate } from '../middleware/auth.js';
import { validate } from '../middleware/validator.js';
import { userSchema } from '../schemas/user.js';
import * as userController from '../controllers/user.js';

const router = express.Router();

// Public routes
router.post('/register', validate(userSchema.register), userController.register);
router.post('/login', validate(userSchema.login), userController.login);

// Protected routes
router.use(authenticate);

router.get('/', userController.getUsers);
router.get('/:id', userController.getUserById);
router.put('/:id', validate(userSchema.update), userController.updateUser);
router.delete('/:id', userController.deleteUser);

export default router;

// src/controllers/user.js
import { UserService } from '../services/user.js';
import { ApiError } from '../utils/ApiError.js';
import { asyncHandler } from '../utils/asyncHandler.js';

const userService = new UserService();

export const register = asyncHandler(async (req, res) => {
  const user = await userService.createUser(req.body);
  res.status(201).json({
    success: true,
    data: user,
  });
});

export const login = asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  const { user, token } = await userService.authenticateUser(email, password);

  res.json({
    success: true,
    data: { user, token },
  });
});

export const getUsers = asyncHandler(async (req, res) => {
  const { page = 1, limit = 10, search } = req.query;
  const result = await userService.getUsers({ page, limit, search });

  res.json({
    success: true,
    data: result.users,
    pagination: {
      page: result.page,
      limit: result.limit,
      total: result.total,
      pages: result.pages,
    },
  });
});

export const getUserById = asyncHandler(async (req, res) => {
  const user = await userService.getUserById(req.params.id);

  if (!user) {
    throw new ApiError(404, 'User not found');
  }

  res.json({
    success: true,
    data: user,
  });
});

export const updateUser = asyncHandler(async (req, res) => {
  const user = await userService.updateUser(req.params.id, req.body);

  res.json({
    success: true,
    data: user,
  });
});

export const deleteUser = asyncHandler(async (req, res) => {
  await userService.deleteUser(req.params.id);

  res.json({
    success: true,
    message: 'User deleted successfully',
  });
});

// src/services/user.js
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { UserRepository } from '../repositories/user.js';
import { ApiError } from '../utils/ApiError.js';
import { config } from '../config/config.js';

export class UserService {
  constructor() {
    this.userRepo = new UserRepository();
  }

  async createUser(userData) {
    // Check if user exists
    const existingUser = await this.userRepo.findByEmail(userData.email);
    if (existingUser) {
      throw new ApiError(400, 'User already exists');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(userData.password, 10);

    // Create user
    const user = await this.userRepo.create({
      ...userData,
      password: hashedPassword,
    });

    // Remove password from response
    delete user.password;
    return user;
  }

  async authenticateUser(email, password) {
    const user = await this.userRepo.findByEmail(email);

    if (!user) {
      throw new ApiError(401, 'Invalid credentials');
    }

    const isValidPassword = await bcrypt.compare(password, user.password);

    if (!isValidPassword) {
      throw new ApiError(401, 'Invalid credentials');
    }

    // Generate JWT
    const token = jwt.sign(
      { id: user.id, email: user.email },
      config.jwt.secret,
      { expiresIn: config.jwt.expiresIn }
    );

    delete user.password;
    return { user, token };
  }

  async getUsers({ page, limit, search }) {
    const offset = (page - 1) * limit;
    const { users, total } = await this.userRepo.findAll({
      offset,
      limit,
      search,
    });

    return {
      users,
      page: parseInt(page),
      limit: parseInt(limit),
      total,
      pages: Math.ceil(total / limit),
    };
  }

  async getUserById(id) {
    const user = await this.userRepo.findById(id);
    if (user) {
      delete user.password;
    }
    return user;
  }

  async updateUser(id, updates) {
    // If password is being updated, hash it
    if (updates.password) {
      updates.password = await bcrypt.hash(updates.password, 10);
    }

    const user = await this.userRepo.update(id, updates);
    if (user) {
      delete user.password;
    }
    return user;
  }

  async deleteUser(id) {
    return await this.userRepo.delete(id);
  }
}

// src/repositories/user.js
import { db } from '../config/database.js';

export class UserRepository {
  async create(userData) {
    const [user] = await db('users')
      .insert(userData)
      .returning('*');
    return user;
  }

  async findByEmail(email) {
    return await db('users')
      .where({ email })
      .first();
  }

  async findById(id) {
    return await db('users')
      .where({ id })
      .first();
  }

  async findAll({ offset, limit, search }) {
    let query = db('users');

    if (search) {
      query = query.where((builder) => {
        builder
          .where('email', 'like', `%${search}%`)
          .orWhere('name', 'like', `%${search}%`);
      });
    }

    const [{ count: total }] = await query.clone().count('* as count');
    const users = await query
      .offset(offset)
      .limit(limit)
      .orderBy('created_at', 'desc');

    return { users, total: parseInt(total) };
  }

  async update(id, updates) {
    const [user] = await db('users')
      .where({ id })
      .update({ ...updates, updated_at: db.fn.now() })
      .returning('*');
    return user;
  }

  async delete(id) {
    return await db('users')
      .where({ id })
      .delete();
  }
}

// tests/user.test.js
import request from 'supertest';
import app from '../src/server.js';
import { db } from '../src/config/database.js';

describe('User API', () => {
  beforeAll(async () => {
    await db.migrate.latest();
  });

  afterAll(async () => {
    await db.destroy();
  });

  beforeEach(async () => {
    await db('users').truncate();
  });

  describe('POST /api/v1/users/register', () => {
    it('should register a new user', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      const response = await request(app)
        .post('/api/v1/users/register')
        .send(userData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.email).toBe(userData.email);
      expect(response.body.data.password).toBeUndefined();
    });

    it('should not register duplicate email', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      await request(app).post('/api/v1/users/register').send(userData);

      const response = await request(app)
        .post('/api/v1/users/register')
        .send(userData)
        .expect(400);

      expect(response.body.success).toBe(false);
    });
  });

  describe('POST /api/v1/users/login', () => {
    it('should login with valid credentials', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      await request(app).post('/api/v1/users/register').send(userData);

      const response = await request(app)
        .post('/api/v1/users/login')
        .send({ email: userData.email, password: userData.password })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.token).toBeDefined();
      expect(response.body.data.user.email).toBe(userData.email);
    });
  });
});
```

**Generated API Structure (FastAPI):**
```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.config import settings
from app.database import engine, Base
from app.routes import users, auth
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import error_handler

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(LoggingMiddleware)

# Exception handler
app.add_exception_handler(Exception, error_handler)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )

# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.services.user import UserService
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """Create a new user"""
    service = UserService(db)
    user = await service.create_user(user_data)
    return UserResponse.from_orm(user)

@router.get("/", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get list of users with pagination"""
    service = UserService(db)
    result = await service.get_users(page, limit, search)
    return result

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user by ID"""
    service = UserService(db)
    user = await service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user"""
    service = UserService(db)
    user = await service.update_user(user_id, user_data)
    return UserResponse.from_orm(user)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete user"""
    service = UserService(db)
    await service.delete_user(user_id)
    return {"message": "User deleted successfully"}

# app/services/user.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from passlib.context import CryptContext
import math

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        # Check if user exists
        existing_user = self.db.query(User).filter(
            User.email == user_data.email
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash password
        hashed_password = pwd_context.hash(user_data.password)

        # Create user
        user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    async def authenticate_user(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user

    async def get_users(self, page: int, limit: int, search: str = None):
        query = self.db.query(User)

        if search:
            query = query.filter(
                or_(
                    User.email.ilike(f"%{search}%"),
                    User.name.ilike(f"%{search}%")
                )
            )

        total = query.count()
        offset = (page - 1) * limit
        users = query.offset(offset).limit(limit).all()

        return {
            "users": users,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": math.ceil(total / limit),
        }

    async def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_data.dict(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    async def delete_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.db.delete(user)
        self.db.commit()
```

### Database Designer

**Database Design Features:**
- Schema generation from models
- Migration management
- Index optimization
- Query performance analysis
- Database seeding
- Backup and restore utilities
- Connection pooling configuration
- Replication setup

**Usage:**
```bash
# Generate database schema
python scripts/db_designer.py generate-schema \
  --models models/ \
  --database postgres \
  --output migrations/

# Create migration
python scripts/db_designer.py create-migration \
  --name add_user_roles \
  --auto-detect

# Optimize indexes
python scripts/db_designer.py optimize-indexes \
  --analyze-queries logs/queries.log \
  --suggest-indexes

# Generate seed data
python scripts/db_designer.py seed \
  --tables users,products \
  --count 1000
```

### Authentication System

**Authentication Features:**
- JWT authentication
- OAuth2 integration (Google, GitHub, etc.)
- Session management
- Role-based access control (RBAC)
- API key management
- Two-factor authentication (2FA)
- Password reset flows
- Email verification

**Implementation:**
```javascript
// JWT Authentication
import jwt from 'jsonwebtoken';

export const authenticate = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Role-based authorization
export const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};
```

### Performance Optimizer

**Optimization Features:**
- Caching strategies (Redis, Memcached)
- Database query optimization
- Connection pool tuning
- Load balancing configuration
- Rate limiting
- Response compression
- CDN integration
- Monitoring and profiling

**Usage:**
```bash
# Analyze API performance
python scripts/performance_optimizer.py analyze \
  --endpoint /api/v1/users \
  --duration 1h \
  --output report.html

# Add caching layer
python scripts/performance_optimizer.py add-cache \
  --endpoints /api/v1/users,/api/v1/products \
  --strategy redis \
  --ttl 300

# Optimize database queries
python scripts/performance_optimizer.py optimize-queries \
  --analyze-slow-queries \
  --threshold 100ms
```

## How It Works

### API Development Workflow

**Step 1: Design API Structure**
```bash
# Generate API with OpenAPI spec
python scripts/api_scaffolder.py from-spec \
  --spec api-spec.yaml \
  --language node \
  --framework express
```

**Step 2: Implement Business Logic**
```javascript
// Service layer implementation
export class ProductService {
  async createProduct(data) {
    // Validate data
    await this.validateProduct(data);

    // Check for duplicates
    const existing = await this.productRepo.findBySku(data.sku);
    if (existing) {
      throw new ApiError(400, 'Product with this SKU already exists');
    }

    // Create product
    const product = await this.productRepo.create(data);

    // Emit event
    await eventBus.emit('product.created', product);

    // Invalidate cache
    await cache.del('products:list');

    return product;
  }
}
```

**Step 3: Add Caching**
```javascript
// Cache middleware
export const cacheMiddleware = (ttl = 300) => {
  return async (req, res, next) => {
    const key = `cache:${req.originalUrl}`;

    const cached = await redis.get(key);
    if (cached) {
      return res.json(JSON.parse(cached));
    }

    // Store original send
    const originalSend = res.json;
    res.json = function(data) {
      redis.setex(key, ttl, JSON.stringify(data));
      originalSend.call(this, data);
    };

    next();
  };
};

// Use in routes
router.get('/products', cacheMiddleware(300), getProducts);
```

**Step 4: Add Monitoring**
```javascript
// Prometheus metrics
import prometheus from 'prom-client';

const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
});

app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration);
  });

  next();
});
```

## Technical Details

### Architecture Patterns

**Layered Architecture:**
```
Controllers (HTTP handlers)
    ↓
Services (Business logic)
    ↓
Repositories (Data access)
    ↓
Database
```

**Microservices Pattern:**
```
API Gateway
    ↓
Service A ← Message Queue → Service B
    ↓                           ↓
Database A                  Database B
```

### Best Practices

**Do:**
- Use environment variables for configuration
- Implement proper error handling
- Validate all inputs
- Use parameterized queries (prevent SQL injection)
- Implement rate limiting
- Use connection pooling
- Log important events
- Write comprehensive tests
- Document APIs (OpenAPI/Swagger)
- Use async/await properly
- Implement health checks
- Use transactions for data consistency

**Don't:**
- Store secrets in code
- Ignore error handling
- Trust user input
- Use synchronous operations for I/O
- Expose internal errors to clients
- Skip input validation
- Ignore performance metrics
- Use SELECT * queries
- Forget to close connections
- Deploy without monitoring

## Integration Points

This skill integrates with:
- **Databases:** PostgreSQL, MySQL, MongoDB, Redis, DynamoDB
- **Message Queues:** RabbitMQ, Kafka, AWS SQS, Redis
- **Caching:** Redis, Memcached, CDN
- **Authentication:** Auth0, Firebase Auth, AWS Cognito
- **Monitoring:** Prometheus, Grafana, DataDog, New Relic
- **Logging:** Winston, Pino, ELK Stack, CloudWatch
- **Deployment:** Docker, Kubernetes, AWS, GCP, Azure
- **Testing:** Jest, Mocha, Pytest, Go test

## Common Challenges and Solutions

### Challenge: Slow Database Queries
**Solution:** Add indexes, use query optimization, implement caching, use read replicas, optimize data models, use database connection pooling, implement pagination

### Challenge: High API Latency
**Solution:** Add caching layers, optimize database queries, use CDN for static content, implement request batching, use async processing, add load balancing, optimize serialization

### Challenge: Authentication Security
**Solution:** Use JWT with short expiration, implement refresh tokens, use HTTPS only, add rate limiting, implement 2FA, use secure password hashing (bcrypt), validate tokens properly

### Challenge: Scaling Issues
**Solution:** Implement horizontal scaling, use load balancers, add caching, implement database sharding, use microservices architecture, add message queues, use serverless functions

### Challenge: API Versioning
**Solution:** Use URL versioning (/v1/, /v2/), implement backward compatibility, document breaking changes, use feature flags, provide migration guides, support multiple versions

### Challenge: Error Handling
**Solution:** Create custom error classes, use consistent error format, log errors properly, don't expose internal errors, use proper HTTP status codes, implement error monitoring
