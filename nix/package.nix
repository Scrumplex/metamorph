{self, ...}: {
  perSystem = {pkgs, ...}: {
    packages = let
      metamorph = pkgs.python3.pkgs.callPackage ./metamorph.nix {inherit self;};
    in {
      default = metamorph;
      inherit metamorph;
    };
  };
}
