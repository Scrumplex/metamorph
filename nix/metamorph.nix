{
  lib,
  buildPythonPackage,
  poetry-core,
  self,
}:
buildPythonPackage {
  name = "metamorph";
  format = "pyproject";

  src = lib.cleanSource self;

  nativeBuildInputs = [
    poetry-core
  ];

  pythonImportsCheck = ["metamorph"];

  meta = with lib; {
    description = "Prism Launcher Metadata Framework";
    homepage = "https://github.com/PrismLauncher/meta-ng";
    license = licenses.agpl3Only;
    maintainers = with maintainers; [Scrumplex];
  };
}
