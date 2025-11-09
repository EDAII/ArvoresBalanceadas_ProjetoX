# Simulador de Logistica 

**Conteúdo da Disciplina**: Ávores Balanceadas

-----

## Sobre o Projeto

Uma simulação 2D em Python e Pygame de um robô de logística em um armazém. Este projeto demonstra visualmente algoritmos de pathfinding (A*) e o uso de Árvores de Busca Balanceadas (Árvore AVL e Rubro-Negra) para gerenciar uma fila de pedidos em tempo real.

O projeto utiliza uma arquitetura "híbrida" desacoplada:
* **Cérebro de Alto Nível (Raspberry Pi):** Um simulador (`cerebro_pi.py`) que toma decisões estratégicas, como calcular a rota ideal (A*) e gerenciar a fila de pedidos (AVL e Rubro-Negra).
* **Controlador de Baixo Nível (ESP32):** Um simulador (`robo.py`) que apenas executa comandos simples ("Vá para frente", "Pare") e reporta status (sensores, chegada).

-----

## Contribuidores

<center>

</head>
<body>

<table>
    <thead>
        <tr>
            <th>Matrícula</th>
            <th>Nome</th>
            <th>GitHub</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>202046102</td>
            <td>Felipe das Neves Freire</td>
            <td><a href="https://github.com/FelipeFreire-gf" target="_blank">Felipe</a></td>
        </tr>
        <tr>
            <td>222037700</td>
            <td>Leonardo de Melo Lima</td>
            <td><a href="https://github.com/leozinlima" target="_blank">Leonardo</a></td>
        </tr>
    </tbody>
</table>

</body>
</html>

</center>

-----

## Funcionalidades

* **Simulação 2D:** Interface gráfica com 3 painéis (Controle, Mundo, Status) construída com Pygame.
* **Pathfinding com A*:** O robô usa o algoritmo A-star (A*) para encontrar o caminho mais curto entre dois nós no mapa do armazém.
* **Fila de Pedidos com Árvore AVL e Rubro-Negra:**
    * Novos pedidos são adicionados a uma **Árvore AVL e Rubro-Negra**, que se mantém balanceada.
    * O robô sempre pega o pedido com o **menor ID** (o nó mais à esquerda da árvore) como prioridade.
    * Quando um pedido é concluído, o nó é **removido** da árvore.
* **Visualização de Dados:**
    * A Árvore AVL de pedidos é desenhada e atualizada em tempo real, permitindo ver as **rotações** de balanceamento quando nós são inseridos ou removidos.
    * Um painel de "Log do Sistema" mostra todas as ações do robô e da árvore.
* **Controle Interativo:**
    * **Pausar/Iniciar:** A barra de espaço alterna o estado do robô (ATIVO/PAUSADO).
    * **Criar Pedidos:** A tecla 'P' permite ao usuário digitar um nó de destino (A-P) para criar um novo pedido com ID aleatório.
    * **Pedidos Prioritários:** Clicar diretamente em um nó no mapa cria um pedido de prioridade máxima (ID 0).
* **Design Modular:** O mapa do armazém (nós e conexões) é definido inteiramente no `config.py`, permitindo fácil expansão ou modificação do layout.

-----

## Tecnologias Utilizadas

* **Python 3**
* **Pygame:** Para o loop principal, visualização e manipulação de eventos.
* **`astar` (biblioteca):** Para a implementação do algoritmo A*.

-----

## Screenshots

<div align="center">
  <font size="4"><p style="text-align: center; margin-bottom: 50px;"><b>Figura 1: Nosso Projeto Rodando</b></p></font>
</div>

<div align="center">
<img src="imagensReadme/projetoX.png" alt="inicial" style=" max-width: 50%; height: auto; margin-bottom: 20px;">
</div>

<div align="center">
  <font size="4"><p style="text-align: center; margin-bottom: 50px;"><b>Figura 2: Código da Busca Binária</b></p></font>
</div>

<div align="center">
<img src="Assets/Images/codigoBusca.png" alt="inicial" style=" max-width: 50%; height: auto; margin-bottom: 20px;">
</div>

<div align="center">
  <font size="4"><p style="text-align: center; margin-bottom: 50px;"><b>Figura 3: Código da Busca Linear</b></p></font>
</div>

<div align="center">
<img src="Assets/Images/buscaLinear.png" alt="inicial" style=" max-width: 50%; height: auto; margin-bottom: 20px;">
</div>

-----

## Como Executar

1.  **Clone ou baixe** este repositório para o seu computador.
2.  **Crie um ambiente virtual** (recomendado):
    ```bash
    python -m venv venv
    ```
3.  **Ative o ambiente virtual:**
    * No Windows (PowerShell): `.\venv\Scripts\Activate`
    * No macOS/Linux: `source venv/bin/activate`
4.  **Instale as dependências:**
    ```bash
    pip install pygame astar
    ```
5.  **Execute a simulação:**
    ```bash
    python main.py
    ```
-----

## Como Usar

1.  **Inicie o programa.** O robô começará `PAUSADO` no Nó 'A'.
2.  **Crie Pedidos:**
    * Aperte a tecla **'P'**.
    * Digite o nó de destino (ex: `G`) e aperte **ENTER**; obs: **ENTER** do teclado numérico não costuma funcionar.
    * Faça isso várias vezes (ex: `P`, `F`, ENTER, `P`, `K`, ENTER) para criar vários pedidos. Você verá a **Árvore AVL** crescer e se balancear no painel da direita.
3.  **Inicie o Robô:**
    * Aperte **ESPAÇO** para mudar o status do robô para `ATIVO`.
4.  **Assista:**
    * O robô automaticamente pegará o pedido de menor ID da árvore.
    * A "raspberry" calculará a rota A* e o robô começará a se mover.
    * Ao chegar, o robô entregará o pacote, o nó será **removido** da Árvore AVL (que se rebalanceará), e ele pegará o próximo pedido da fila.
5.  **Pause/Continue:** Você pode apertar **ESPAÇO** a qualquer momento para pausar ou continuar o trabalho do robô.

-----

## Vídeo

<a href="https://youtu.be/TFeyVYnvyy4" target="_blank">
    <p align="center"><strong>Vídeo do Projeto</strong></p>
</a>
<p align="center">
  <a href="https://youtu.be/TFeyVYnvyy4" target="_blank">
    <img src="https://img.youtube.com/vi/TFeyVYnvyy4/0.jpg" alt="Vídeo 01" width="480">
  </a>
</p>
