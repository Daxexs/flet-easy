## Publishing Flet app to multiple platforms

### Installation requirements

> [!NOTE]
    For local testing or web use

* flet
* flet-easy
* peewee

### Packaging app for Android
Route where it should be located in the project: `./flet`

> [!IMPORTANT]
    If there is an error, rename the folder, for example from `flet to app`.

```bash
cd flet
```

#### APK
```bash
flet build apk -vv
```

#### WINDOWS
```bash
flet build windows -vv
```

#### WEB
```bash
flet run main.py -w -d -r
```