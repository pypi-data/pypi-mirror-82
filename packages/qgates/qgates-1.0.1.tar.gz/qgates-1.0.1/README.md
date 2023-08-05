# QGates

[![Build Status](https://travis-ci.org/a-poor/QGates.svg?branch=master)](https://travis-ci.org/a-poor/QGates)
[![PyPI](https://img.shields.io/pypi/v/qgates)](https://pypi.org/project/qgates/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qgates)](https://pypi.org/project/qgates/)
[![GitHub last commit](https://img.shields.io/github/last-commit/a-poor/qgates)](https://github.com/a-poor/QGates)
[![PyPI - License](https://img.shields.io/pypi/l/qgates)](https://github.com/a-poor/QGates)


created by Austin Poor

A small file with some helper functions and quantum gates represented as numpy matrices.


## Requirements

* [Python 3](https://www.python.org/downloads/)
* [Numpy](https://numpy.org/)

## Installation

```bash
pip install qgates
```

## Usage

### Helper Functions

`qgates.tens(v,w)`

...

`qgates.matmul(v,w)`

...

`qgates.state(num)`

...

`qgates.conjugate(num)`

...

### State Vectors

[__Basic Qubits__](https://en.wikipedia.org/wiki/Qubit)

`qgates.QB0`: Quantum state 0

`qgates.QB1`: Quantum state 1

`qgates.QB00`: Quantum state 00

`qgates.QB01`: Quantum state 01

`qgates.QB10`: Quantum state 10

`qgates.QB11`: Quantum state 11

[__Bell States__](https://en.wikipedia.org/wiki/Bell_state)

`qgates.BELL00`: Bell state 00

`qgates.BELL01`: Bell state 01

`qgates.BELL10`: Bell state 10

`qgates.BELL11`: Bell state 11


### Gate Matrices

`qgates.IDEN`: 2x2 Identity matrix 

```
[[ 1, 0 ],
 [ 0, 1 ]]
```

`qgates.NOT`: 2x2 NOT matrix 

```
[[ 0, 1 ],
 [ 1, 0 ]]
```

`qgates.OR`: 2x4 OR matrix 

```
[[ 1, 0, 0, 0 ],
 [ 0, 1, 1, 1 ]]
```

`qgates.AND`: 2x4 AND matrix 

```
[[ 1, 1, 1, 0 ],
 [ 0, 0, 0, 1 ]]
```

`qgates.XOR`: 2x4 XOR matrix 

```
[[ 1, 0, 0, 1 ],
 [ 0, 1, 1, 0 ]]
```

`qgates.NOR`: 2x4 NOR matrix 

```
[[ 0, 1, 1, 1 ],
 [ 1, 0, 0, 0 ]]
```

`qgates.NAND`: 2x4 NAND matrix 

```
[[ 0, 0, 0, 1 ],
 [ 1, 1, 1, 0 ]]
```

`qgates.COPY`: A 4x2 gate matrix for copying a state vector

```
[[ 1, 0 ],
 [ 0, 0 ],
 [ 0, 0 ],
 [ 0, 1 ]]
```

`qgates.SWAP`: A 4x4 gate matrix for swapping a the middle two positions of a length-4 state vector

```
[[ 1, 0, 0, 0 ],
 [ 0, 0, 1, 0 ],
 [ 0, 1, 0, 0 ],
 [ 0, 0, 0, 1 ]]
```

`qgates.CNOT`: 4x4 Conditional-NOT gate. (Read more [here](https://en.wikipedia.org/wiki/Controlled_NOT_gate))

```
[[ 1, 0, 0, 0 ],
 [ 0, 1, 0, 0 ],
 [ 0, 0, 0, 1 ],
 [ 0, 0, 1, 0 ]]
```

`qgates.TOFFOLI`: 8x8 Toffoli gate. (Read more [here](https://en.wikipedia.org/wiki/Toffoli_gate))

```
[[1, 0, 0, 0, 0, 0, 0, 0],
 [0, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0],
 [0, 0, 0, 1, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 0, 0, 0],
 [0, 0, 0, 0, 0, 1, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 0, 1, 0]]
```

`qgates.HAD`: 2x2 Hadamard gate. (Read more [here](https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_(H)_gate))

```
[[ 1/√2,  1/√2 ],
 [ 1/√2, -1/√2 ]]
```


