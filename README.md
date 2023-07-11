# database-viewer

Repository to handle chat.db files or csv files and transform into desired tables with guided user input. 

## To Run Jupyter Notebook Container

Container can be built using Makefile commands
Need to change **make build_jupyter** command in order to successfully import file into jupyter notebook environment.

Run the following to build and deploy jupyter notebook instance to the url **http://localhost:8888/lab**:
```
make build_jupyter
make run_jupyter
```
