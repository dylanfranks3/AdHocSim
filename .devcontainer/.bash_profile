# profile for pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export LD_LIBRARY_PATH="/usr/lib/aarch64-linux-gnu/"
eval "$(pyenv init -)"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

NS3_BINDINGS_INSTALL_DIR="/dcs/21/u2109078/.local/lib/python3.6/site-packages"