# Publishing Flet app to multiple platforms

## Installation requirements

> [!IMPORTANT]
    For local testing or web use

* flet
* flet-easy[jwt]
* tortoise-orm

---

## Packaging app

Route where it should be located in the project: `./flet-app`

```bash
cd flet-app
```

### APK

```bash
flet build apk -vv
```

### WINDOWS
>
> [!NOTE]
    **If you have any problem - build Windows**
    Remove `print()` from Python if used in 'add_middleware' functions.

```bash
flet build windows -vv
```

### WEB
>
> [!NOTE]
    **If you have any problem - build web**
    Use `ft.app(target=app.get())` when compiling web statica.

```bash
flet build web -vv
```
