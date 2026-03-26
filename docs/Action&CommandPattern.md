# Actions & Command Pattern

A espinha dorsal de interatividade do Spectrum 3 foi desenhada para garantir um desacoplamento absoluto entre a Interface Gráfica e a Lógica de Negócio. Inspirado em arquiteturas modernas de alta performance, o pipeline divide a execução de tarefas em dois paradigmas distintos, **Ações** e **Comandos**, governados por um sistema de metadados.

### 1. A Dicotomia de Execução (Actions vs. Commands)

Para evitar a poluição do histórico de edições e suportar operações assíncronas de forma segura, o sistema classifica as interações em dois tipos:

* **Actions (Ações Puras):** Funções *stateless*, sem estado, frequentemente assíncronas, que executam tarefas de sistema, navegação, chamadas HTTP ou interações com hardware. **Não** afetam o histórico do documento. Exemplo: *Iniciar Sessão (Login), Abrir Janela de Preferências, Solicitar Telemetria MQTT.*  
* **Commands (Comandos de Edição):** Operações síncronas e reversíveis que mutam o estado dos dados do utilizador. São encapsulados no padrão `QUndoCommand` e empurrados para a `QUndoStack`, fornecendo suporte automático a *Undo/Redo* (`Ctrl+Z` / `Ctrl+Y`). Exemplo: *Mover Área de Inspeção, Aplicar Filtro de Imagem, Alterar Contraste.*

### 2. Componentes Centrais da Arquitetura  

O fluxo de interatividade transita pelos seguintes componentes principais:

* **CommandDescriptor (Metadados e Roteamento Visual):** Estrutura central que define a identidade de uma ação (ID, Texto, Ícone). O descritor atua como o motor de **Data-Driven UI**, possuindo *flags* de roteamento (`showInMenu`, `showInPalette`, `showInToolbar`) e caminhos hierárquicos (`menuPath`). Isso permite que um plugin dite exatamente onde e como a sua ação será visível na interface, sem escrever uma única linha de QML.  
* **CommandRegistry (O Repositório):** Implementação do `ICommandRegistry` que atua como o cofre central do sistema. Durante o bootstrap, os plugins injetam as suas *Actions* via `ActionHandler` e as suas *Commands* via `CommandFactory` neste registo.  
* **ActionDispatcher (O Orquestrador):** O único ponto de entrada para invocar uma operação. A UI (QML) nunca chama um plugin diretamente; ela pede ao Dispatcher para executar um `commandId`. O Dispatcher consulta o Registry, descobre se a operação é uma *Action* executando-a imediatamente ou um *Command* instanciando a fábrica e empurrando o objeto para a `QUndoStack`.

### 3. Consumo Reativo pela Interface (QML)

Para que a interface gráfica reaja dinamicamente aos plugins instalados, o Core fornece modelos C++ rigorosamente otimizados para o Qt:

* **MenuModel:** Transforma a lista plana de metadados do `CommandRegistry` numa estrutura hierárquica em árvore `QAbstractItemModel`. Ignora comandos internos e constrói as barras de menu tradicionais da aplicação ex: `*Arquivo > Exportar*`.  
* **CommandSearchModel:** Fornece uma lista plana filtrável em tempo real (`QAbstractListModel`). É o cérebro por trás da **Paleta de Comandos** (*Command Palette*), permitindo que os utilizadores localizem e executem ações rapidamente através de pesquisa por texto, atalho global `Ctrl+Shift+P`, ocultando ações marcadas como puramente internas.

![](images/diagrams/CommandPipeline.png)
![](images/diagrams/CommandView_Architecture.png)