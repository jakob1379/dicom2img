{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            uv
          ];

          LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
          ]}:$LD_LIBRARY_PATH";

          shellHook = ''
          '' ;
        };
      }
  );

}
