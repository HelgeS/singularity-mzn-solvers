# Abel HPC has only singularity 2.3.2, which somehow requires the two-step creation process
# Once it has 2.4, singularity build mzn-solvers.img Singularity can be used. This will also result in smaller images.
sudo rm mzn-solvers.img
sudo singularity image.create -s 1500 mzn-solvers.img
sudo singularity bootstrap mzn-solvers.img Singularity
