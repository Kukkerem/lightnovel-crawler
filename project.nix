{ config, modulesPath, nix2container, pkgs, ... }:

{
  # modules that our project will use
  require = [
    "${modulesPath}/tools/mod-lean-python.nix"
    "${modulesPath}/languages/python-poetry.nix"
    "${modulesPath}/builders/docker-nix2container.nix"
  ];

  # name of our application
  name = "lightnovel-crawler";

  # files to exclude (there often are files that you need to have in git, but
  # you don't want nix to rebuild your app if they change)
  # simpliarly to .gitignore you can also exclude everything and implicitly
  # list files you want included
  src_exclude = [
    ''
      *
      !/lncrawl
      !/sources
      !/pyproject.toml
      !/poetry.lock
    ''
  ];

  lean_python = {
    enable = true;
    package = pkgs.python311;
    configd = true;
    expat = true;
    libffi = true;
    openssl = true;
    zlib = true;
  };

  python = {
    enable = true;
    # package = pkgs.python311; # use python3.11
    package = config.out_lean_python;
    inject_app_env = true; # add project dependencies to dev shell (simplar to to being in an activated virtualenv)
    prefer_wheels = false; # whether to compile packages ourselves or use wheels
  };

  docker = {
    enable = true;
    copy_to_root = pkgs.buildEnv {
      name = "root";
      paths = [
        config.out_python
        pkgs.busybox # only for debugging
      ];
      pathsToLink = [ "/bin" ];
    };
    entrypoint = [ "${pkgs.tini}/bin/tini" ];

    # getting permission error on some k8s clusters
    user = "65535:65535";

    # call /bin/hello when running the container
    command = [ "${config.out_python}/bin/lncrawl" ];

    # organize the container into 3 layers:
    # - base layer with pythoni, busybox & tini
    # - layer with application dependencies
    # - our application
    layers = with nix2container; let
      layer-1 = buildLayer {
        deps = with pkgs; [
          busybox
          config.out_lean_python
          tini
        ];
      };
      layer-2 = buildLayer {
        deps = config.out_python.propagatedBuildInputs;
        layers = [
          layer-1
        ];
      };
    in
    [
      layer-1
      layer-2
    ];
  };

  # packages that should be available in dev shell
  dev_commands = with pkgs; [
    dive
  ];
}
