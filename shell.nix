{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.python311Packages; [ django pymupdf ] ++ [pkgs.docker-compose pkgs.gnumake] ;
  }
