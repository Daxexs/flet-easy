# Contributing to FletEasy

First off, thanks for taking the time to contribute! Contributions include but are not restricted to:

* Reporting bugs
* Contributing to code
* Writing tests
* Writing documentation

The following is a set of guidelines for contributing.

### 1. Install pdm
For more information [here](https://github.com/pdm-project/pdm).

```bash
pip install pdm
```

### 2. Clone repository

```
git clone https://github.com/Daxexs/flet-easy.git
```

### 3. Maintain dependencies to initialize the project
Install all dependencies and create a runtime environment for python automatically.

```bash
pdm update
```

### 4. Code formatting and check
If you make some changes in the src/ and you want to preview the result of the code if it is optimal, just do it:

```bash
pdm run format
```
```bash
pdm run check
```

### 5. Preview the documentation
If you make some changes to the docs/ and you want to preview the build result, simply do:
```bash
pdm run doc
```

### 6. Create a Pull Request
Once you have reviewed step 4 you can make the pull request with a detailed description of the new integrations or changes made to the code, with images or videos demonstrating what the code does if possible.