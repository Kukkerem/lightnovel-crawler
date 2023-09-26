{
  description = "An example application";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    nixpkgs-unstable.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    nix-cde.url = "github:takeda/nix-cde";
    nix-cde.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, flake-utils, nix-cde, nixpkgs, ... }: flake-utils.lib.eachDefaultSystem (build_system:
    let
      cde = is_shell: nix-cde.lib.mkCDE ./project.nix { inherit build_system is_shell self; };
      cde-docker = nix-cde.lib.mkCDE ./project.nix {
        inherit build_system self;
        host_system = "x86_64-linux";
        # cross_system = nixpkgs.lib.systems.examples.musl64;
      };
      cde-docker-aarch64 = nix-cde.lib.mkCDE ./project.nix {
        inherit build_system self;
        # host_system = "x86_64-linux";
        cross_system = nixpkgs.lib.systems.examples.aarch64-unknown-linux-gnu;
      };
    in
    {
      packages.default = (cde false).outputs.out_python;
      packages.docker = cde-docker.outputs.out_docker;
      packages.docker_aarch64 = cde-docker-aarch64.outputs.out_docker;
      devShells.default = (cde true).outputs.out_shell;
    });
}
