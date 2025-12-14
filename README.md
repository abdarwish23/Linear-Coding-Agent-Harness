# Autonomous Coding Agent Demo (GitHub-Integrated)

A minimal harness demonstrating long-running autonomous coding with the Claude Agent SDK. This demo implements a two-agent pattern (initializer + coding agent) with **GitHub Issues as the core project management system** for tracking all work.

## Key Features

- **GitHub Integration**: All work is tracked as GitHub issues, not local files
- **Real-time Visibility**: Watch agent progress directly in your GitHub repository
- **Session Handoff**: Agents communicate via GitHub issue comments, not text files
- **Two-Agent Pattern**: Initializer creates issues with labels, coding agents implement them
- **Browser Testing**: Puppeteer MCP for UI verification
- **Claude Opus 4.5**: Uses Claude's most capable model by default

## Prerequisites

### 1. Install Claude Code CLI and Python SDK

```bash
# Install Claude Code CLI (latest version required)
npm install -g @anthropic-ai/claude-code

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Set Up Authentication

You need two authentication tokens:

**Claude Code OAuth Token:**
```bash
# Generate the token using Claude Code CLI
claude setup-token

# Set the environment variable
export CLAUDE_CODE_OAUTH_TOKEN='your-oauth-token-here'
```

**GitHub Personal Access Token:**
```bash
# Create token at: https://github.com/settings/tokens
# Select "Personal access tokens (classic)"
# Required scopes:
#   - repo (Full control of private repositories)
#   - project (Full control of projects)

export GITHUB_TOKEN='ghp_xxxxxxxxxxxxx'
```

### 3. Create a GitHub Repository

Before running, you need a GitHub repository for the project:

```bash
# Create a new repo on GitHub or use an existing one
# The agent will need the repo in format: owner/repo-name
# For example: username/my-awesome-project
```

### 4. Verify Installation

```bash
claude --version  # Should be latest version
pip show claude-code-sdk  # Check SDK is installed
npx @modelcontextprotocol/server-github --version  # Check GitHub MCP
```

## Quick Start

```bash
# The agent will ask for your GitHub repository (owner/repo-name)
python autonomous_agent_demo.py --project-dir ./my_project
```

For testing with limited iterations:
```bash
python autonomous_agent_demo.py --project-dir ./my_project --max-iterations 3
```

## How It Works

### GitHub-Centric Workflow

```
┌────────────────────────────────────────────────────────────────┐
│                    GITHUB-INTEGRATED WORKFLOW                  │
├────────────────────────────────────────────────────────────────┤
│  app_spec.txt ──► Initializer Agent ──► GitHub Issues (50)    │
│                                              │                  │
│                    ┌─────────────────────────▼──────────────┐  │
│                    │        GITHUB REPOSITORY               │  │
│                    │  ┌─────────────────────────────────┐   │  │
│                    │  │ Issue #1: Auth - Login flow     │   │  │
│                    │  │ Labels: status:todo             │   │  │
│                    │  │         priority:urgent         │   │  │
│                    │  │         category:functional     │   │  │
│                    │  │ Comments: [session notes]       │   │  │
│                    │  └─────────────────────────────────┘   │  │
│                    └────────────────────────────────────────┘  │
│                                              │                  │
│                    Coding Agent queries GitHub                 │
│                    ├── List issues with status:todo            │
│                    ├── Update labels to status:in-progress     │
│                    ├── Implement & test with Puppeteer         │
│                    ├── Add comment with implementation notes   │
│                    └── Update labels to status:done            │
└────────────────────────────────────────────────────────────────┘
```

### Two-Agent Pattern

1. **Initializer Agent (Session 1):**
   - Reads `app_spec.txt`
   - Verifies GitHub repository access
   - Creates workflow labels (status, priority, category)
   - Creates 50 GitHub issues with detailed test steps
   - Creates a META issue for session tracking
   - Sets up project structure, `init.sh`, and git

2. **Coding Agent (Sessions 2+):**
   - Queries GitHub for issues with label `status:todo`
   - Runs verification tests on previously completed features
   - Claims issue (label: `status:todo` → `status:in-progress`)
   - Implements the feature
   - Tests via Puppeteer browser automation
   - Adds implementation comment to issue
   - Marks complete (label: `status:in-progress` → `status:done`)
   - Updates META issue with session summary

### Session Handoff via GitHub

Instead of local text files, agents communicate through:
- **Issue Comments**: Implementation details, blockers, context
- **META Issue**: Session summaries and handoff notes
- **Issue Labels**: `status:todo` / `status:in-progress` / `status:done` workflow

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code OAuth token (from `claude setup-token`) | Yes |
| `GITHUB_TOKEN` | GitHub Personal Access Token (PAT) | Yes |

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project-dir` | Directory for the project | `./autonomous_demo_project` |
| `--max-iterations` | Max agent iterations | Unlimited |
| `--model` | Claude model to use | `claude-opus-4-5-20251101` |

## Project Structure

```
github-agent-harness/
├── autonomous_agent_demo.py  # Main entry point
├── agent.py                  # Agent session logic
├── client.py                 # Claude SDK + MCP client configuration
├── security.py               # Bash command allowlist and validation
├── progress.py               # Progress tracking utilities
├── prompts.py                # Prompt loading utilities
├── github_config.py          # GitHub configuration constants
├── prompts/
│   ├── app_spec.txt          # Application specification
│   ├── initializer_prompt.md # First session prompt (creates GitHub issues)
│   └── coding_prompt.md      # Continuation session prompt (works issues)
└── requirements.txt          # Python dependencies
```

## Generated Project Structure

After running, your project directory will contain:

```
my_project/
├── .github_project.json      # GitHub project state (marker file)
├── app_spec.txt              # Copied specification
├── init.sh                   # Environment setup script
├── .claude_settings.json     # Security settings
└── [application files]       # Generated application code
```

## MCP Servers Used

| Server | Transport | Purpose |
|--------|-----------|---------|
| **GitHub** | stdio | Issue tracking, project management, labels |
| **Puppeteer** | stdio | Browser automation for UI testing |

## Security Model

This demo uses defense-in-depth security (see `security.py` and `client.py`):

1. **OS-level Sandbox:** Bash commands run in an isolated environment
2. **Filesystem Restrictions:** File operations restricted to project directory
3. **Bash Allowlist:** Only specific commands permitted (npm, node, git, etc.)
4. **MCP Permissions:** Tools explicitly allowed in security settings

## GitHub Setup

Before running, ensure you have:

1. A GitHub repository with appropriate access
2. A Personal Access Token with `repo` and `project` scopes
3. The agent will automatically detect your repository or ask for it

The initializer agent will create:
- Workflow labels (status, priority, category)
- 50 feature issues based on `app_spec.txt`
- 1 META issue for session tracking and handoff

All subsequent coding agents will work from these GitHub issues.

## GitHub Labels

The agent uses a label-based workflow:

**Status Labels:**
- `status:todo` - Work not yet started (blue)
- `status:in-progress` - Currently being worked on (orange)
- `status:done` - Completed and verified (green)

**Priority Labels:**
- `priority:urgent` - Priority 1 - Foundational/urgent (red)
- `priority:high` - Priority 2 - High importance (red-orange)
- `priority:medium` - Priority 3 - Medium importance (orange)
- `priority:low` - Priority 4 - Low priority/polish (yellow)

**Category Labels:**
- `category:functional` - Functional feature (blue)
- `category:style` - UI/styling feature (light blue)
- `category:infrastructure` - Infrastructure/tooling (purple)

**Meta Label:**
- `meta` - Meta/tracking issue (pink)

## Customization

### Changing the Application

Edit `prompts/app_spec.txt` to specify a different application to build.

### Adjusting Issue Count

Edit `prompts/initializer_prompt.md` and change "50 issues" to your desired count.

### Modifying Allowed Commands

Edit `security.py` to add or remove commands from `ALLOWED_COMMANDS`.

### Changing Labels

Edit `github_config.py` to customize label names, colors, and descriptions.

## Troubleshooting

**"CLAUDE_CODE_OAUTH_TOKEN not set"**
Run `claude setup-token` to generate a token, then export it.

**"GITHUB_TOKEN not set"**
Get your token from `https://github.com/settings/tokens` with `repo` and `project` scopes.

**"Appears to hang on first run"**
Normal behavior. The initializer is creating workflow labels and 50 GitHub issues with detailed descriptions. Watch for `[Tool: mcp__github__create_issue]` output.

**"Command blocked by security hook"**
The agent tried to run a disallowed command. Add it to `ALLOWED_COMMANDS` in `security.py` if needed.

**"GitHub MCP server connection failed"**
Verify your `GITHUB_TOKEN` is valid and has appropriate permissions. Try running:
```bash
npx -y @modelcontextprotocol/server-github
```

**"Repository not found"**
Ensure the repository exists and your token has access to it.

## Viewing Progress

Open your GitHub repository to see:
- All 50 issues created by the initializer agent
- Real-time label changes (todo → in-progress → done)
- Implementation comments on each issue
- Session summaries on the META issue

You can filter issues by label:
- `is:issue is:open label:status:todo` - Remaining work
- `is:issue is:open label:status:done` - Completed work
- `is:issue is:open label:priority:urgent` - High priority items

## Advantages of GitHub Integration

1. **Tighter Integration**: Issues, commits, and PRs all in one place
2. **Better Visibility**: Anyone with repo access can see progress
3. **Simpler Setup**: No additional tool accounts needed
4. **Free**: No subscription costs for unlimited issues
5. **Better Automation**: GitHub Actions can trigger on issue events
6. **Community Friendly**: Open source projects benefit from public visibility
7. **Rich Ecosystem**: Integrates with VS Code, GitHub CLI, and other tools

## License

MIT License - see [LICENSE](LICENSE) for details.
