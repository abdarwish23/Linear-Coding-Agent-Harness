"""
GitHub Configuration
====================

Configuration constants for GitHub integration.
These values are used in prompts and for project state management.
"""

import os

# Environment variables (must be set before running)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Default number of issues to create (can be overridden via command line)
DEFAULT_ISSUE_COUNT = 50

# Status labels (will be created as GitHub labels)
LABEL_STATUS_TODO = "status:todo"
LABEL_STATUS_IN_PROGRESS = "status:in-progress"
LABEL_STATUS_DONE = "status:done"

# Priority labels (map to Linear's 1-4 priority scale)
LABEL_PRIORITY_URGENT = "priority:urgent"     # Priority 1
LABEL_PRIORITY_HIGH = "priority:high"         # Priority 2
LABEL_PRIORITY_MEDIUM = "priority:medium"     # Priority 3
LABEL_PRIORITY_LOW = "priority:low"           # Priority 4

# Category labels (map to feature types)
LABEL_CATEGORY_FUNCTIONAL = "category:functional"
LABEL_CATEGORY_STYLE = "category:style"
LABEL_CATEGORY_INFRASTRUCTURE = "category:infrastructure"

# Meta label for tracking issue
LABEL_META = "meta"

# Local marker file to track GitHub project initialization
GITHUB_PROJECT_MARKER = ".github_project.json"

# Meta issue title for project tracking and session handoff
META_ISSUE_TITLE = "[META] Project Progress Tracker"

# Label definitions for creation (with colors and descriptions)
LABELS_TO_CREATE = [
    # Status labels
    {"name": LABEL_STATUS_TODO, "color": "0052CC", "description": "Work not yet started"},
    {"name": LABEL_STATUS_IN_PROGRESS, "color": "FFA500", "description": "Currently being worked on"},
    {"name": LABEL_STATUS_DONE, "color": "00B300", "description": "Completed and verified"},

    # Priority labels
    {"name": LABEL_PRIORITY_URGENT, "color": "D73A4A", "description": "Priority 1 - Foundational/urgent"},
    {"name": LABEL_PRIORITY_HIGH, "color": "FF6B6B", "description": "Priority 2 - High importance"},
    {"name": LABEL_PRIORITY_MEDIUM, "color": "FFA500", "description": "Priority 3 - Medium importance"},
    {"name": LABEL_PRIORITY_LOW, "color": "FBCA04", "description": "Priority 4 - Low priority/polish"},

    # Category labels
    {"name": LABEL_CATEGORY_FUNCTIONAL, "color": "1D76DB", "description": "Functional feature"},
    {"name": LABEL_CATEGORY_STYLE, "color": "C5DEF5", "description": "UI/styling feature"},
    {"name": LABEL_CATEGORY_INFRASTRUCTURE, "color": "5319E7", "description": "Infrastructure/tooling"},

    # Meta label
    {"name": LABEL_META, "color": "E99695", "description": "Meta/tracking issue"},
]
