{ lib, config, pkgs, ... }:
{
  # nix expressions to configure the relevant things
  # manual nix-shell -c "make clean && make" (etc) is still needed, sadly

  virtualisation.docker.enable = true;

  services.nginx.virtualHosts."franklincce.beepboop.systems" = {
    forceSSL = true;
    enableACME = true;
    locations."/" = {
      proxyPass = "http://localhost:1337";
    };
  };
}
