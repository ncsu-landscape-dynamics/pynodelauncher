# pynodelauncher

The *pynodelauncher* tool launches pleasantly parallel tasks on multiple nodes
on a HPC cluster.

It is using MPI through the *mpi4py* package which in turn is using system MPI library.
A task can be any command, typically a call of a script with a series of parameters.

## Installation

Use *pip* to install *pynodelauncher*:

```sh
python -m pip install git+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
```

This will also install the *mpi4py* package (again using pip) if it is not already
installed (using pip or in any other way).

## Authors

* Vaclav Petras, [NC State University, Center for Geospatial Analytics](https://geospatial.ncsu.edu/)
* Lisa L. Lowe, NC State University, Office of Information Technology, Advanced Computing

## Copyright, License, and Disclaimer

Copyright (C) 2021 The Authors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
