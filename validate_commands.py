#!/usr/bin/env python3
"""
Slash Command Validator

Validates slash command markdown files against Claude Code requirements.
Requirements based on slash.md documentation.

Usage:
    python validate_commands.py [directory]

    Default directory: ./commands/
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

try:
    import frontmatter
except ImportError:
    print("Error: python-frontmatter is required. Install with: pip install python-frontmatter")
    sys.exit(1)


@dataclass
class ValidationResult:
    """Represents the validation result for a single command file."""
    file_path: str
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)


class SlashCommandValidator:
    """Validates slash command markdown files."""

    # Valid frontmatter fields per slash.md documentation
    VALID_FRONTMATTER_FIELDS = {
        'allowed-tools',
        'argument-hint',
        'description',
        'model',
        'disable-model-invocation'
    }

    # Valid model strings
    VALID_MODELS = {
        'claude-3-5-sonnet-20241022',
        'claude-3-5-haiku-20241022',
        'claude-opus-4-20250514',
        'claude-sonnet-4-5-20250929'
    }

    # Tool patterns for allowed-tools validation
    TOOL_PATTERNS = {
        r'^Read$',
        r'^Write$',
        r'^Edit$',
        r'^View$',
        r'^Grep$',
        r'^Glob$',
        r'^Task$',
        r'^TodoWrite$',
        r'^Create$',
        r'^WebFetch$',
        r'^WebSearch$',
        r'^Bash\(.+\)$',
        r'^SlashCommand.*$',
        r'^mcp__.+$'
    }

    def __init__(self, directory: str = "./commands/"):
        self.directory = Path(directory)
        self.results: List[ValidationResult] = []

    def validate_all(self) -> List[ValidationResult]:
        """Validate all markdown files in the directory."""
        if not self.directory.exists():
            print(f"Error: Directory '{self.directory}' does not exist.")
            sys.exit(1)

        markdown_files = list(self.directory.rglob("*.md"))

        # Exclude README files from validation
        markdown_files = [f for f in markdown_files if f.name.lower() != 'readme.md']

        print(f"Found {len(markdown_files)} slash command files to validate...\n")

        for file_path in markdown_files:
            result = self.validate_file(file_path)
            self.results.append(result)

        return self.results

    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single markdown file."""
        result = ValidationResult(file_path=str(file_path))

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter
            try:
                post = frontmatter.loads(content)
                metadata = post.metadata
                body = post.content
            except Exception as e:
                result.is_valid = False
                result.errors.append(f"Failed to parse frontmatter: {str(e)}")
                return result

            # Validate frontmatter
            self._validate_frontmatter(metadata, result)

            # Validate content
            self._validate_content(body, file_path, result)

            # Check for argument usage
            self._validate_arguments(metadata, body, result)

        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Unexpected error: {str(e)}")

        return result

    def _validate_frontmatter(self, metadata: Dict, result: ValidationResult):
        """Validate frontmatter fields."""
        if not metadata:
            result.warnings.append("No frontmatter found. Consider adding 'description' field.")
            return

        # Check for unknown fields
        unknown_fields = set(metadata.keys()) - self.VALID_FRONTMATTER_FIELDS
        if unknown_fields:
            result.warnings.append(f"Unknown frontmatter fields: {', '.join(unknown_fields)}")

        # Validate description (recommended)
        if 'description' not in metadata:
            result.warnings.append("Missing 'description' field (recommended for /help listing)")
        else:
            desc = metadata['description']
            # Handle both string and list (YAML can parse as list)
            if isinstance(desc, list):
                desc = ' '.join(str(d) for d in desc)
            desc = str(desc).strip()

            if not desc:
                result.errors.append("'description' field is empty")
                result.is_valid = False
            elif len(desc) > 200:
                result.warnings.append("'description' is very long (>200 chars). Consider shortening.")

        # Validate allowed-tools
        if 'allowed-tools' in metadata:
            self._validate_allowed_tools(metadata['allowed-tools'], result)

        # Validate model
        if 'model' in metadata:
            model = metadata['model']
            if model not in self.VALID_MODELS:
                result.warnings.append(f"Model '{model}' may not be valid. Check Claude documentation.")

        # Validate argument-hint
        if 'argument-hint' in metadata:
            hint = metadata['argument-hint']
            # Handle both string and list
            if isinstance(hint, list):
                hint = ' '.join(str(h) for h in hint)
            hint = str(hint).strip() if hint else ""
            if not hint:
                result.warnings.append("'argument-hint' is empty")

        # Validate disable-model-invocation
        if 'disable-model-invocation' in metadata:
            value = metadata['disable-model-invocation']
            if not isinstance(value, bool):
                result.errors.append("'disable-model-invocation' must be a boolean (true/false)")
                result.is_valid = False

    def _validate_allowed_tools(self, tools_value, result: ValidationResult):
        """Validate allowed-tools field."""
        if isinstance(tools_value, str):
            tools = [t.strip() for t in tools_value.split(',')]
        elif isinstance(tools_value, list):
            tools = tools_value
        else:
            result.errors.append("'allowed-tools' must be a string or list")
            result.is_valid = False
            return

        for tool in tools:
            tool = tool.strip()
            if not tool:
                continue

            # Check if tool matches any valid pattern
            valid = False
            for pattern in self.TOOL_PATTERNS:
                if re.match(pattern, tool):
                    valid = True
                    break

            if not valid:
                result.warnings.append(f"Tool '{tool}' may not be a valid tool name")

    def _validate_content(self, body: str, file_path: Path, result: ValidationResult):
        """Validate markdown content."""
        if not body or not body.strip():
            result.errors.append("File has no content after frontmatter")
            result.is_valid = False
            return

        # Check for bash command execution (! prefix)
        bash_commands = re.findall(r'!\`([^`]+)\`', body)
        if bash_commands:
            result.info.append(f"Found {len(bash_commands)} bash command execution(s)")

            # Check if Bash tool is allowed
            metadata_check = self._get_frontmatter_from_file(file_path)
            if metadata_check and 'allowed-tools' in metadata_check:
                allowed_tools = str(metadata_check['allowed-tools'])
                if 'Bash' not in allowed_tools:
                    result.errors.append("Bash commands found but 'Bash' not in allowed-tools")
                    result.is_valid = False

        # Check for file references (@ prefix)
        file_refs = re.findall(r'@([\w\-./]+)', body)
        if file_refs:
            result.info.append(f"Found {len(file_refs)} file reference(s)")

        # Check for thinking mode keywords
        thinking_keywords = ['<ultrathink>', '<megaexpertise>', '<think>', '<thinking>']
        if any(keyword in body for keyword in thinking_keywords):
            result.info.append("Extended thinking mode detected")

    def _validate_arguments(self, metadata: Dict, body: str, result: ValidationResult):
        """Validate argument usage consistency."""
        # Check for $ARGUMENTS usage
        has_arguments = '$ARGUMENTS' in body

        # Check for positional arguments ($1, $2, etc.)
        positional_args = re.findall(r'\$(\d+)', body)
        has_positional = len(positional_args) > 0

        # Both types shouldn't be mixed
        if has_arguments and has_positional:
            result.warnings.append("Mixed usage of $ARGUMENTS and positional args ($1, $2). Use one style.")

        # If arguments are used, suggest argument-hint
        if (has_arguments or has_positional) and 'argument-hint' not in metadata:
            result.warnings.append("Arguments detected but no 'argument-hint' in frontmatter")

        # If argument-hint exists but no arguments used
        if 'argument-hint' in metadata and not has_arguments and not has_positional:
            result.warnings.append("'argument-hint' specified but no $ARGUMENTS or $N found in content")

    def _get_frontmatter_from_file(self, file_path: Path) -> Optional[Dict]:
        """Helper to get frontmatter from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                return post.metadata
        except:
            return None

    def print_results(self):
        """Print validation results in a readable format."""
        total = len(self.results)
        valid = sum(1 for r in self.results if r.is_valid)
        invalid = total - valid

        print("\n" + "=" * 80)
        print("VALIDATION RESULTS")
        print("=" * 80)
        print(f"Total files: {total}")
        print(f"Valid: {valid}")
        print(f"Invalid: {invalid}")
        print("=" * 80 + "\n")

        # Print invalid files first
        if invalid > 0:
            print("❌ INVALID FILES:\n")
            for result in self.results:
                if not result.is_valid:
                    self._print_file_result(result)

        # Print valid files with warnings
        has_warnings = [r for r in self.results if r.is_valid and r.warnings]
        if has_warnings:
            print("\n⚠️  VALID FILES WITH WARNINGS:\n")
            for result in has_warnings:
                self._print_file_result(result)

        # Print fully valid files
        fully_valid = [r for r in self.results if r.is_valid and not r.warnings]
        if fully_valid:
            print(f"\n✅ FULLY VALID FILES ({len(fully_valid)}):\n")
            for result in fully_valid:
                print(f"  • {result.file_path}")
                if result.info:
                    for info in result.info:
                        print(f"      ℹ️  {info}")

        print("\n" + "=" * 80)

        return 0 if invalid == 0 else 1

    def _print_file_result(self, result: ValidationResult):
        """Print detailed results for a single file."""
        status = "✅" if result.is_valid else "❌"
        print(f"{status} {result.file_path}")

        for error in result.errors:
            print(f"    ❌ ERROR: {error}")

        for warning in result.warnings:
            print(f"    ⚠️  WARNING: {warning}")

        for info in result.info:
            print(f"    ℹ️  INFO: {info}")

        print()


def main():
    """Main entry point."""
    directory = sys.argv[1] if len(sys.argv) > 1 else "./commands/"

    print(f"Slash Command Validator")
    print(f"Directory: {directory}\n")

    validator = SlashCommandValidator(directory)
    validator.validate_all()
    exit_code = validator.print_results()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
