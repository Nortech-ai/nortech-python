{
  description = "Nortech Python";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
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

        isDarwin = pkgs.stdenv.hostPlatform.isDarwin;
        darwinPackages = if isDarwin then [ ] else [ ];
      in
      pkgs.mkShell {
        buildInputs = [
          pkgs.uv
          pkgs.watchexec
          pkgs.git
        ] ++ darwinPackages;

        shellHook = '''';
      };
    in
    {
      devShells = forAllSystems (system: {
        default = makeDevShell system;
      });
    };
}
