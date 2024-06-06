
# Projeto - Modern stack

  

Para esse projeto, foi criado uma arquitetura básica de "Modern Stack".
O projeto consiste basicamente em:

 1. Coletar dados do **Google Sheets** através do **Airbyte**
 2. Levar esses dados até um schema **Bronze** em um banco de dados **Postgres**
 3. Realizar uma transformação básica de dados pelo **dbt Cloud**, lendo dados da **Bronze** e criando um novo schema **Gold** e nova tabela com os dados transformados.
 4. Realizar a orquestração de todo o processo através do **Airflow**, utilizando uma **DAG** para executar cada step acima.
 5. Por trás de tudo isso, foram utilizadas bibliotecas de desenvolvimento como **Poetry**, **Pyenv** e também o **Astro Python SDK** 

Para ilustrar o fluxo:

```mermaid
graph LR
A[Google Sheets] -- Airbyte --> B((Postgres Bronze))
B -- dbt Cloud --> C{Postgres Gold}
A -- Airflow--> C