#!/usr/bin/env python3
"""
Generate a markdown tree of folders only (no files)
"""
import os
import argparse
from pathlib import Path
from typing import List, Set

def generate_folder_tree(
		root_path: str,
		prefix: str = "",
		is_last: bool = True,
		ignore_dirs: Set[str] = None,
		max_depth: int = None,
		current_depth: int = 0
) -> List[str]:
	"""
	Generate a markdown tree structure of folders only

	Args:
		root_path: Root directory path
		prefix: Prefix for tree formatting
		is_last: Whether this is the last item in its level
		ignore_dirs: Set of directory names to ignore
		max_depth: Maximum depth to traverse (None for unlimited)
		current_depth: Current depth level

	Returns:
		List of formatted tree lines
	"""
	if ignore_dirs is None:
		ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv',
		               '.idea', '.vscode', '__MACOSX', '.DS_Store'}

	lines = []
	path = Path(root_path)

	# Get folder name
	folder_name = path.name if path.name else str(path)

	# Add current folder
	if current_depth == 0:
		lines.append(f"{folder_name}/")
	else:
		connector = "└── " if is_last else "├── "
		lines.append(f"{prefix}{connector}{folder_name}/")

	# Check max depth
	if max_depth is not None and current_depth >= max_depth:
		return lines

	# Get subdirectories, sorted
	try:
		subdirs = [d for d in path.iterdir()
		           if d.is_dir() and d.name not in ignore_dirs]
		subdirs.sort(key=lambda x: x.name.lower())
	except PermissionError:
		return lines

	# Process each subdirectory
	for idx, subdir in enumerate(subdirs):
		is_last_subdir = (idx == len(subdirs) - 1)

		# Update prefix for children
		if current_depth == 0:
			new_prefix = ""
		else:
			extension = "    " if is_last else "│   "
			new_prefix = prefix + extension

		# Recursively process subdirectory
		sublines = generate_folder_tree(
			str(subdir),
			new_prefix,
			is_last_subdir,
			ignore_dirs,
			max_depth,
			current_depth + 1
		)
		lines.extend(sublines)

	return lines


def main():
	"""Main function with CLI interface"""
	parser = argparse.ArgumentParser(
		description='Generate a markdown tree of folders only',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  %(prog)s /path/to/directory
  %(prog)s . --max-depth 2
  %(prog)s /path/to/dir --ignore .git node_modules --output tree.md
        """
	)

	parser.add_argument(
		'path',
		nargs='?',
		default='.',
		help='Root directory path (default: current directory)'
	)

	parser.add_argument(
		'--max-depth',
		type=int,
		default=None,
		help='Maximum depth to traverse (default: unlimited)'
	)

	parser.add_argument(
		'--ignore',
		nargs='+',
		default=[],
		help='Additional directories to ignore'
	)

	parser.add_argument(
		'--output',
		'-o',
		help='Output file (default: print to stdout)'
	)

	parser.add_argument(
		'--include-hidden',
		action='store_true',
		help='Include hidden directories (starting with .)'
	)

	args = parser.parse_args()

	# Prepare ignore set
	default_ignore = {'.git', '__pycache__', 'node_modules', '.venv', 'venv',
	                  '.idea', '.vscode', '__MACOSX'}

	if not args.include_hidden:
		# Add all hidden dirs to ignore (except explicitly allowed ones)
		ignore_dirs = default_ignore | set(args.ignore)
	else:
		# Only ignore explicitly mentioned dirs
		ignore_dirs = set(args.ignore) if args.ignore else set()

	# Generate tree
	tree_lines = generate_folder_tree(
		args.path,
		ignore_dirs=ignore_dirs,
		max_depth=args.max_depth
	)

	# Format as markdown
	markdown = "```\n" + "\n".join(tree_lines) + "\n```"

	# Output
	if args.output:
		with open(args.output, 'w', encoding='utf-8') as f:
			f.write(markdown)
		print(f"Folder tree written to {args.output}")
	else:
		print(markdown)


if __name__ == '__main__':
	main()