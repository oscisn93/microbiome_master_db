{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    pkgs.python310
    pkgs.poetry
    pkgs.sqlite
  ];
  shellHook = ''
    poetry shell
  '';
}

