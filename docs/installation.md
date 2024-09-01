# Installation
FletEasy provides several ways to install. This allows you to use dependencies that must be used, avoiding unnecessary things when building your application, allowing better control.

## Ways to install

### Install FletEasy Complete
!!! note
    If you use the [`fs`](/flet-easy/0.2.4/cli-to-create-app/) cli, it is important to have [`git`](https://git-scm.com/downloads) installed.

Installs all the dependencies to use, you can use all the functionalities provided by FletEasy

```bash
pip install flet-easy[all]
```

---

### Install clean FletEasy
!!! tip
    [Recommended for `Flet` Packaging Application](https://flet.dev/docs/publish).

Requires installation of [Flet >= 0.21](https://github.com/flet-dev/flet).

```bash
pip install flet
```

#### If you do not use: [CLI-to-create-app](/flet-easy/0.2.4/cli-to-create-app)

```bash
pip install flet-easy
```

---

#### Install FletEasy if you need to use [Basic-JWT](/flet-easy/0.2.4/basic-jwt)

```bash
pip install flet-easy[JWT]
```