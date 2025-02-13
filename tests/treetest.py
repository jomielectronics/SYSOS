import os

def tree(directory, prefix=""):
	"""Recursively prints a tree-like structure of the directory"""
	entries = sorted(os.listdir(directory))  # Sort alphabetically
	entries = [e for e in entries if not e.startswith(".")]  # Hide hidden files
	last_index = len(entries) - 1  # Find last element for proper formatting

	for i, entry in enumerate(entries):
		path = os.path.join(directory, entry)
		connector = "\u2570" if i == last_index else "\u251c\u2500"  # Last entry uses └──

		print(prefix + connector + entry)

		# If it's a directory, recurse with increased indentation
		if os.path.isdir(path):
			new_prefix = prefix + ("    " if i == last_index else "│   ")
			tree(path, new_prefix)

# Example usage:
tree("/Users/Micah/Documents/Tech/Coding/Programs/Python/SYSOS")