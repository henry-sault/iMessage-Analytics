FROM jupyter/base-notebook

ARG FILE_NAME

WORKDIR /
USER root

RUN echo "c.NotebookApp.token = ''" >> ./etc/jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> ./etc/jupyter/jupyter_notebook_config.py


WORKDIR /home/jovyan/work


RUN cd .. && \
    sudo rm -rf ./work/
COPY /src/ .
COPY requirements.txt .
COPY ${FILE_NAME} .
RUN chown -R jovyan:root .

USER jovyan


# RUN sudo chown -R root ./src/

RUN pip install -r requirements.txt

