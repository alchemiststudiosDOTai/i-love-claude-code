#!/usr/bin/env python3
"""
Concept Extraction Script for Ontological Documentation

This script analyzes codebases to extract domain concepts, entities, and relationships
for building ontological documentation. It supports multiple programming languages
and can identify inheritance hierarchies, composition patterns, and semantic relationships.
"""

import ast
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict

class ConceptExtractor:
    """Extracts ontological concepts from source code."""

    def __init__(self):
        self.concepts = defaultdict(dict)
        self.relationships = defaultdict(list)
        self.taxonomies = defaultdict(list)

    def extract_from_python(self, file_path: Path) -> Dict[str, Any]:
        """Extract concepts from Python source code."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            visitor = ClassVisitor()
            visitor.visit(tree)

            return {
                'classes': visitor.classes,
                'inheritance': visitor.inheritance,
                'imports': visitor.imports,
                'functions': visitor.functions
            }
        except Exception as e:
            return {'error': str(e)}

    def extract_from_javascript(self, file_path: Path) -> Dict[str, Any]:
        """Extract concepts from JavaScript/TypeScript source code."""
        concepts = {
            'classes': [],
            'interfaces': [],
            'functions': [],
            'imports': []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract class declarations
            class_pattern = r'(?:class|interface)\s+(\w+)(?:\s+extends\s+(\w+))?'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                parent_class = match.group(2)
                concepts['classes'].append({
                    'name': class_name,
                    'parent': parent_class,
                    'type': 'class' if 'class' in match.group(0) else 'interface'
                })

            # Extract function declarations
            func_pattern = r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:\([^)]*\)\s*)?=>|(\w+)\s*:\s*\([^)]*\)\s*=>)'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1) or match.group(2) or match.group(3)
                if func_name:
                    concepts['functions'].append({'name': func_name})

            # Extract imports
            import_pattern = r'import\s+.*?from\s+["\']([^"\']+)["\']'
            for match in re.finditer(import_pattern, content):
                concepts['imports'].append({'source': match.group(1)})

        except Exception as e:
            concepts['error'] = str(e)

        return concepts

    def build_ontology(self, extracted_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build ontological structure from extracted data."""
        ontology = {
            'concepts': {},
            'relationships': {
                'is_a': [],  # inheritance
                'part_of': [],  # composition
                'depends_on': [],  # dependencies
                'associates_with': []  # loose associations
            },
            'taxonomies': {}
        }

        all_classes = []
        all_functions = []
        all_imports = []

        # Collect all entities
        for data in extracted_data:
            if 'classes' in data:
                all_classes.extend(data['classes'])
            if 'functions' in data:
                all_functions.extend(data['functions'])
            if 'imports' in data:
                all_imports.extend(data['imports'])

        # Build concepts
        for cls in all_classes:
            if isinstance(cls, dict):
                concept_name = cls.get('name', str(cls))
                ontology['concepts'][concept_name] = {
                    'type': 'class',
                    'properties': cls
                }

                # Build inheritance relationships
                parent = cls.get('parent')
                if parent:
                    ontology['relationships']['is_a'].append({
                        'subject': concept_name,
                        'object': parent
                    })

        for func in all_functions:
            if isinstance(func, dict):
                func_name = func.get('name', str(func))
                ontology['concepts'][func_name] = {
                    'type': 'function',
                    'properties': func
                }

        return ontology

    def generate_mermaid_diagram(self, ontology: Dict[str, Any]) -> str:
        """Generate Mermaid diagram from ontology."""
        lines = ["graph TD"]

        # Add concepts as nodes
        for concept_name, concept_data in ontology['concepts'].items():
            concept_type = concept_data.get('type', 'concept')
            if concept_type == 'class':
                lines.append(f"    {concept_name}[({concept_name})]")
            else:
                lines.append(f"    {concept_name}[{concept_name}]")

        # Add relationships
        for rel_type, relationships in ontology['relationships'].items():
            for rel in relationships:
                subject = rel['subject']
                obj = rel['object']

                if rel_type == 'is_a':
                    lines.append(f"    {subject} --|> {obj}")
                elif rel_type == 'part_of':
                    lines.append(f"    {subject} --* {obj}")
                elif rel_type == 'depends_on':
                    lines.append(f"    {subject} -.-> {obj}")
                else:
                    lines.append(f"    {subject} --- {obj}")

        return "\n".join(lines)


class ClassVisitor(ast.NodeVisitor):
    """AST visitor for Python class analysis."""

    def __init__(self):
        self.classes = []
        self.inheritance = []
        self.imports = []
        self.functions = []

    def visit_ClassDef(self, node):
        class_info = {
            'name': node.name,
            'bases': [base.id for base in node.bases if hasattr(base, 'id')],
            'methods': [],
            'line_number': node.lineno
        }

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_info['methods'].append({
                    'name': item.name,
                    'args': [arg.arg for arg in item.args.args],
                    'line_number': item.lineno
                })

        self.classes.append(class_info)

        # Track inheritance
        for base in node.bases:
            if hasattr(base, 'id'):
                self.inheritance.append({
                    'child': node.name,
                    'parent': base.id
                })

        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname
            })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'line_number': node.lineno
        }
        self.functions.append(func_info)
        self.generic_visit(node)


def main():
    """Main function to run concept extraction."""
    if len(sys.argv) < 2:
        print("Usage: python extract_concepts.py <file_or_directory_path>")
        sys.exit(1)

    path = Path(sys.argv[1])
    extractor = ConceptExtractor()
    extracted_data = []

    if path.is_file():
        if path.suffix == '.py':
            data = extractor.extract_from_python(path)
            extracted_data.append(data)
        elif path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
            data = extractor.extract_from_javascript(path)
            extracted_data.append(data)
    elif path.is_dir():
        for file_path in path.rglob('*'):
            if file_path.is_file():
                if file_path.suffix == '.py':
                    data = extractor.extract_from_python(file_path)
                    extracted_data.append(data)
                elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                    data = extractor.extract_from_javascript(file_path)
                    extracted_data.append(data)

    ontology = extractor.build_ontology(extracted_data)

    # Output as JSON
    print(json.dumps(ontology, indent=2))

    # Also generate Mermaid diagram
    diagram = extractor.generate_mermaid_diagram(ontology)
    print("\n--- Mermaid Diagram ---")
    print(diagram)


if __name__ == "__main__":
    main()