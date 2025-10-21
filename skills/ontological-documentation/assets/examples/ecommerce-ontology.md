# E-Commerce Domain Ontology Example

## Overview
This example demonstrates an ontological documentation approach for a typical e-commerce system.

## Core Concepts

### Primary Entities
```
E-Commerce Domain
├── Customer Management
│   ├── Customer
│   ├── CustomerProfile
│   └── Address
├── Product Management
│   ├── Product
│   ├── Category
│   └── ProductVariant
├── Order Management
│   ├── Order
│   ├── OrderLine
│   └── OrderStatus
└── Payment Management
    ├── Payment
    ├── PaymentMethod
    └── PaymentStatus
```

### Key Relationships

#### Customer Relationships
- **Customer** has-a **CustomerProfile**
- **Customer** has-many **Address**
- **Customer** places-many **Order**
- **Customer** has-many **Payment**

#### Product Relationships
- **Product** belongs-to **Category**
- **Product** has-many **ProductVariant**
- **ProductVariant** appears-in **OrderLine**

#### Order Relationships
- **Order** contains-many **OrderLine**
- **Order** has-a **OrderStatus**
- **Order** has-a **Payment**
- **OrderLine** references-a **ProductVariant**

## Business Rules

### Customer Rules
- Customer must have at least one address
- Customer profile must include valid email
- Customer can have multiple shipping addresses

### Order Rules
- Order must have at least one order line
- Order total must equal sum of order line totals
- Order status progression is immutable

### Payment Rules
- Payment amount must match order total
- Payment method must be valid for customer
- Payment status affects order fulfillment

## Implementation Examples

### Order Entity Example
```python
class Order:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.order_lines: List[OrderLine] = []
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()

    def add_product(self, product: ProductVariant, quantity: int):
        # Add business logic for adding products
        pass

    def calculate_total(self) -> Money:
        # Calculate order total
        pass
```

### Relationship Example
```python
# Order -> Customer relationship
class Order:
    def __init__(self, customer: Customer):
        self.customer_id = customer.id  # Reference relationship
        self.customer = customer  # Object relationship
```

## Documentation Links
- [Customer Documentation](customer-concept.md)
- [Product Documentation](product-concept.md)
- [Order Documentation](order-concept.md)
- [Payment Documentation](payment-concept.md)