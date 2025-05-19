# https://github.com/maximoffua/flutter.nix
{ pkgs, inputs, config, ... }:
let
  system = pkgs.stdenv.system;
  git-hooks = inputs.git-hooks.packages.${system}.git-hooks;
in {
  #cachix.enable = false;
  languages = {
    python = {
      enable = true;
      version = "3.12.7";
      uv = {
        enable = true;
        sync = { enable = true; };
      };
    };
    dart = {
      enable = true;
      package = pkgs.dart;
    };
  };

  # Enable android studio
  android = {
    enable = true;
    android-studio = {
      enable = true;
      package = pkgs.android-studio;
    };
    flutter = {
      enable = true;
      package = pkgs.flutter;
    };
    emulator = { enable = true; };
  };

  # Define packages to be included in the development environment
  packages = with pkgs; [
    bashInteractive
    pre-commit
    just
    uv
    flutter
    ungoogled-chromium
  ];

  # Git pre-commit hooks, defined here. LINK: https://github.com/cachix/git-hooks.nix/tree/master
  git-hooks = {
    excludes = [ ".xml" ".dll" ".exe" ".pdb" ".flake.nix" ];
    enabledPackages = [ pkgs.python312Packages.ruff ];
    hooks = {
      # Lint and format YAML files
      yamllint = {
        enable = false;
        #excludes = [ "*/.circleci/config.yml" ];
        settings = { preset = "relaxed"; };
      };
      yamlfmt.enable = false;

      # Lint and format shell scripts
      shellcheck = {
        enable = true;
        excludes = [ ".envrc" ];
      };
      shfmt.enable = true;

      # Lint and format python using ruff
      ruff.enable = true; # ruff check
      ruff-format.enable = true;

      # Lint and format for nix files
      nixfmt-classic.enable = true;
      #   statix.enable = true;
      #   statix.settings.ignore = [ ".devenv*" ];

      # No-commit-to-branch
      no-commit-to-branch.enable = true;

      # Spell-checking hook
      typos = {
        enable = true;
        settings = { ignored-words = [ "datas" ]; };

      };

      # Prevent secrets from being committed
      ripsecrets.enable = true;
    };
  };

  env = {
    UV_LINK_MODE = "copy";
    UV_PYTHON_PREFERENCE = "only-system";
    UV_PYTHON = "3.12";
    UV_PYTHON_DOWNLOADS = "never";

    CHROME_EXECUTABLE = "${pkgs.ungoogled-chromium}/bin/chromium";
  };

  # Commands which run when the shell is started
  enterShell = ''
    export UV_PROJECT_ENVIRONMENT=$(pwd)/.venv


    # Flutter configuration
    flutter config --enable-web
    #flutter config --android-studio-dir $ANDROID_STUDIO_DIR

    # Set the SSH agent if not already set
    if [ -z "$SSH_AUTH_SOCK" ] ; then
      eval `ssh-agent -s`
      ssh-add $PRIVATE_SSH_PATH
    fi

    uv tool update-shell

    # Python environment setup
    just ready-py

    # Own the local directory
    just own

    # Run the fish shell instead of bash
    fish --init-command="source ./.venv/bin/activate.fish"

    # When the command 'exit' is run to exit the fish shell, then the bash shell is run, so exit that
    exit
  '';
}
