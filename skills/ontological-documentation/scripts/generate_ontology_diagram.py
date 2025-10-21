#!/usr/bin/env python3
"""
Ontology Diagram Generator

This script generates visual representations of ontologies in various formats
including Mermaid, PlantUML, GraphViz DOT, and JSON-LD for semantic web applications.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional


class OntologyDiagramGenerator:
    """Generates diagrams for ontological documentation."""

    def __init__(self):
        self.relationship_symbols = {
            'is_a': '--|>',  # Inheritance
            'part_of': '--*',  # Composition
            'depends_on': '-.->',  # Dependency
            'associates_with': '---',  # Association
            'instance_of': '..>'  # Instantiation
        }

    def generate_mermaid(self, ontology: Dict[str, Any]) -> str:
        """Generate Mermaid diagram from ontology."""
        lines = ["graph TD"]
        lines.append("    %% Ontology Diagram")
        lines.append("    %% Generated from ontological documentation")

        # Add styling
        lines.extend([
            "    classDef concept fill:#e1f5fe,stroke:#01579b,stroke-width:2px",
            "    classDef class fill:#f3e5f5,stroke:#4a148c,stroke-width:2px",
            "    classDef interface fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px",
            "    classDef function fill:#fff3e0,stroke:#e65100,stroke-width:2px"
        ])

        # Add concepts as nodes
        concept_classes = {}
        for concept_name, concept_data in ontology['concepts'].items():
            concept_type = concept_data.get('type', 'concept')

            if concept_type == 'class':
                lines.append(f"    {self._safe_name(concept_name)}[({concept_name})]")
                concept_classes[concept_name] = 'class'
            elif concept_type == 'interface':
                lines.append(f"    {self._safe_name(concept_name)}[{{interface}}{concept_name}]")
                concept_classes[concept_name] = 'interface'
            elif concept_type == 'function':
                lines.append(f"    {self._safe_name(concept_name)}[{concept_name}()]")
                concept_classes[concept_name] = 'function'
            else:
                lines.append(f"    {self._safe_name(concept_name)}[{concept_name}]")
                concept_classes[concept_name] = 'concept'

        # Add relationships
        for rel_type, relationships in ontology['relationships'].items():
            symbol = self.relationship_symbols.get(rel_type, '---')
            for rel in relationships:
                subject = self._safe_name(rel['subject'])
                obj = self._safe_name(rel['object'])
                label = rel.get('label', rel_type.replace('_', ' ').title())
                lines.append(f"    {subject} {symbol} {obj}")

        # Apply classes
        for concept_name, css_class in concept_classes.items():
            lines.append(f"    class {self._safe_name(concept_name)} {css_class}")

        return "\n".join(lines)

    def generate_plantuml(self, ontology: Dict[str, Any]) -> str:
        """Generate PlantUML diagram from ontology."""
        lines = ["@startuml Ontology"]
        lines.append("!theme plain")
        lines.append("skinparam classAttributeIconSize 0")

        # Add concepts as classes
        for concept_name, concept_data in ontology['concepts'].items():
            concept_type = concept_data.get('type', 'concept')

            if concept_type == 'class':
                lines.append(f"class {concept_name} {{}}")
            elif concept_type == 'interface':
                lines.append(f"interface {concept_name} {{}}")
            elif concept_type == 'function':
                lines.append(f"object {concept_name} {{}}")
            else:
                lines.append(f"abstract {concept_name} {{}}")

        lines.append("")  # Empty line for separation

        # Add relationships
        for rel_type, relationships in ontology['relationships'].items():
            for rel in relationships:
                subject = rel['subject']
                obj = rel['object']

                if rel_type == 'is_a':
                    lines.append(f"{subject} <|-- {obj}")
                elif rel_type == 'part_of':
                    lines.append(f"{subject} *-- {obj}")
                elif rel_type == 'depends_on':
                    lines.append(f"{subject} ..> {obj}")
                else:
                    lines.append(f"{subject} -- {obj}")

        lines.append("@enduml")
        return "\n".join(lines)

    def generate_dot(self, ontology: Dict[str, Any]) -> str:
        """Generate GraphViz DOT diagram from ontology."""
        lines = ["digraph Ontology {"]
        lines.append('    rankdir=TB;')
        lines.append('    node [shape=box, style=filled];')
        lines.append('    edge [fontsize=10];')

        # Add concepts as nodes
        for concept_name, concept_data in ontology['concepts'].items():
            concept_type = concept_data.get('type', 'concept')

            # Set colors based on type
            if concept_type == 'class':
                color = "lightpurple"
            elif concept_type == 'interface':
                color = "lightgreen"
            elif concept_type == 'function':
                color = "lightorange"
            else:
                color = "lightblue"

            lines.append(f'    "{concept_name}" [label="{concept_name}", fillcolor="{color}"];')

        lines.append("")  # Empty line for separation

        # Add relationships
        for rel_type, relationships in ontology['relationships'].items():
            for rel in relationships:
                subject = rel['subject']
                obj = rel['object']
                label = rel.get('label', rel_type.replace('_', ' ').title())

                # Set arrow styles based on relationship type
                if rel_type == 'is_a':
                    arrow = 'empty'
                elif rel_type == 'part_of':
                    arrow = 'diamond'
                elif rel_type == 'depends_on':
                    arrow = 'dashed'
                else:
                    arrow = 'normal'

                lines.append(f'    "{subject}" -> "{obj}" [label="{label}", arrowhead={arrow}];')

        lines.append("}")
        return "\n".join(lines)

    def generate_json_ld(self, ontology: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON-LD representation of ontology."""
        context = {
            "@context": {
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "owl": "http://www.w3.org/2002/07/owl#",
                "Concept": "rdfs:Class",
                "subClassOf": {
                    "@id": "rdfs:subClassOf",
                    "@type": "@id"
                },
                "partOf": {
                    "@id": "http://example.org/ontology#partOf",
                    "@type": "@id"
                },
                "dependsOn": {
                    "@id": "http://example.org/ontology#dependsOn",
                    "@type": "@id"
                }
            },
            "@graph": []
        }

        # Add concepts
        for concept_name, concept_data in ontology['concepts'].items():
            concept_entry = {
                "@id": f"http://example.org/ontology#{concept_name}",
                "@type": ["Concept"]
            }

            concept_type = concept_data.get('type', 'concept')
            if concept_type == 'class':
                concept_entry["@type"].append("owl:Class")
            elif concept_type == 'interface':
                concept_entry["@type"].append("owl:Class")

            context["@graph"].append(concept_entry)

        # Add relationships
        for rel_type, relationships in ontology['relationships'].items():
            for rel in relationships:
                subject = rel['subject']
                obj = rel['object']

                if rel_type == 'is_a':
                    context["@graph"].append({
                        "@id": f"http://example.org/ontology#{subject}",
                        "subClassOf": f"http://example.org/ontology#{obj}"
                    })
                elif rel_type == 'part_of':
                    context["@graph"].append({
                        "@id": f"http://example.org/ontology#{subject}",
                        "partOf": f"http://example.org/ontology#{obj}"
                    })
                elif rel_type == 'depends_on':
                    context["@graph"].append({
                        "@id": f"http://example.org/ontology#{subject}",
                        "dependsOn": f"http://example.org/ontology#{obj}"
                    })

        return context

    def _safe_name(self, name: str) -> str:
        """Convert name to safe identifier for diagram formats."""
        # Replace special characters and spaces with underscores
        return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def load_ontology(file_path: Path) -> Dict[str, Any]:
    """Load ontology from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Main function to generate diagrams."""
    parser = argparse.ArgumentParser(description='Generate ontology diagrams')
    parser.add_argument('ontology_file', help='Path to ontology JSON file')
    parser.add_argument('--format', choices=['mermaid', 'plantuml', 'dot', 'json-ld', 'all'],
                       default='all', help='Diagram format to generate')
    parser.add_argument('--output', help='Output directory (default: current directory)')
    args = parser.parse_args()

    ontology_path = Path(args.ontology_file)
    if not ontology_path.exists():
        print(f"Error: Ontology file '{ontology_path}' not found")
        sys.exit(1)

    ontology = load_ontology(ontology_path)
    generator = OntologyDiagramGenerator()

    output_dir = Path(args.output) if args.output else Path('.')
    output_dir.mkdir(exist_ok=True)

    formats_to_generate = ['mermaid', 'plantuml', 'dot', 'json-ld'] if args.format == 'all' else [args.format]

    for format_type in formats_to_generate:
        if format_type == 'mermaid':
            diagram = generator.generate_mermaid(ontology)
            output_file = output_dir / f"{ontology_path.stem}_mermaid.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {ontology_path.stem} Ontology Diagram\n\n")
                f.write("```mermaid\n")
                f.write(diagram)
                f.write("\n```")
            print(f"Generated Mermaid diagram: {output_file}")

        elif format_type == 'plantuml':
            diagram = generator.generate_plantuml(ontology)
            output_file = output_dir / f"{ontology_path.stem}_plantuml.puml"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(diagram)
            print(f"Generated PlantUML diagram: {output_file}")

        elif format_type == 'dot':
            diagram = generator.generate_dot(ontology)
            output_file = output_dir / f"{ontology_path.stem}.dot"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(diagram)
            print(f"Generated GraphViz DOT diagram: {output_file}")

        elif format_type == 'json-ld':
            json_ld = generator.generate_json_ld(ontology)
            output_file = output_dir / f"{ontology_path.stem}_jsonld.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_ld, f, indent=2)
            print(f"Generated JSON-LD: {output_file}")


if __name__ == "__main__":
    import re
    main()