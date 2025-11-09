#!/usr/bin/env python3
"""
Slash Command Auto-Fixer

Automatically fixes common issues in slash command markdown files.

Usage:
    python fix_commands.py [directory] [--dry-run]

    --dry-run: Show what would be fixed without making changes
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Tuple

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


class SlashCommandFixer:
    """Automatically fixes common issues in slash command files."""

    def __init__(self, directory: str = "./commands/", dry_run: bool = False):
        self.directory = Path(directory)
        self.dry_run = dry_run
        self.fixes_applied = []

    def fix_all(self) -> List[Tuple[str, List[str]]]:
        """Fix all markdown files in the directory."""
        if not self.directory.exists():
            print(f"Error: Directory '{self.directory}' does not exist.")
            sys.exit(1)

        markdown_files = list(self.directory.rglob("*.md"))
        markdown_files = [f for f in markdown_files if f.name.lower() != 'readme.md']

        print(f"Found {len(markdown_files)} slash command files to check...\n")

        for file_path in markdown_files:
            fixes = self.fix_file(file_path)
            if fixes:
                self.fixes_applied.append((str(file_path), fixes))

        return self.fixes_applied

    def fix_file(self, file_path: Path) -> List[str]:
        """Fix a single markdown file and return list of fixes applied."""
        fixes = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Try to parse frontmatter
            try:
                post = frontmatter.loads(content)
                metadata = post.metadata
                body = post.content
            except Exception:
                # If frontmatter parsing fails, try to fix it
                content, frontmatter_fixes = self._fix_frontmatter_syntax(content)
                fixes.extend(frontmatter_fixes)

                # Try parsing again
                try:
                    post = frontmatter.loads(content)
                    metadata = post.metadata
                    body = post.content
                except Exception as e:
                    fixes.append(f"Could not parse frontmatter: {str(e)}")
                    return fixes

            # Apply fixes to metadata and body
            new_metadata, metadata_fixes = self._fix_metadata(metadata, body)
            fixes.extend(metadata_fixes)

            # Check if bash commands need allowed-tools update
            bash_fixes = self._check_bash_permissions(metadata, body)
            if bash_fixes:
                fixes.extend(bash_fixes)
                new_metadata = self._add_bash_to_allowed_tools(new_metadata)

            # Reconstruct the file if changes were made
            if fixes:
                new_post = frontmatter.Post(body, **new_metadata)
                new_content = frontmatter.dumps(new_post)

                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

        except Exception as e:
            fixes.append(f"Unexpected error: {str(e)}")

        return fixes

    def _fix_frontmatter_syntax(self, content: str) -> Tuple[str, List[str]]:
        """Fix common YAML frontmatter syntax issues."""
        fixes = []

        # Extract frontmatter section
        fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not fm_match:
            return content, fixes

        fm_content = fm_match.group(1)
        body = fm_match.group(2)

        # Fix unquoted square brackets in values
        def quote_brackets(match):
            key = match.group(1)
            value = match.group(2)
            if '[' in value and not (value.startswith('"') or value.startswith("'")):
                fixes.append(f"Quoted square brackets in '{key}' field")
                return f'{key}: "{value}"'
            return match.group(0)

        fm_content = re.sub(r'^(\w[\w-]*?):\s*(.+?)$', quote_brackets, fm_content, flags=re.MULTILINE)

        # Reconstruct
        new_content = f"---\n{fm_content}\n---\n{body}"
        return new_content, fixes

    def _fix_metadata(self, metadata: dict, body: str) -> Tuple[dict, List[str]]:
        """Fix metadata issues and return new metadata with fixes applied."""
        fixes = []
        new_metadata = metadata.copy()

        # Fix description if it's a list
        if 'description' in new_metadata and isinstance(new_metadata['description'], list):
            new_metadata['description'] = ' '.join(str(d) for d in new_metadata['description'])
            fixes.append("Converted description from list to string")

        # Fix argument-hint if it's a list
        if 'argument-hint' in new_metadata and isinstance(new_metadata['argument-hint'], list):
            new_metadata['argument-hint'] = ' '.join(str(h) for h in new_metadata['argument-hint'])
            fixes.append("Converted argument-hint from list to string")

        # Add argument-hint if arguments are used but hint is missing
        has_arguments = '$ARGUMENTS' in body
        positional_args = re.findall(r'\$(\d+)', body)
        has_positional = len(positional_args) > 0

        if (has_arguments or has_positional) and 'argument-hint' not in new_metadata:
            if has_arguments:
                new_metadata['argument-hint'] = "[args]"
                fixes.append("Added generic argument-hint for $ARGUMENTS usage")
            elif has_positional:
                max_arg = max(int(n) for n in positional_args)
                hint_parts = ' '.join([f'[arg{i}]' for i in range(1, max_arg + 1)])
                new_metadata['argument-hint'] = hint_parts
                fixes.append(f"Added argument-hint for positional arguments ($1-${max_arg})")

        return new_metadata, fixes

    def _check_bash_permissions(self, metadata: dict, body: str) -> List[str]:
        """Check if bash commands are used without permissions."""
        bash_commands = re.findall(r'!\`([^`]+)\`', body)
        if not bash_commands:
            return []

        # Check if Bash is in allowed-tools
        if 'allowed-tools' not in metadata:
            return ["Bash commands found but no allowed-tools defined"]

        allowed_tools = metadata.get('allowed-tools', '')
        if isinstance(allowed_tools, list):
            allowed_tools = ', '.join(allowed_tools)

        if 'Bash' not in allowed_tools:
            return ["Bash commands found but Bash not in allowed-tools"]

        return []

    def _add_bash_to_allowed_tools(self, metadata: dict) -> dict:
        """Add Bash to allowed-tools if needed."""
        new_metadata = metadata.copy()

        if 'allowed-tools' not in new_metadata:
            new_metadata['allowed-tools'] = 'Bash'
        else:
            tools = new_metadata['allowed-tools']
            if isinstance(tools, list):
                tools.append('Bash')
                new_metadata['allowed-tools'] = tools
            else:
                new_metadata['allowed-tools'] = f"{tools}, Bash"

        return new_metadata

    def print_results(self):
        """Print results of fixes applied."""
        print("\n" + "=" * 80)
        print("AUTO-FIX RESULTS")
        print("=" * 80)
        print(f"Total files checked: {len(list(self.directory.rglob('*.md'))) - 1}")  # -1 for README
        print(f"Files fixed: {len(self.fixes_applied)}")
        if self.dry_run:
            print("\n🔍 DRY RUN MODE - No changes were made")
        print("=" * 80 + "\n")

        if not self.fixes_applied:
            print("✅ No fixes needed - all files are good!\n")
            return

        for file_path, fixes in self.fixes_applied:
            print(f"{'🔍' if self.dry_run else '🔧'} {file_path}")
            for fix in fixes:
                print(f"    {'[DRY RUN] ' if self.dry_run else ''}✓ {fix}")
            print()

        if self.dry_run:
            print("💡 Run without --dry-run to apply these fixes\n")
        else:
            print("✅ All fixes applied successfully!\n")
            print("⚠️  Remember to:")
            print("    1. Review the changes")
            print("    2. Run the validator: python validate_commands.py")
            print("    3. Test your commands\n")

        print("=" * 80)


def main():
    """Main entry point."""
    dry_run = '--dry-run' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != '--dry-run']
    directory = args[0] if args else "./commands/"

    mode_text = "DRY RUN - " if dry_run else ""
    print(f"Slash Command Auto-Fixer ({mode_text})")
    print(f"Directory: {directory}\n")

    fixer = SlashCommandFixer(directory, dry_run=dry_run)
    fixer.fix_all()
    fixer.print_results()


if __name__ == "__main__":
    main()
