# compas\_rcf

[![Travis (.com)](https://img.shields.io/travis/com/tetov/compas_rcf?style=for-the-badge)](https://travis-ci.com/tetov/compas_rcf)
[![GitHub](https://img.shields.io/github/license/tetov/compas_rcf?style=for-the-badge)](https://github.com/tetov/compas_rcf/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/compas_rcf?style=for-the-badge)](https://pypi.org/project/compas-rcf/)

python module for MAS DFAB project Rapid Clay Formations

* [Getting started](https://compas_rcf.tetov.se/getting_started.html) - for installation and update instructions
* [Example files](https://compas_rcf.tetov.se/examples.html) - for demonstration purposes
* [Contributing](https://compas_rcf.tetov.se/contributing.html) - how to start working on the code
* [Known issues](https://compas_rcf.tetov.se/known_issues.html) - for things that we know don't work
* [Issues](https://github.com/tetov/compas_rcf/issues) - for unknown issues, as well as suggestions and questions
* [Documentation](https://compas_rcf.tetov.se/)

## COMPAS

`compas_rcf` is part is built on top of [`compas`](https://compas-dev.github.io/),
 [`compas_fab`](https://gramaziokohler.github.io/compas_fab/) and
 [`compas_rrc`](https://bitbucket.org/ethrfl/compas_rrc/).

## Note on compatibility

Installation of the package requires Python \>\= 3.6.

Big parts are compatible with IronPython 2.7 (to be run inside Rhino plugin
Grasshopper).

The modules that require Python \>\= 3.6 should raise an exception on import.
