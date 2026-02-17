# Claude Code Agent Setup Guide

## Complete Instructions from "How to Automate Your Life & Work w/ Claude Code"

## Table of Contents

1. [Understanding Claude Code as a Digital Employee](#understanding-claude-code)
2. [Workspace Architecture](#workspace-architecture)
3. [Four Critical Mistakes to Avoid](#mistakes-to-avoid)
4. [Context Stacking Framework](#context-stacking)
5. [Installation and Setup](#installation-setup)
6. [Workspace Configuration](#workspace-configuration)
7. [Creating Commands and Workflows](#commands-workflows)
8. [Practical Implementation Example](#practical-example)

---

## Understanding Claude Code as a Digital Employee {#understanding-claude-code}

Claude Code acts as a **digital employee** that requires:

- **Tools/Access**: Scripts, APIs, external integrations
- **Context**: Understanding of who you are, what you do, current strategies
- **Knowledge**: Business information, processes, workflows
- **Workspace**: A structured folder system to operate within

### Key Principle

> "When set up correctly and used correctly, it can automate up to 90% of the stuff that you do."

---

## Workspace Architecture {#workspace-architecture}

A **workspace** is one folder on your computer containing:

### Core Folder Structure

```
claude-workspace/
├── commands/          # Reusable prompts for work functions
├── skills/           # Installable plugins from others
├── context/          # Essential context about you and your work
├── outputs/          # Generated reports and files
├── plans/            # Implementation plans
├── reference/        # Templates, competitor lists, etc.
├── scripts/          # Code snippets for external data
└── claude.md         # Workspace description document
```

### Folder Purposes

**Commands Folder**

- Reusable prompts to automate work functions
- Uses natural language to guide Claude through workflows
- Examples: `/marketing-report`, `/competitor-analysis`

**Skills Folder**

- Installable plugins for enhanced capabilities
- Can be downloaded from skills marketplaces
- More advanced than basic commands

**Context Folder**

- Essential information about who you are
- What you do and how you do it
- Current strategies and data
- Read every session to bring Claude up to speed

**Scripts Folder**

- Code snippets created by Claude Code
- Pull external data (APIs, web scraping)
- Process data and return to Claude
- You don't write the code - Claude creates it

**Claude.md File**

- Describes entire workspace to Claude every session
- Combined with context folder for full understanding
- Acts as "employee onboarding" document

---

## Four Critical Mistakes to Avoid {#mistakes-to-avoid}

### Mistake #1: Using Claude Code Like a Chatbot

**Problem**: Long conversations fill up context (200,000 token limit)

- Messages can take up 26%+ of available context
- Leads to "context bloat" - diluted instructions
- Inconsistent, low-quality outputs

**Solution**: Create reusable structured commands instead of chatting

### Mistake #2: Not Contextualizing at Start of Each Session

**Problem**: Poor quality output without proper context

- Missing tone of voice, business context
- Requires constant back-and-forth corrections
- 70% completed work vs 95% completed work

**Solution**: Always run `/prime` command at session start

### Mistake #3: Not Using Planning and Implementation Loops

**Problem**: Manual setup leads to misaligned workflows

- Doesn't consider full workspace integration
- Results in janky, disconnected processes

**Solution**: Use `/create-plan` and `/implement` commands

### Mistake #4: Not Utilizing Scripts

**Problem**: Can't access real-time data or take meaningful digital actions

- Hands tied without external integrations
- Limited to static information only

**Solution**: Let Claude create scripts through planning commands

---

## Context Stacking Framework {#context-stacking}

### The Context Stack (Bottom to Top)

1. **Claude.md File** - Workspace purpose and orientation
2. **Business Information** - What the business does
3. **Personal Information** - Who you are, your role
4. **Strategy** - Current quarterly/project strategies
5. **Current Data** - Real-time metrics and analytics
6. **Workflow Layer** - Commands and tools built on top

### Context Management Rules

- 200,000 token limit for all context
- Start fresh sessions frequently to minimize context bloat
- Always prime with `/prime` command
- Keep context documents updated and relevant

---

## Installation and Setup {#installation-setup}

### Step 1: Install VS Code

1. Search "VS Code" in browser
2. Download for your operating system
3. Follow setup instructions

### Step 2: Install Claude Code Extension

1. Open VS Code
2. Go to Terminal → New Terminal
3. Run installation command (copy from Claude Code website)
4. Follow setup wizard

### Step 3: Account Setup Options

**Option A: Use Existing Claude Pro/Max Account**

- Select Claude account option during setup

**Option B: Create Developer Account**

1. Go to `console.anthropic.com`
2. Sign up for developer/business account
3. Set up billing and add $5 balance
4. Go to Settings → API Keys
5. Create new API key
6. Copy API key for VS Code setup

### Step 4: Set Up Quick Start Aliases

Copy this configuration into Claude Code:

```bash
# Claude Safety (with permissions)
alias cs='claude --prime'

# Claude Risky (skip permissions + auto-prime)
alias cr='claude --skip-permissions --prime'
```

This allows you to:

- Type `cs` for safe mode with permissions
- Type `cr` for fast mode (recommended) with auto-priming

---

## Workspace Configuration {#workspace-configuration}

### Download and Setup Workspace Template

1. Download Claude Workspace Template (provided in video description)
2. Unzip folder
3. Open VS Code → File → Open Folder
4. Select the unzipped workspace folder

### Configure Context Files

**Business Context** (`context/business.md`)

- Company/business information
- Mission, values, objectives
- Products/services offered
- Target audience

**Personal Information** (`context/personal.md`)

- Your role and responsibilities
- How you relate to the business
- Your working style and preferences
- Key contacts and relationships

**Strategy** (`context/strategy.md`)

- Current quarterly/yearly strategies
- Active projects and priorities
- Goals and KPIs
- Recent strategic decisions

**Current Data** (`context/data.md`)

- Latest analytics and metrics
- Performance data
- Market insights
- Can be manually updated or automated via scripts

### Update Claude.md File

- Describes workspace purpose
- Lists available commands
- Explains folder structure
- Gets automatically updated by planning commands

---

## Creating Commands and Workflows {#commands-workflows}

### Basic Command Structure

Commands are markdown files with natural language instructions:

```markdown
# Command Name: /analyze-competitor

## Purpose

Create a comprehensive competitor analysis report

## Prerequisites

- Apify API key configured
- PowerPoint skill installed

## Workflow

1. **Deep Research**: Use background research agent to find competitor info
2. **Data Collection**: Scrape YouTube/social data using Apify
3. **Report Generation**: Create markdown analysis report
4. **Presentation**: Convert to PowerPoint using PPTX skill

## Instructions

Take the input competitor name and:

- Research their background, positioning, content strategy
- Pull real-time metrics from their channels
- Analyze their top-performing content
- Generate SWOT analysis
- Create visual presentation
```

### Planning and Implementation Workflow

**Step 1: Create Plan**

```bash
/create-plan I want to create a competitor analysis command that researches podcasts and creates reports
```

**Step 2: Review Plan**

- Claude analyzes workspace
- Creates detailed implementation plan
- Shows exactly what files will be modified
- Explains integration with existing systems

**Step 3: Implement Plan**

```bash
/implement [paste plan content]
```

**Step 4: Test and Iterate**

- Run the new command
- Refine based on results
- Update using same planning process

---

## Practical Implementation Example {#practical-example}

### Real Example: Podcast Competitor Analysis

**Goal**: Automate competitor research for podcast guests and market analysis

**Implementation Steps**:

1. **Context Setup**
   - Added personal info about podcast
   - Updated strategy document with podcast goals
   - Modified claude.md for podcasting workspace

2. **Command Creation**

   ```bash
   /create-plan Create /analyze-competitor command that:
   - Takes podcast/person name as input
   - Uses deep research agent for web research
   - Integrates Apify MCP for YouTube data scraping
   - Generates comprehensive markdown report
   - Creates PowerPoint presentation using PPTX skill
   ```

3. **Required Integrations**
   - **Apify**: Web scraping platform for real-time data
   - **MCP Integration**: Connects Claude to external APIs
   - **PowerPoint Skill**: Converts reports to presentations
   - **Background Research Agent**: Enhanced web research

4. **Command Usage**

   ```bash
   /analyze-competitor Lenny's Podcast
   ```

5. **Output Generated**
   - Comprehensive markdown research report
   - PowerPoint presentation with:
     - Channel overview and metrics
     - Content strategy analysis
     - Top performing content
     - SWOT analysis
     - Strategic recommendations

### Results Achieved

- Automated 2+ hours of manual research
- Generated professional presentation
- Integrated real-time data from YouTube
- Created reusable workflow for future analysis

---

## Advanced Tips and Best Practices

### Session Management

- Start new Claude sessions frequently with `cr` command
- Always begin with `/prime` to load context
- Use Command + K to clear terminal
- Command + \ to open new terminal

### File Management

- Command + Click to open files in new tabs
- Command + W to close tabs
- Command + S to save files
- Right-click markdown files → "Open Preview" for formatted view

### API Keys and Security

- Store API keys in `.env` file in workspace root
- Never commit API keys to version control
- Use environment variables for sensitive data

### Skills and Extensions

- Browse skills marketplace at `skillsmpp.com`
- Download as ZIP and place in skills folder
- Let Claude integrate new skills through planning process
- Test skills individually before building into workflows

### Workspace Organization

- Create separate workspaces for different business functions
- Keep context documents updated and relevant
- Regular cleanup of outputs and plans folders
- Back up workspace configurations

---

## Conclusion

This Claude Code setup can automate up to 90% of repetitive work tasks when configured properly. The key is:

1. **Proper workspace structure** with organized folders and context
2. **Consistent priming** at the start of each session
3. **Reusable commands** instead of ad-hoc chatting
4. **Planning workflow** for complex implementations
5. **External integrations** via scripts and skills

Start with basic commands and gradually build complexity. The investment in proper setup pays massive dividends in productivity gains.

---

_This guide is based on the comprehensive tutorial "How to Automate Your Life & Work w/ Claude Code: Ultimate Beginner's Guide" - a complete system for AI-powered productivity automation._
