O Organize é uma aplicação web feita com **Flask** e **PostgreSQL**. O código segue a organização **MVC**, que separa os dados, as telas e o processamento das requisições.

- **Model (`models/`)** — define os dados armazenados no banco, como lançamentos, investimentos e aportes.
- **View (`views/`)** — reúne os arquivos HTML que mostram os formulários e os resultados. O CSS, o JavaScript e as imagens ficam em `static/`.
- **Controller (`controllers/`)** — recebe as ações do usuário, consulta ou atualiza o banco e envia os dados para a tela.

