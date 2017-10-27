BootStrap: docker
From: ubuntu:xenial

%setup
cp ./main.py ${SINGULARITY_ROOTFS}/main.py
cp -R ./solvers ${SINGULARITY_ROOTFS}/solvers
cp -R ./solvers_exec ${SINGULARITY_ROOTFS}/solvers_exec

%post
DEBIAN_FRONTEND=noninteractive apt-get update  # need to update, otherwise qt5-default is not found
DEBIAN_FRONTEND=noninteractive apt-get install -y flex bison qt5-default openjdk-8-jre python wget

wget https://github.com/MiniZinc/MiniZincIDE/releases/download/2.1.6/MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz
wget https://github.com/google/or-tools/releases/download/v6.5/or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527.tar.gz
wget https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-4.0.4/choco-parsers-4.0.4-with-dependencies.jar

tar zxvf MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz
rm MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz
mv MiniZincIDE-2.1.6-bundle-linux-x86_64 /minizinc

# Link minizinc bundle solvers
mkdir /solvers_exec/chuffed_exec
ln -s /minizinc/fzn-chuffed /solvers_exec/chuffed_exec/fzn_chuffed
cp /minizinc/share/minizinc/gecode/* /solvers/gecode/mzn-lib/

# or-tools
tar xvzf or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527.tar.gz
rm or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527.tar.gz
mv or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527 /solvers_exec/ortools_exec
ln -s /solvers_exec/ortools_exec/share/minizinc_cp /minizinc/share/minizinc/ortools

mv choco-parsers-4.0.4-with-dependencies.jar /solvers_exec/choco_exec/

python2 solvers/make_pfolio.py

rm -rf /var/lib/apt/lists/*

# For abel compatibility
mkdir /cluster /work /usit /projects

%runscript
echo "Arguments: $*"
cd /
exec python2 main.py $@

%environment
PATH=/minizinc:/solvers_exec/choco_exec:/solvers/ortools:$PATH
export PATH
