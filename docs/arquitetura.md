O Organize é uma aplicação web feita com **Flask** e **PostgreSQL**. O código segue a organização **MVC**, que separa os dados, as telas e o processamento das requisições.

- **Model (`models/`)** — define os dados armazenados no banco, como lançamentos, investimentos e aportes.
- **View (`views/`)** — reúne os arquivos HTML que mostram os formulários e os resultados. O CSS, o JavaScript e as imagens ficam em `static/`.
- **Controller (`controllers/`)** — recebe as ações do usuário, consulta ou atualiza o banco e envia os dados para a tela.

Um exemplo é o relatório por período. O controlador valida as datas escolhidas, busca os lançamentos e soma os aportes daquele intervalo. O ServicoRelatorio, em services/, calcula o saldo e organiza os gastos por categoria. Depois, a página relatorios.html exibe os resultados.

Essa separação facilita a manutenção. As regras de cálculo ficam fora do HTML, e o menu é reutilizado pelas páginas principais por meio do arquivo views/navbar.html. Assim, uma mudança no menu pode ser feita em um só lugar.