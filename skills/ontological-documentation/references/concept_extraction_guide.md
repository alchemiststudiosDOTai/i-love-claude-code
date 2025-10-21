# Concept Extraction Guide for Software Systems

This guide provides methodologies and techniques for identifying and extracting domain concepts, entities, and relationships from software codebases to build ontological documentation.

## Extraction Methodologies

### 1. Static Code Analysis

#### Class and Interface Analysis
- **Objective**: Identify conceptual entities and their hierarchies
- **Sources**: Class definitions, interface declarations, type annotations
- **Techniques**:
  - Parse AST (Abstract Syntax Trees) to find type definitions
  - Extract inheritance relationships (extends, implements)
  - Identify composition patterns through member variables
  - Analyze method signatures for behavioral concepts

#### Function and Method Analysis
- **Objective**: Discover actions, processes, and behavioral concepts
- **Sources**: Function definitions, method declarations
- **Techniques**:
  - Group related functions into conceptual categories
  - Identify command/query patterns (CQRS)
  - Extract business process flows from method call chains
  - Map function parameters to conceptual relationships

#### Import and Dependency Analysis
- **Objective**: Understand system boundaries and external dependencies
- **Sources**: Import statements, package dependencies, service calls
- **Techniques**:
  - Map module dependencies to conceptual relationships
  - Identify external system boundaries
  - Categorize dependencies (internal, external, third-party)
  - Analyze dependency graphs for architectural insights

### 2. Naming Convention Analysis

#### Semantic Naming Patterns
- **Entity Nouns**: User, Order, Product, Account (domain objects)
- **Process Verbs**: ProcessPayment, ValidateInput, SendEmail (actions)
- **State Adjectives**: Active, Pending, Completed, Expired (states)
- **Role-based Names**: AdminService, UserGateway, PaymentProcessor (roles)

#### Naming Pattern Recognition
```
Entity + Pattern = Concept Type
- User + Repository = Data Access Concept
- Order + Service = Business Logic Concept
- Payment + Gateway = Integration Concept
- Notification + Event = Event Concept
```

### 3. Data Structure Analysis

#### Database Schema Analysis
- **Tables as Entities**: Each table represents a domain concept
- **Foreign Keys as Relationships**: FKs define relationships between concepts
- **Indexes as Properties**: Important attributes for concept identification
- **Constraints as Rules**: Business rules and validation logic

#### API Contract Analysis
- **REST Resources**: URL paths often map to domain concepts
- **GraphQL Types**: Schema types define conceptual models
- **Message Schemas**: Event/message structures reveal concepts
- **OpenAPI Specifications**: Complete conceptual model of external interface

### 4. Configuration and Metadata Analysis

#### Configuration Files
- **Application Settings**: System behavior concepts
- **Feature Flags**: Feature-based concept organization
- **Environment Variables**: Deployment and environment concepts
- **Routing Tables**: Navigation and flow concepts

#### Documentation and Comments
- **README Files**: High-level conceptual overview
- **Code Comments**: Designer intent and conceptual explanations
- **API Documentation**: External conceptual contracts
- **Architecture Diagrams**: Visual conceptual relationships

## Extraction Techniques by Language

### Python
```python
# Key patterns to identify:
class UserService:                    # Service concept
    def __init__(self, user_repo):   # Dependency relationship
        self.user_repo = user_repo

    def create_user(self, user_dto): # Action concept
        # Domain logic here
        pass

# Look for:
# - Class definitions (entities, services, repositories)
# - Method names (actions, processes)
# - Parameter types (relationships)
# - Decorators (cross-cutting concerns)
```

### JavaScript/TypeScript
```typescript
// Key patterns to identify:
interface User {                     # Entity concept
  id: string;
  name: string;
}

class UserService {                  # Service concept
  constructor(private userRepo: UserRepository) {} # Dependency

  async createUser(userData: CreateUserDto): Promise<User> { # Action + types
    // Implementation
  }
}

// Look for:
# - Interface definitions (contracts, entities)
# - Class definitions (services, controllers)
# - Type annotations (concept properties)
# - Decorators (metadata, concerns)
```

### Java
```java
// Key patterns to identify:
@Entity                             # Entity annotation
public class User {                 # Entity concept
    @Id
    private Long id;

    @OneToMany                      # Relationship annotation
    private List<Order> orders;
}

@Service                           # Service annotation
public class UserService {         # Service concept
    @Autowired                     # Dependency injection
    private UserRepository userRepo;

    public User createUser(UserDto userDto) { // Action + type
        // Implementation
    }
}

// Look for:
# - Annotations (component types, relationships)
# - Class definitions (entities, services)
# - Interface definitions (contracts)
# - Method signatures (actions, processes)
```

## Concept Categorization Framework

### Primary Categories

1. **Domain Entities** (Nouns)
   - Core business objects: User, Order, Product, Account
   - Usually persistent, have identity
   - Contain business logic and state

2. **Value Objects** (Nouns)
   - Immutable concepts without identity: Address, Money, DateRange
   - Defined by their attributes
   - Often embedded in entities

3. **Services** (Verb + Noun)
   - Business logic coordinators: UserService, PaymentService
   - Stateless operations
   - Orchestrate domain objects

4. **Repositories** (Noun + Repository/Store)
   - Data access abstractions: UserRepository, OrderRepository
   - Collection-like interfaces
   - Hide storage details

5. **Controllers/Handlers** (Noun + Controller/Handler)
   - Request/response coordination: UserController, OrderController
   - Interface between external world and domain
   - Thin layer, delegate to services

### Secondary Categories

6. **Events/Notifications** (Past Tense Verbs + Noun)
   - State changes: OrderCreated, PaymentProcessed, UserRegistered
   - Asynchronous communication
   - Decouple system components

7. **DTOs/Models** (Noun + Dto/Model)
   - Data transfer objects: UserDto, OrderModel
   - External contract representations
   - No business logic

8. **Utilities/Helpers** (Adjective/Noun + Utility/Helper)
   - Cross-cutting functionality: ValidationHelper, EmailUtility
   - Reusable operations
   - No domain concepts

## Relationship Identification

### Direct Relationships
- **Inheritance**: `class Admin extends User` (Is-A)
- **Composition**: `class Order { private List<OrderLine> lines; }` (Part-Of)
- **Dependency**: `UserService(UserRepository repo)` (Depends-On)

### Indirect Relationships
- **Shared Interfaces**: Implement same interface (Associates-With)
- **Common Patterns**: Similar naming or structure (Similar-To)
- **Event Connections**: Producer-consumer patterns (Communicates-With)

### Semantic Relationships
- **Temporal**: CreatedBefore, UpdatedAfter
- **Spatial**: Contains, LocatedWithin
- **Causal**: Triggers, Enables, Prevents
- **Logical**: Implies, Contradicts, Equivalent

## Extraction Workflow

### Phase 1: Automated Extraction
1. Run static analysis tools to identify:
   - Class/interface definitions
   - Inheritance hierarchies
   - Import dependencies
   - Method signatures

### Phase 2: Manual Analysis
1. Review automated results for semantic accuracy
2. Identify implicit concepts not captured by code
3. Map business terminology to technical concepts
4. Validate relationships with domain experts

### Phase 3: Ontology Construction
1. Organize concepts into hierarchies
2. Define relationships between concepts
3. Add semantic metadata and descriptions
4. Validate completeness and consistency

### Phase 4: Documentation Generation
1. Create visual representations
2. Generate textual documentation
3. Create interactive navigation
4. Establish maintenance processes

## Quality Assurance

### Validation Checks
- [ ] All identified concepts have clear definitions
- [ ] Relationships are correctly classified
- [ ] No circular inheritance exists
- [ ] Domain terminology is consistent
- [ ] Technical and business concepts are aligned

### Review Process
1. **Developer Review**: Technical accuracy and completeness
2. **Domain Expert Review**: Business concept validation
3. **Architecture Review**: Consistency with system design
4. **Documentation Review**: Clarity and usability

## Maintenance Strategies

### Continuous Updates
- Monitor code changes for new concepts
- Update ontology when requirements evolve
- Regular reviews with stakeholders
- Automated validation checks

### Version Management
- Tag ontology versions with releases
- Track concept evolution over time
- Maintain change logs
- Backward compatibility considerations