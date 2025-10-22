#!/usr/bin/env python3
"""
Validates that all slash commands in the repository follow the Claude Code standard format.

Standard requirements:
- Markdown files with .md extension
- Optional YAML frontmatter with specific fields
- Proper content structure
- Valid tool specifications in allowed-tools

Usage: python validate_slash_commands.py [--fix] [--verbose]
"""

import os
import sys
import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ValidationStatus(Enum):
    """Validation result status."""
    PASS = "✓"
    FAIL = "✗"
    WARNING = "⚠"
    INFO = "ℹ"


@dataclass
class ValidationResult:
    """Result of a validation check."""
    status: ValidationStatus
    message: str
    file_path: str
    line_number: Optional[int] = None


@dataclass
class CommandFile:
    """Represents a slash command file."""
    path: Path
    name: str
    content: str
    frontmatter: Optional[Dict[str, Any]] = None
    body: str = ""


class SlashCommandValidator:
    """Validates slash command files against Claude Code standards."""
    
    # Valid frontmatter fields according to documentation
    VALID_FRONTMATTER_FIELDS = {
        'allowed-tools',
        'argument-hint', 
        'description',
        'model',
        'disable-model-invocation'
    }
    
    # Known Claude models
    VALID_MODELS = {
        'claude-3-5-sonnet-20241022',
        'claude-3-5-haiku-20241022',
        'claude-3-opus-20240229',
        'claude-3-sonnet-20240229',
        'claude-3-haiku-20240307',
    }
    
    # Common tool patterns
    TOOL_PATTERNS = {
        'bash': re.compile(r'Bash\(([^)]*)\)'),
        'edit': re.compile(r'Edit'),
        'view': re.compile(r'View'),
        'create': re.compile(r'Create'),
        'search': re.compile(r'Search'),
        'grep': re.compile(r'Grep'),
        'glob': re.compile(r'Glob'),
    }
    
    def __init__(self, root_dir: Path, verbose: bool = False):
        """Initialize the validator."""
        self.root_dir = root_dir
        self.verbose = verbose
        self.results: List[ValidationResult] = []
        
    def validate_all(self) -> Tuple[int, int, int]:
        """
        Validate all command files in the repository.
        
        Returns:
            Tuple of (passed, warnings, failed) counts
        """
        commands_dir = self.root_dir / "commands"
        
        if not commands_dir.exists():
            self.add_result(ValidationResult(
                ValidationStatus.FAIL,
                "Commands directory not found",
                str(commands_dir)
            ))
            return 0, 0, 1
        
        # Find all .md files in commands directory
        command_files = list(commands_dir.rglob("*.md"))
        
        if not command_files:
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                "No command files found",
                str(commands_dir)
            ))
            return 0, 1, 0
        
        for file_path in command_files:
            # Skip README files
            if file_path.name.lower() == "readme.md":
                continue
                
            self.validate_command_file(file_path)
        
        # Count results
        passed = sum(1 for r in self.results if r.status == ValidationStatus.PASS)
        warnings = sum(1 for r in self.results if r.status == ValidationStatus.WARNING)
        failed = sum(1 for r in self.results if r.status == ValidationStatus.FAIL)
        
        return passed, warnings, failed
    
    def validate_command_file(self, file_path: Path) -> None:
        """Validate a single command file."""
        try:
            command = self.load_command_file(file_path)
            
            # Validate file name
            self.validate_file_name(command)
            
            # Validate frontmatter
            self.validate_frontmatter(command)
            
            # Validate content
            self.validate_content(command)
            
            # If no issues found, mark as passed
            if not any(r.file_path == str(file_path) for r in self.results):
                self.add_result(ValidationResult(
                    ValidationStatus.PASS,
                    f"Command '{command.name}' is valid",
                    str(file_path)
                ))
                
        except Exception as e:
            self.add_result(ValidationResult(
                ValidationStatus.FAIL,
                f"Error processing file: {e}",
                str(file_path)
            ))
    
    def load_command_file(self, file_path: Path) -> CommandFile:
        """Load and parse a command file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        command = CommandFile(
            path=file_path,
            name=file_path.stem,
            content=content
        )
        
        # Check for frontmatter
        if content.startswith('---'):
            try:
                # Find the closing ---
                end_match = re.search(r'\n---\n', content[3:])
                if end_match:
                    frontmatter_text = content[4:end_match.start() + 3]
                    command.frontmatter = yaml.safe_load(frontmatter_text)
                    command.body = content[end_match.end() + 4:]
                else:
                    command.body = content
            except yaml.YAMLError as e:
                self.add_result(ValidationResult(
                    ValidationStatus.FAIL,
                    f"Invalid YAML frontmatter: {e}",
                    str(file_path)
                ))
        else:
            command.body = content
        
        return command
    
    def validate_file_name(self, command: CommandFile) -> None:
        """Validate command file naming conventions."""
        name = command.name
        
        # Check for valid characters in command name
        if not re.match(r'^[a-z0-9-]+$', name):
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                f"Command name '{name}' should use lowercase letters, numbers, and hyphens only",
                str(command.path)
            ))
    
    def validate_frontmatter(self, command: CommandFile) -> None:
        """Validate frontmatter structure and fields."""
        if not command.frontmatter:
            # Frontmatter is optional, but recommended for discoverability
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                "No frontmatter found - consider adding 'description' for better discoverability",
                str(command.path)
            ))
            return
        
        # Check for unknown fields
        unknown_fields = set(command.frontmatter.keys()) - self.VALID_FRONTMATTER_FIELDS
        if unknown_fields:
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                f"Unknown frontmatter fields: {', '.join(unknown_fields)}",
                str(command.path)
            ))
        
        # Validate specific fields
        self.validate_allowed_tools(command)
        self.validate_description(command)
        self.validate_model(command)
        self.validate_argument_hint(command)
        
    def validate_allowed_tools(self, command: CommandFile) -> None:
        """Validate the allowed-tools field."""
        if 'allowed-tools' not in command.frontmatter:
            # Check if body contains bash commands or file references
            if '!`' in command.body or '@' in command.body:
                self.add_result(ValidationResult(
                    ValidationStatus.WARNING,
                    "Command uses bash commands or file references but no 'allowed-tools' specified",
                    str(command.path)
                ))
            return
        
        tools = command.frontmatter['allowed-tools']
        
        if not isinstance(tools, str):
            self.add_result(ValidationResult(
                ValidationStatus.FAIL,
                f"'allowed-tools' must be a string, got {type(tools).__name__}",
                str(command.path)
            ))
            return
        
        # Parse and validate tool specifications
        tool_list = [t.strip() for t in tools.split(',')]
        for tool in tool_list:
            if not self.is_valid_tool_spec(tool):
                self.add_result(ValidationResult(
                    ValidationStatus.WARNING,
                    f"Potentially invalid tool specification: '{tool}'",
                    str(command.path)
                ))
    
    def is_valid_tool_spec(self, tool_spec: str) -> bool:
        """Check if a tool specification is valid."""
        # Common valid patterns
        if tool_spec in ['Edit', 'View', 'Create', 'Search', 'Grep', 'Glob', 'Read', 'MultiEdit']:
            return True
        
        # Bash command patterns
        if tool_spec.startswith('Bash(') and tool_spec.endswith(')'):
            return True
        
        # Other patterns (can be extended)
        return False
    
    def validate_description(self, command: CommandFile) -> None:
        """Validate the description field."""
        if 'description' not in command.frontmatter:
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                "No 'description' in frontmatter - required for SlashCommand tool discovery",
                str(command.path)
            ))
            return
        
        description = command.frontmatter['description']
        
        if not isinstance(description, str):
            self.add_result(ValidationResult(
                ValidationStatus.FAIL,
                f"'description' must be a string, got {type(description).__name__}",
                str(command.path)
            ))
            return
        
        if len(description) < 10:
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                "Description is very short - consider adding more detail",
                str(command.path)
            ))
        
        if len(description) > 200:
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                "Description is very long - consider making it more concise",
                str(command.path)
            ))
    
    def validate_model(self, command: CommandFile) -> None:
        """Validate the model field if present."""
        if 'model' not in command.frontmatter:
            return
        
        model = command.frontmatter['model']
        
        if not isinstance(model, str):
            self.add_result(ValidationResult(
                ValidationStatus.FAIL,
                f"'model' must be a string, got {type(model).__name__}",
                str(command.path)
            ))
            return
        
        # Check if it's a known model
        if model not in self.VALID_MODELS:
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                f"Unknown model '{model}' - may be outdated or custom",
                str(command.path)
            ))
    
    def validate_argument_hint(self, command: CommandFile) -> None:
        """Validate the argument-hint field if present."""
        if 'argument-hint' not in command.frontmatter:
            # Check if command uses arguments
            if '$ARGUMENTS' in command.body or '$1' in command.body:
                self.add_result(ValidationResult(
                    ValidationStatus.INFO,
                    "Command uses arguments - consider adding 'argument-hint' for better UX",
                    str(command.path)
                ))
            return
        
        hint = command.frontmatter['argument-hint']
        
        if not isinstance(hint, str):
            self.add_result(ValidationResult(
                ValidationStatus.FAIL,
                f"'argument-hint' must be a string, got {type(hint).__name__}",
                str(command.path)
            ))
    
    def validate_content(self, command: CommandFile) -> None:
        """Validate the command content/body."""
        body = command.body.strip()
        
        if not body:
            self.add_result(ValidationResult(
                ValidationStatus.FAIL,
                "Command has no content body",
                str(command.path)
            ))
            return
        
        # Check for common patterns and best practices
        self.check_bash_commands(command)
        self.check_file_references(command)
        self.check_argument_usage(command)
    
    def check_bash_commands(self, command: CommandFile) -> None:
        """Check bash command usage."""
        bash_pattern = re.compile(r'!\`([^`]+)\`')
        bash_commands = bash_pattern.findall(command.body)
        
        if bash_commands and 'allowed-tools' in command.frontmatter:
            tools = command.frontmatter['allowed-tools']
            if 'Bash' not in tools:
                self.add_result(ValidationResult(
                    ValidationStatus.FAIL,
                    "Command uses bash execution (!`) but 'Bash' not in allowed-tools",
                    str(command.path)
                ))
    
    def check_file_references(self, command: CommandFile) -> None:
        """Check file reference patterns."""
        # Look for @filename patterns
        file_refs = re.findall(r'@[\w/.-]+', command.body)
        
        if file_refs and self.verbose:
            self.add_result(ValidationResult(
                ValidationStatus.INFO,
                f"Command references {len(file_refs)} file(s)",
                str(command.path)
            ))
    
    def check_argument_usage(self, command: CommandFile) -> None:
        """Check argument placeholder usage."""
        has_arguments = '$ARGUMENTS' in command.body
        has_positional = any(f'${i}' in command.body for i in range(1, 10))
        
        if has_arguments and has_positional:
            self.add_result(ValidationResult(
                ValidationStatus.WARNING,
                "Command uses both $ARGUMENTS and positional arguments - consider using one pattern",
                str(command.path)
            ))
    
    def add_result(self, result: ValidationResult) -> None:
        """Add a validation result."""
        self.results.append(result)
        if self.verbose or result.status in [ValidationStatus.FAIL, ValidationStatus.WARNING]:
            print(f"{result.status.value} {result.file_path}: {result.message}")
    
    def print_summary(self) -> None:
        """Print a summary of validation results."""
        passed = sum(1 for r in self.results if r.status == ValidationStatus.PASS)
        warnings = sum(1 for r in self.results if r.status == ValidationStatus.WARNING)
        failed = sum(1 for r in self.results if r.status == ValidationStatus.FAIL)
        info = sum(1 for r in self.results if r.status == ValidationStatus.INFO)
        
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"✓ Passed:   {passed}")
        print(f"⚠ Warnings: {warnings}")
        print(f"✗ Failed:   {failed}")
        if info > 0:
            print(f"ℹ Info:     {info}")
        print("=" * 60)
        
        if failed > 0:
            print("\nFAILED CHECKS:")
            for result in self.results:
                if result.status == ValidationStatus.FAIL:
                    print(f"  - {result.file_path}")
                    print(f"    {result.message}")
        
        if warnings > 0 and self.verbose:
            print("\nWARNINGS:")
            for result in self.results:
                if result.status == ValidationStatus.WARNING:
                    print(f"  - {result.file_path}")
                    print(f"    {result.message}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate slash commands against Claude Code standards"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation information'
    )
    parser.add_argument(
        '--path', '-p',
        type=str,
        default='.',
        help='Path to the repository root (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Find repository root
    root_path = Path(args.path).resolve()
    
    # Look for commands directory
    if not (root_path / "commands").exists():
        # Try to find it in parent directories
        for parent in root_path.parents:
            if (parent / "commands").exists():
                root_path = parent
                break
    
    print(f"Validating slash commands in: {root_path}")
    print("=" * 60)
    
    # Run validation
    validator = SlashCommandValidator(root_path, verbose=args.verbose)
    passed, warnings, failed = validator.validate_all()
    
    # Print summary
    validator.print_summary()
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    elif warnings > 0:
        sys.exit(0)  # Warnings don't fail the check
    else:
        print("\n✅ All slash commands are valid!")
        sys.exit(0)


if __name__ == '__main__':
    main()
