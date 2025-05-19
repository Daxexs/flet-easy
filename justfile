set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"]
set export := true
set positional-arguments := true
set unstable
set script-interpreter := ['uv', 'run', '--script']

user := file_stem(home_directory())
curr_time := datetime("%Y%m%dT%H%M%S")

# Open the devenv shell
shell:
    {{ if env("DEVENV_RUNTIME", "") == "" { "sudo -E devenv shell --impure --verbose" } else { "echo 'Already in devenv shell!'" } }}

# Own the current directory as the logged in user
own:
    sudo chown -R {{ user }} .

# Run the flet app using the Python runtime
run:
    uv run fs

# Run the tests using the Python runtime
test:
    uv run pytest

# Initialize the python project environment   
ready-py:
    uv lock
    uv sync --locked --all-extras --all-groups
    unset VIRTUAL_ENV

# Set the git repo remote url (should be set to original repo)   
set-remote:
    git remote set-url origin git@github.com:topher097/flet-easy.git
    
# Run windows VM
windows:
    quickget windows 11 English
    quickemu --ignore-msrs-always
    quickemu --vm windows-11-English.conf

# Stage all files for git
gadd:
    git add .

# Garbage collect
gc:
    sudo devenv gc
    sudo nix-collect-garbage -d

# Run pre-commit hooks
pre-commit args="": gadd
    pre-commit run {{ args }}

# Run ruff checks on all of the git staged files
check: gadd
    uv run ruff check --fix $(git --no-pager diff --cached --name-only --diff-filter=d '*.py')

# Run ruff formatting on all of the git staged files
format dry="": gadd
    uv run ruff format {{ if dry == "foreal" { "" } else { "--check" } }} $(git --no-pager diff --cached --name-only --diff-filter=d '*.py')

# Preview the changes to the docs
docs:
    uv run mkdocs serve