# Ontological Patterns in Software Documentation

This document describes common ontological patterns and taxonomies found in software systems for creating effective conceptual documentation.

## Core Ontological Concepts

### Fundamental Relationship Types

**Is-A (Inheritance/Hyponymy)**
- Description: A concept is a subtype or specialization of another concept
- Example: `User` is-a `Person`, `Manager` is-a `Employee`
- Code pattern: Class inheritance, interface implementation
- Documentation: Use "extends," "inherits from," "is a type of"

**Part-Of (Mereology/Composition)**
- Description: A concept is a component or constituent of another concept
- Example: `Wheel` is-part-of `Car`, `Method` is-part-of `Class`
- Code pattern: Object composition, nested classes, containment relationships
- Documentation: Use "contains," "comprises," "consists of"

**Instance-Of (Instantiation)**
- Description: An object is an instance of a concept/class
- Example: `john_doe` is-instance-of `User`, `order_123` is-instance-of `Order`
- Code pattern: Object creation, variable assignment
- Documentation: Use "instance of," "example of," "specific case of"

**Depends-On (Dependency)**
- Description: A concept requires or relies on another concept
- Example: `OrderService` depends-on `PaymentGateway`, `Controller` depends-on `Service`
- Code pattern: Import statements, dependency injection, method calls
- Documentation: Use "requires," "uses," "relies on"

**Associates-With (Association)**
- Description: A concept has a loose semantic connection to another concept
- Example: `User` associates-with `Order`, `Product` associates-with `Category`
- Code pattern: Foreign keys, bidirectional references, event subscriptions
- Documentation: Use "related to," "connected with," "associated with"

## Common Software Ontology Patterns

### Layered Architecture Pattern

```
Presentation Layer
├── Controllers
├── Views
└── ViewModels

Business Logic Layer
├── Services
├── Domain Models
└── Business Rules

Data Access Layer
├── Repositories
├── Data Mappers
└── Database Models

Infrastructure Layer
├── External APIs
├── Message Queues
└── File Storage
```

**Relationships:**
- Controllers depend-on Services
- Services depend-on Repositories
- Repositories depend-on Database Models
- ViewModels part-of Presentation Layer

### Domain-Driven Design Pattern

**Entities**: Objects with distinct identity
- `Customer`, `Order`, `Product`

**Value Objects**: Objects defined by their attributes
- `Address`, `Money`, `DateRange`

**Aggregates**: Clusters of domain objects
- `OrderAggregate` contains `Order`, `OrderLine`, `OrderStatus`

**Repositories**: Collections of aggregate roots
- `CustomerRepository`, `OrderRepository`

**Domain Services**: Business logic that doesn't fit in entities
- `PaymentService`, `ShippingService`

### MVC Pattern Ontology

```
Model
├── Entity Models
├── View Models
└── Data Transfer Objects

View
├── Templates
├── Components
└── Layouts

Controller
├── Action Methods
├── Route Handlers
└── API Endpoints
```

**Relationships:**
- Controllers manipulate Models
- Controllers select Views
- Views display Models
- Models notify Views of changes

### Microservices Pattern Ontology

**Service Categories:**
- **API Gateway**: Entry point for external requests
- **Core Services**: Business logic services
- **Supporting Services**: Shared functionality (auth, logging)
- **Data Services**: Database operations

**Service Relationships:**
- `API Gateway` routes-to `Core Services`
- `Core Services` call `Supporting Services`
- `Services` publish-to `Message Broker`
- `Services` read-from `Configuration Service`

## Taxonomy Classification Systems

### Functional Classification

**By Purpose:**
- Business Logic Components
- Data Management Components
- Presentation Components
- Integration Components
- Infrastructure Components

**By Lifecycle:**
- Singleton Components
- Scoped Components
- Transient Components
- Request-scoped Components

### Structural Classification

**By Abstraction Level:**
- Interface Layer (highest abstraction)
- Service Layer
- Repository Layer
- Data Layer (lowest abstraction)

**By Coupling:**
- Tightly Coupled Components
- Loosely Coupled Components
- Decoupled Components

## Documentation Templates

### Concept Documentation Template

```markdown
# [Concept Name]

## Definition
Brief, clear definition of the concept

## Purpose
Why this concept exists and what problem it solves

## Characteristics
Key attributes and properties of the concept

## Relationships
- **Is-A**: [Parent concepts]
- **Part-Of**: [Containing concepts]
- **Depends-On**: [Required concepts]
- **Associates-With**: [Related concepts]

## Examples
Concrete examples of the concept in use

## Implementation Notes
Technical implementation details and considerations
```

### Relationship Documentation Template

```markdown
# [Relationship Type]: [Source] → [Target]

## Relationship Description
Description of the semantic relationship

## Cardinality
- One-to-One, One-to-Many, Many-to-Many
- Required vs Optional

## Constraints
Rules and limitations on the relationship

## Implementation
How the relationship is implemented in code

## Examples
Specific examples of the relationship
```

## Ontology Validation Rules

### Consistency Rules

1. **No Circular Inheritance**: A class cannot inherit from itself (directly or indirectly)
2. **Complete Relationships**: All referenced concepts must be defined
3. **Consistent Naming**: Use consistent terminology throughout the ontology
4. **Proper Abstraction Levels**: Related concepts should be at similar abstraction levels

### Completeness Rules

1. **Defined Concepts**: All concepts must have clear definitions
2. **Documented Relationships**: All relationships should be explicitly documented
3. **Coverage**: Important domain concepts should be represented
4. **Hierarchy**: Concepts should be organized in logical hierarchies

### Best Practices

1. **Use Standard Terminology**: Prefer established domain vocabulary
2. **Avoid Ambiguity**: Define terms clearly and consistently
3. **Maintain Separation**: Separate conceptual models from implementation details
4. **Document Rationale**: Explain why certain relationships exist
5. **Regular Review**: Update ontology as system evolves