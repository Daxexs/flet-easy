# Installation

!!! info
    In **version 0.1.3 from now on** it requires installing [`flet`](http://github.com/flet-dev/flet) separately, in previous versions it is installed by default.

    ```bash
    pip install flet
    ```
To install flet-easy just copy this into your terminal after having already installed `python >= 3.8`

```bash
pip install flet-easy
```

---

## Ways to install

!!! warning "Available from version 0.2.4""

Flet-Easy provides several ways to install. This allows you to use dependencies that must be used, avoiding unnecessary things when building your application, allowing better control.

### Install Flet-Easy Complete

!!! note
    If you use the [`fs`](/flet-easy/0.2.0/cli-to-create-app/) cli, it is important to have [`git`](https://git-scm.com/downloads) installed.

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

#### If you do not use: [`[CLI-to-create-app]`](/flet-easy/0.2.0/cli-to-create-app)

```bash
pip install flet-easy
```

---

#### Install Flet-Easy if you need to use [`[Basic-JWT]`](/flet-easy/0.2.0/basic-jwt)

```bash
pip install flet-easy[JWT]
```
