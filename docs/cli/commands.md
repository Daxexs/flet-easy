# CLI Commands

Flet-Easy provides a powerful command-line interface (CLI) to streamline development workflows. The CLI helps you create project structures, manage dependencies, and automate common tasks.

## Overview

The Flet-Easy CLI (`fs`) offers:

- **Project Scaffolding**: Create new projects with MVC structure
- **Template Management**: Use pre-built project templates
- **Development Tools**: Utilities for building and testing
- **Code Generation**: Generate boilerplate code automatically

## Installation

The CLI is automatically installed with Flet-Easy when using the full installation:

```bash
pip install flet-easy[all] --upgrade
```

Or install just the CLI dependencies:

```bash
pip install flet-easy cookiecutter rich-argparse
```

## Basic Usage

### Check Version

```bash
fs --version
# or
fs -v
```

### Get Help

```bash
fs --help
```

## Commands

### `fs init` - Create New Project

Create a new Flet-Easy project with a complete MVC structure.

**Syntax:**

```bash
fs init
# or
fs i
```

**Interactive Setup:**
When you run `fs init`, you'll be prompted for:

1. **Project Name**: The name of your project directory
2. **App Name**: The main application name
3. **Author**: Your name or organization
4. **Description**: Brief project description
5. **License**: Choose from common licenses (MIT, Apache, etc.)
6. **Python Version**: Minimum Python version requirement

**Example Session:**

```bash
$ fs init
[1/6] Project name (my-flet-app): todo-app
[2/6] App name (TodoApp): Task Manager
[3/6] Author (Your Name): John Doe
[4/6] Description: A simple task management application
[5/6] License [MIT]: MIT
[6/6] Python version (3.8): 3.9

✅ Project created successfully!
📁 Project location: ./todo-app/
```
