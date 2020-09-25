# default ~/.bashrc script

# NOTE: See ~freeware/bash_profile.d/README before making
# changes to this file.

source ~freeware/bash_profile.d/bashrc.general

##########################
# CUSTOMIZATIONS GO HERE #
##########################
export PATH=$HOME/local/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/local/lib

#alias tmux="TERM=screen-256color tmux"
export TERM=screen-256color 

alias cdq='watch -d -n 1.0 condor_q'
alias smi='watch -d -n 1.0 nvidia-smi'
alias cds='condor_submit'
alias mystat="condor_status -constraint 'RemoteUser == \"zwang@esat.kuleuven.be\" || RemoteUser == \"nice-user.zwang@esat.kuleuven.be\"'"
alias pycharm='bash /users/visics/zwang/Tools/pycharm-community-2020.1.2/bin/pycharm.sh'
alias tnew='tmux new -s'

# Blender path
#export BLENDER=/users/visics/zwang/ExternelLib/Blender/blender-2.90.1-linux64/2.90
#alias blender='/users/visics/zwang/ExternelLib/Blender/blender-2.90.1-linux64/blender'
export BLENDER=/users/visics/zwang/ExternelLib/Blender/blender-2.79b-linux64/2.79
alias blender='/users/visics/zwang/ExternelLib/Blender/blender-2.79b-linux64/blender'

####################

export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}$
export PATH=/users/visics/zwang/miniconda3:$PATH
export PATH=/users/visics/zwang/miniconda3/bin:$PATH
export PATH=/users/visics/zwang/.local/bin:$PATH
export PATH=/users/visics/zwang/pydevd-pycharm.egg:$PATH
export PATH=/users/visics/zwang/Tools/gitkraken:$PATH
# jiayuan mao custum lib
export PATH=/users/visics/zwang/ExternelLib/Jacinle/bin:$PATH
# add customized lib
export PYTHONPATH=$PYTHONPATH:/users/visics/zwang/Documents/workplace/ZHToolkit
export PYTHONPATH=$PYTHONPATH:/users/visics/zwang/ExternelLib/Jacinle


export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export CUDA_HOME=/usr/local/cuda-10.2 
export CUDAHOME=/usr/local/cuda-10.2
export CUDA_DEVICE_ORDER=PCI_BUS_ID

export MMF_HOME=/users/visics/zwang/miniconda3/envs/torch15/lib/python3.8/site-packages/mmf

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/users/visics/zwang/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/users/visics/zwang/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/users/visics/zwang/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/users/visics/zwang/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


export FZF_DEFAULT_OPTS='--height 40% --border --layout=reverse'

# add explicity PATH because of strange error occured when desktop restart
export PATH=/users/visics/zwang/.fzf/bin:$PATH

[ -f ~/.fzf.bash ] && source ~/.fzf.bash

# redirect picture file
export PICTURES=/users/visics/zwang/Pictures
