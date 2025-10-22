# Ontological Documentation Skill

## What are Claude Skills?

Claude Skills are reusable modules that package specialized knowledge and instructions for specific tasks. A skill consists of a folder containing a `SKILL.md` file with YAML frontmatter (name, description) and markdown instructions.

**Key points:**
- Skills activate automatically based on task relevance
- Work across Claude web app, Claude Code, and API
- Transform Claude from general AI to domain specialist
- Can include code, data, and supporting files
- Minimal skill = folder + SKILL.md file

**Structure:**
```
skill-folder/
├── SKILL.md (with YAML header + instructions)
└── (optional supporting files)
```

Skills act like on-demand expert modules that Claude loads only when needed, making them context-specific and efficient.

## Overview

The **ontological-documentation** skill transforms Claude into a specialized assistant for creating, organizing, and maintaining ontological documentation. It provides structured approaches to knowledge representation, taxonomic classification, and semantic relationship mapping.

## Purpose

This skill is activated when users need to:
- Create knowledge ontologies and taxonomies
- Document complex conceptual relationships
- Build structured information architectures
- Design semantic data models
- Organize hierarchical knowledge systems

## Key Capabilities

- **Ontology Design**: Creates formal ontological structures with proper classification schemes
- **Relationship Mapping**: Documents semantic relationships between concepts
- **Taxonomy Development**: Builds hierarchical classification systems
- **Semantic Modeling**: Creates structured data models with clear relationships
- **Knowledge Organization**: Organizes complex information into coherent frameworks

## Usage Examples

The skill automatically engages when you mention:
- "Create an ontology for..."
- "Design a taxonomy of..."
- "Map the relationships between..."
- "Document the conceptual framework..."
- "Build a knowledge structure..."

## Core Methodology

Based on established ontological principles:
- Entity-relationship modeling
- Hierarchical classification systems
- Semantic web standards (RDF/OWL concepts)
- Knowledge representation frameworks
- Conceptual mapping techniques

## Integration

This skill works seamlessly with other documentation and analytical skills, providing the semantic foundation for comprehensive knowledge systems.