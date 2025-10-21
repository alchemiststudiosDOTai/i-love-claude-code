---
name: ontological-documentation
description: This skill should be used when creating comprehensive ontological documentation for software systems, including extracting domain concepts, modeling semantic relationships, and generating visual representations of system architectures and business domains.
---

# Ontological Documentation

## Overview

This skill enables the creation of comprehensive ontological documentation that captures the fundamental concepts, relationships, and classification systems within code and systems. It goes beyond typical API documentation to include semantic structure, conceptual models, and domain taxonomies that provide deep understanding of system architecture and business logic.

## When to Use This Skill

Use this skill when you need to:
- Document the conceptual structure and domain model of a software system
- Extract and organize business concepts from existing codebases
- Create visual representations of system architectures and relationships
- Build semantic maps of entities, services, and their interactions
- Design or document domain models for new systems
- Analyze and communicate complex system architectures to stakeholders
- Create knowledge graphs or concept maps for development teams

## Quick Start

### For New Systems
1. **Design Phase**: Start with domain modeling templates in `assets/ontology-templates/`
2. **Concept Identification**: Use patterns from `references/ontology_patterns.md`
3. **Documentation Creation**: Apply templates from `references/documentation_templates.md`
4. **Visualization**: Generate diagrams using `scripts/generate_ontology_diagram.py`

### For Existing Systems
1. **Concept Extraction**: Run `scripts/extract_concepts.py` on your codebase
2. **Analysis**: Review extracted concepts using guidelines in `references/concept_extraction_guide.md`
3. **Documentation**: Create comprehensive concept documentation
4. **Visualization**: Generate ontology diagrams for various formats

## Core Capabilities

### 1. Concept Extraction and Analysis
Use automated tools to identify and categorize domain concepts from source code:

```bash
# Extract concepts from Python codebase
python scripts/extract_concepts.py ./src

# Extract concepts from JavaScript/TypeScript
python scripts/extract_concepts.py ./frontend

# Generate ontology JSON structure
python scripts/extract_concepts.py ./src > ontology.json
```

**Identifies:**
- Class and interface hierarchies (is-a relationships)
- Composition patterns (part-of relationships)
- Service dependencies (depends-on relationships)
- Domain entities vs technical concepts

### 2. Ontology Visualization
Generate multiple diagram formats for different audiences:

```bash
# Generate all diagram formats
python scripts/generate_ontology_diagram.py ontology.json --format all

# Generate specific formats
python scripts/generate_ontology_diagram.py ontology.json --format mermaid
python scripts/generate_ontology_diagram.py ontology.json --format plantuml
```

**Supported formats:**
- **Mermaid**: For README files and documentation
- **PlantUML**: For technical architecture diagrams
- **GraphViz DOT**: For publication-quality graphics
- **JSON-LD**: For semantic web applications

### 3. Documentation Templates
Standardized templates for consistent documentation:

- **Concept Definition**: Comprehensive entity documentation
- **Relationship Documentation**: Detailed relationship analysis
- **Domain Model Overview**: High-level domain architecture
- **Change Log**: Ontology evolution tracking

### 4. Pattern Recognition
Identify common ontological patterns in software:

- **Layered Architecture Patterns**: Presentation, Business, Data layers
- **Domain-Driven Design Patterns**: Entities, Value Objects, Aggregates
- **Microservice Patterns**: Service boundaries and relationships
- **MVC/MVVM Patterns**: Component relationships and data flow

## Workflow

### Step 1: Discovery and Extraction
1. **Analyze Codebase**: Run concept extraction tools
2. **Review Patterns**: Identify common architectural patterns
3. **Map Terminology**: Align technical terms with business vocabulary
4. **Consult Stakeholders**: Validate concepts with domain experts

### Step 2: Ontology Construction
1. **Categorize Concepts**: Group entities, services, and relationships
2. **Define Relationships**: Document semantic connections
3. **Create Hierarchies**: Build taxonomic structures
4. **Validate Logic**: Ensure consistency and completeness

### Step 3: Documentation Creation
1. **Use Templates**: Apply standardized documentation formats
2. **Add Examples**: Include concrete usage examples
3. **Document Rules**: Capture business logic and constraints
4. **Cross-Reference**: Link related concepts and documentation

### Step 4: Visualization and Communication
1. **Generate Diagrams**: Create visual representations
2. **Choose Formats**: Select appropriate diagrams for audiences
3. **Create Navigation**: Build browsable concept maps
4. **Present to Stakeholders**: Communicate domain understanding

## Common Use Cases

### Use Case 1: System Onboarding
*"I need to understand the domain model of this complex e-commerce system to onboard new developers."*

**Approach:**
1. Run concept extraction on the entire codebase
2. Generate domain overview diagrams
3. Create concept documentation for core entities
4. Build interactive navigation for the ontology

### Use Case 2: Architecture Documentation
*"Document the microservice architecture and service relationships for our CTO presentation."*

**Approach:**
1. Identify service boundaries and responsibilities
2. Map service dependencies and communication patterns
3. Generate architecture diagrams in multiple formats
4. Create service-level documentation

### Use Case 3: Domain Model Design
*"We're building a new healthcare platform and need to design the domain model."*

**Approach:**
1. Use domain modeling templates
2. Apply healthcare-specific patterns
3. Create comprehensive entity documentation
4. Validate model with domain experts

### Use Case 4: Legacy System Analysis
*"Analyze this 10-year-old codebase to understand the business domain before refactoring."*

**Approach:**
1. Extract concepts from legacy code
2. Identify business rules and logic
3. Map domain terminology
4. Create migration documentation

## Resources

### Scripts (Executable Tools)
- **`extract_concepts.py`**: Automated concept extraction from source code
- **`generate_ontology_diagram.py`**: Multi-format diagram generation from ontology JSON

### References (Guidance Documentation)
- **`ontology_patterns.md`**: Common ontological patterns in software architecture
- **`concept_extraction_guide.md`**: Methodologies for identifying domain concepts
- **`documentation_templates.md`**: Standardized templates for documentation

### Assets (Templates and Examples)
- **`ontology-templates/`**: Reusable templates for different ontology types
- **`examples/`**: Sample ontological documentation from various domains

## Quality Assurance

### Validation Checklist
- [ ] All concepts have clear, unambiguous definitions
- [ ] Relationships are properly categorized and documented
- [ ] Business rules and constraints are captured
- [ ] Technical and business terminology are aligned
- [ ] Visualizations accurately represent the ontology
- [ ] Documentation follows established templates
- [ ] Examples are relevant and illustrative

### Review Process
1. **Technical Review**: Validate code analysis and relationships
2. **Domain Review**: Confirm business concept accuracy with experts
3. **Documentation Review**: Ensure clarity and completeness
4. **Visual Review**: Validate diagram accuracy and readability

