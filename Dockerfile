FROM ubuntu:xenial

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y flex bison qt5-default openjdk-8-jre python

RUN mkdir /solvers /solvers_exec
COPY ./ortools /solvers/ortools
COPY ./choco_exec /solvers_exec/choco_exec
COPY ./chuffed /solvers/chuffed
ADD https://github.com/MiniZinc/MiniZincIDE/releases/download/2.1.6/MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz /MiniZincIDE.tgz
ADD https://github.com/google/or-tools/releases/download/v6.5/or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527.tar.gz /or-tools.tar.gz
ADD https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-4.0.4/choco-parsers-4.0.4-with-dependencies.jar /

# RUN apk --update add --virtual build-deps openssl openjdk8-jre python python-dev libc6-compat libstdc++ g++ && \
# wget -O MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz https://github.com/MiniZinc/MiniZincIDE/releases/download/2.1.6/MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
# wget -O or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527.tar.gz https://github.com/google/or-tools/releases/download/v6.5/or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527.tar.gz && \
# wget -O choco-parsers-4.0.4-with-dependencies.jar https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-4.0.4/choco-parsers-4.0.4-with-dependencies.jar && \



RUN cd / && tar zxvf MiniZincIDE.tgz && \
	rm -rf MiniZincIDE.tgz && \
	mv MiniZincIDE-2.1.6-bundle-linux-x86_64 /minizinc && \
	tar xvfz or-tools.tar.gz && \
	rm or-tools.tar.gz && \
	mv or-tools_flatzinc_Ubuntu-16.04-64bit_v6.5.4527 /solvers_exec/ortools_exec && \
	cp -R /solvers_exec/ortools_exec/share/minizinc_cp /minizinc/share/minizinc/ortools && \
	mv choco-parsers-4.0.4-with-dependencies.jar /solvers_exec/choco_exec/ && \
	cp /minizinc/fzn-chuffed /solvers/chuffed/fzn_chuffed && \
  rm -rf /var/lib/apt/lists/*

ENV PATH /minizinc:/solvers/choco_exec:/solvers/ortools:$PATH
