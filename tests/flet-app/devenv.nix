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
    fish
    flutter
    ungoogled-chromium

    # Packages needed for flet to run
    util-linux
    gtk3
    pango
    cairo
    glib
    at-spi2-atk
    gdk-pixbuf
    harfbuzz
    libepoxy
    fontconfig
  ];

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

    # Add the included packages outputs to the LD_LIBRARY_PATH for easier linking
    export DEVENV_LIB=$DEVENV_DOTFILE/profile/lib
    export LD_LIBRARY_PATH=$DEVENV_LIB:$LD_LIBRARY_PATH

    # Run the fish shell instead of bash
    fish --init-command="source ./.venv/bin/activate.fish"

    # When the command 'exit' is run to exit the fish shell, then the bash shell is run, so exit that
    exit
  '';
}
