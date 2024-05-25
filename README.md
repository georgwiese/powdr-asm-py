# Setup

<!-- Install the `powdr` command-line tool:

```sh
git clone git@github.com:powdr-labs/powdr.git
cd powdr
cargo install --path cli --features halo2
powdr --help
``` -->

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

# Misc

Update powdr-py:
```sh
pixi remove --pypi powdr-py
pixi add --pypi "powdr-py @ git+https://github.com/georgwiese/powdr-py.git"
```

rustup target add riscv32imac-unknown-none-elf
