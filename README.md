# Pywdr - zk-VMs in Python

This project is a submission to [ETH Berlin](https://ethberlin.org/), building on [powdr](https://powdr.org) and [`powdr-py`](https://github.com/georgwiese/powdr-py).

With this library, you can specify zk-VMs succinctly in Python. For example, see:
- [`src/hello_world.py`](./src/hello_world.py): An example VM with several registers, control flow instructions, and memory.
- [`src/hello_world.asm`](./src/hello_world.asm): An assembly program written for the "Hello world" processor defined above.
- [`src/demo.py`](./src/demo.py): The main python program to compile the zk-VM and generate a proof for the correct execution of the assembly program.

## Setup

```sh
# Install pixi
curl -fsSL https://pixi.sh/install.sh | bash
# or use alternative installation methods:
https://pixi.sh/latest/

# Install the project requirements
pixi install
pixi run install-powdr

# Enter the pixi environment
pixi shell
```
