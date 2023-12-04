{
  description = "Nortech Python";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, poetry2nix }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgsForAllSystems = forAllSystems (system: import nixpkgs { 
        inherit system;
        config = { allowUnfree = true; }; 
      });

      makeDevShell = system: let
        inherit pkgsForAllSystems;
        pkgs = pkgsForAllSystems.${system};
        pythonPkg = pkgs.python39;
        pythonEnv = pythonPkg.buildEnv.override {
          extraLibs = [ pythonPkg.pkgs.pip pythonPkg.pkgs.virtualenv ];
        };

        isDarwin = pkgs.stdenv.hostPlatform.isDarwin;
        darwinPackages = if isDarwin then [ ] else [ ];
      in
      pkgs.mkShell {
        buildInputs = [
          pythonEnv
        ] ++ darwinPackages;

        shellHook = ''
          # Create a virtual environment
          virtualenv .venv

          # Activate the virtual environment
          source .venv/bin/activate

          # Install poetry inside the virtual environment
          pip install poetry==1.4.2 
        '';
      };
    in
    {
      devShells = forAllSystems (system: {
          default = makeDevShell system;
      });
    };
}