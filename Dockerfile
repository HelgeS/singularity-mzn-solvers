FROM alpine:3.6

# Install packages for compiling the feature extractor
#RUN apt-get update && apt-get upgrade -y && \
#  apt-get install -y flex bison qt5-default && \
#  rm -rf /var/lib/apt/lists/*
RUN mkdir /solvers
COPY ./ortools /solvers/ortools
COPY ./choco_exec /solvers/choco_exec
COPY ./chuffed /solvers/chuffed

RUN apk --update add --virtual build-deps openssl openjdk8-jre python python-dev libstdc++ g++ && \
	wget -O MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz https://github.com/MiniZinc/MiniZincIDE/releases/download/2.1.6/MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
	tar zxvf MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
	rm -rf MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
	mv MiniZincIDE-2.1.6-bundle-linux-x86_64 /minizinc && \
	wget -O or-tools_flatzinc_Ubuntu-14.04-64bit_v6.5.4527.tar.gz https://github.com/google/or-tools/releases/download/v6.5/or-tools_flatzinc_Ubuntu-14.04-64bit_v6.5.4527.tar.gz && \
	tar xvfz or-tools_flatzinc_Ubuntu-14.04-64bit_v6.5.4527.tar.gz && \
	rm or-tools_flatzinc_Ubuntu-14.04-64bit_v6.5.4527.tar.gz && \
	mv or-tools_flatzinc_Ubuntu-14.04-64bit_v6.5.4527 ortools_exec && \
	cp -R ortools_exec/share/minizinc_cp /minizinc/share/minizinc/ortools && \
	wget -O choco-parsers-4.0.4-with-dependencies.jar https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-4.0.4/choco-parsers-4.0.4-with-dependencies.jar && \
	mv choco-parsers-4.0.4-with-dependencies.jar /solvers/choco_exec/ && \
	cp /minizinc/fzn-chuffed /solvers/chuffed/fzn_chuffed && \
	rm -rf /var/cache/apk/*

ENV PATH /minizinc:/solvers/choco_exec:/solvers/ortools:$PATH
RUN ls -l /minizinc/
