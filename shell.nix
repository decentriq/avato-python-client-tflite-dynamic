with import <nixpkgs> {};

pkgs.mkShell {

  buildInputs = with pkgs; [
      python37
      python37Packages.pip
      python37Packages.virtualenv
      python37Packages.setuptools

  ];
}
