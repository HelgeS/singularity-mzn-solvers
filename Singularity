BootStrap: docker
From: ubuntu:xenial

%setup
cp ./main.py ${SINGULARITY_ROOTFS}/main.py
cp -R ./solvers ${SINGULARITY_ROOTFS}/solvers
cp -R ./solvers_exec ${SINGULARITY_ROOTFS}/solvers_exec

%post
DEBIAN_FRONTEND=noninteractive apt-get update  # need to update, otherwise qt5-default is not found
DEBIAN_FRONTEND=noninteractive apt-get install -y flex bison qt5-default openjdk-8-jre python wget

wget https://github.com/MiniZinc/MiniZincIDE/releases/download/2.1.7/MiniZincIDE-2.1.7-bundle-linux-x86_64.tgz
wget https://github.com/google/or-tools/releases/download/v6.8/or-tools_flatzinc_ubuntu-16.04_v6.8.5452.tar.gz
wget https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-4.0.4/choco-parsers-4.0.4-with-dependencies.jar
#wget http://ie.technion.ac.il/~ofers/HCSP/hcsp-1.3.0-x86_64.tar.xz
#wget http://strichman.net.technion.ac.il/files/2016/07/hcsp-mzn-lib.tar_.zip

tar zxf MiniZincIDE-2.1.7-bundle-linux-x86_64.tgz
rm MiniZincIDE-2.1.7-bundle-linux-x86_64.tgz
mv MiniZincIDE-2.1.7-bundle-linux-x86_64 /minizinc

# Link minizinc bundle solvers to paths the main.py script knows
mkdir /solvers_exec/chuffed_exec
ln -s /minizinc/fzn-chuffed /solvers_exec/chuffed_exec/fzn_chuffed
ln -s /minizinc/share/minizinc/chuffed /solvers/chuffed/mzn-lib
ln -s /minizinc/share/minizinc/gecode /solvers/gecode/mzn-lib

cat /solvers/chuffed/int_pow.mzn >> /solvers/chuffed/mzn-lib/redefinitions.mzn

# or-tools
tar xzf or-tools_flatzinc_ubuntu-16.04_v6.8.5452.tar.gz
rm or-tools_flatzinc_ubuntu-16.04_v6.8.5452.tar.gz
mv or-tools_flatzinc_Ubuntu-16.04-64bit_v6.8.5452 /solvers_exec/ortools_exec
ln -s /solvers_exec/ortools_exec/share/minizinc_sat /minizinc/share/minizinc/ortools
ln -s /solvers_exec/ortools_exec/bin/fzn-or-tools /solvers/ortools/fzn-exec
cp /solvers_exec/ortools_exec/share/minizinc_sat/*mzn /solvers/ortools/mzn-lib/

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
#PATH=/minizinc:/solvers_exec/choco_exec:/solvers/ortools:$PATH
PATH=/minizinc:/solvers/ortools:$PATH
export PATH
