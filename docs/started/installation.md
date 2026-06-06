# Installation

## System Requirements

- **Python**: 3.9 or higher (✨ Enhanced support in v0.3.0)
- **Flet**: 0.27.0 or higher (required dependency)
- **Operating Systems**: Windows, macOS, Linux, iOS, Android, Web

!!! info "Dependency Changes"
    Since **version 0.1.3**, Flet must be installed separately. This allows better version control and reduces package size.

## Quick Installation

### Option 1: Complete Installation (Recommended)

Installs Flet-Easy with all features including JWT support and CLI tools:

```bash
# Install with all features
pip install flet-easy[all] --upgrade
```

### Option 2: Basic Installation

Minimal installation for basic functionality:

```bash
# Install Flet first
pip install flet>=0.21.0

# Then install Flet-Easy
pip install flet-easy
```

---

## Ways to install

!!! warning "Available from version 0.2.4"

Flet-Easy provides several ways to install. This allows you to use dependencies that must be used, avoiding unnecessary things when building your application, allowing better control.

### Install Flet-Easy Complete

!!! note
    If you use the [`fs`](../cli/commands.md) cli, it is important to have [`git`](https://git-scm.com/downloads) installed.

Installs all the dependencies to use, you can use all the functionalities provided by Flet-Easy

```bash
pip install flet-easy[all]
```

---

### Install clean Flet-Easy

!!! tip
    [Recommended for `Flet` Packaging Application](https://flet.dev/docs/publish).

Requires installation of [Flet >= 0.21](https://github.com/flet-dev/flet).

```bash
pip install flet>=0.21
```

#### If you do not use: [`[CLI-to-create-app]`](../cli/create-app.md)

```bash
pip install flet-easy
```

---

#### Install Flet-Easy if you need to use [`[Basic-JWT]`](../advanced/basic-jwt.md)

```bash
pip install flet-easy[JWT]
```
