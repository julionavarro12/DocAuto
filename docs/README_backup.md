# Documento de Arquitetura: Spectrum 3 (v2)

**Autor:** André Luz  
**Contato:** andre.luz@vmis.com.br  
**Paradigma:** Microkernel / Plugin-Based Architecture  
**Status:** Ativo  
**Versão:** 1.0  

---  

## Introdução

Este documento adota dois modelos de representação arquitetural: o *C4 Model* e a *UML (Unified Modeling Language)*, utilizados para descrever diferentes níveis de abstração do sistema.  

---  

## 1. Visão Geral e Objetivos Estratégicos

O Spectrum 3 (v2) é a nova geração do ecossistema de inspeção da VMI, fundamentado no padrão arquitetural Microkernel. Esta arquitetura foi projetada para oferecer uma velocidade de resposta sem precedentes às demandas do mercado, permitindo a implementação de novas funcionalidades e customizações especiais para clientes em tempo recorde.

Graças ao desacoplamento total entre o núcleo (Core) e as extensões (Plugins), é possível realizar entregas customizadas sem que isso afete a estabilidade do sistema ou gere dívidas técnicas que limitem o crescimento futuro da plataforma. O sistema passa a ser um ecossistema evolutivo e sustentável em longo prazo.

![Visão Geral do Sistema](images/diagrams/VisaoGeral.png)


## 2. Critérios de Aceitação e Validação

Para garantir a superioridade técnica o sistema deve atender aos seguintes requisitos:

+ **Acoplamento Mínimo:** Separação física entre SDK, Core e Implementações.  
+ **C++ Moderno (C++17/20/23):** Uso de RAII e *Smart Pointers*.  
+ **Performance de UI:** Interfaces responsivas através de modelos assíncronos e `QAbstractItemModel`.  
+ **Resiliência:** Ampla cobertura de testes unitários no **Core**.  

[Critérios de Aceitação e Validação](CriteriosDeAvaliacaoDeArquitetura.md)

## 3. Qualidade de Engenharia e Fluxo de Desenvolvimento

O fluxo de trabalho garante que o "Core" do sistema seja resiliente a regressões.  

* **Fase POC:** Validação rápida de funcionalidades.  
* **Fortalecimento do Core:** Implementação de testes unitários para cobrir e proteger o Core de plugins defeituosos.  
* **Ciclo de Correção:** Cada bug identificado gera um teste de reprodução que falha propositalmente antes da correção, essa abordagem evita regreções.  

![Fluxo de Desenvolvimento](images/diagrams/UML_QA.png)


## 4. Contêineres e Integrações  

o Spectrum 3 se comunica com microserviços internos para processamento e gestão de dados:

![Visão Geral do Sistema](images/diagrams/SpectrumMicroservices.png)


## 5. Divisão de Responsabilidades

A arquitetura é dividida em camadas para garantir a evolução do software:

* **SDK:** Define os contratos (Interfaces) e tipos fundamentais. Dependência comum a todos os módulos.
* **Core:** Implementa o motor de plugins, barramento de eventos e serviços base.
* **App:** O executável principal que orquestra o boot e as janelas ou modo headless.
* **Plugins:** Extensões dinâmicas (.so) que injetam regras de negócio.

![Spectrum](images/diagrams/Spectrum.png)
![Dentro do Spectrum 3 (v2)](images/diagrams/InsideSpectrum3.png)

## 6. Detalhamento Técnico e Decisões Arquiteturais

### 6.1 Ciclo de Vida e Bootstrapping (Dual-Engine)

O sistema utiliza uma abordagem de **Dual-Engine** para garantir que a UI não congele durante o carregamento.

* **Engine A (Splash):** Sobe imediatamente para dar feedback ao usuário sobre o carregamento dos plugins.
* **Engine B (Main UI):** Inicializada de forma limpa com todos os plugins necessários carregados.

![Bootstrapping](images/diagrams/SequenceBootstrappingDualEngine.png)

### 6.2 Plugins e Extensibilidade

A descoberta de plugins ocorre em duas fases:
1.  **Static Discovery:** O `PluginScanner` extrai metadados JSON sem carregar a biblioteca na memória (Lazy Loading).
2.  **Dynamic Loading:** Carregamento real via `PluginLoader` encapsulado em contratos RAII.
* **Extension Broadcasting:** O sistema notifica os `IPluginExtensionHandlers` para injetar comandos, views, e outros componentes passivamente.

![PluginLifecycle](images/diagrams/SequencePluginLifecycle.png)


### 6.3 Padrão Extension Object  

A interface base `IPlugin` expõe o método genérico `extension()`. Em vez de o Core conhecer todas as possíveis interfaces em tempo de compilação, o plugin devolve ponteiros para suas implementações com base em identificadores dinâmicos ex: `"vmi.sdk.IAuthService"`.
* **Benefícios:** Reduz o acoplamento, evita o overhead de múltiplos `dynamic_cast` e facilita a evolução contínua das APIs.


### Para tornar o conceito mais claro, a explicação será apresentada em três camadas complementares, primeiro uma analogia com o mundo real, em seguida o fluxo técnico detalhado e, por fim, os fundamentos que permitem a escalabilidade praticamente ilimitada desse modelo.

O padrão de `extensions` também conhecido como *Extension Object Pattern* é um dos padrões mais poderosos para arquiteturas escaláveis.

#### 6.3.1. A Analogia: A Recepção do Prédio

Imagine que um Plugin é um grande prédio comercial.  

Numa abordagem tradicional **(herança múltipla)**, o próprio prédio tenta **"SER"** o cozinheiro, o segurança, o faxineiro e o contador ao mesmo tempo.  
Se o sistema precisa de um balancete, ele pede para o prédio.  
Se o prédio cresce e passa a oferecer 50 serviços diferentes, ele vira um monstro impenetrável, a famosa *God Class*, ou seja uma classe que herda muitas interfaces.

Com a abordagem do mecanismo de `extension()`, o prédio passa a ter apenas uma **Recepcionista**.  

1. O Core é como se fosse um **"visitante"** chega na recepção e pergunta: *"Com licença, vocês têm um departamento de Interface Gráfica (IViewContributor)?"*  
2. A recepcionista olha a lista de extensões `extensionId`.  
3. Se tiver, ela entrega um crachá de acesso genérico `void*` apontando exatamente para a sala onde fica o especialista de UI.  
4. Se não tiver, ela responde *"Não"* `nullptr`, e o visitante simplesmente vai embora sem causar erros.  

#### 6.3.2. O Caminho Técnico

No código, esse fluxo acontece em três etapas bem definidas e totalmente isoladas:

**Passo 1: O Contrato SDK**  

O SDK define o que é esperado de um especialista e cria uma **"senha"** única para ele o "`IID` - Interface ID". Por exemplo, quem quer desenhar telas precisa falar o idioma `vmi.sdk.IViewContributor`.

**Passo 2: O Plugin**  

O Plugin implementa a interface base `IPlugin`, que possui a função vital `virtual void* extension(const QString& extensionId) = 0;`.  

Internamente, o plugin instancia classes menores e especializadas. Quando a função é chamada, ela atua como um roteador de tráfego.

```cpp
void* MeuPlugin::extension(const QString& iid) {
    if (iid == "vmi.sdk.IViewContributor") {
        return m_meuEspecialistaDeViews; // Retorna o ponteiro disfarçado de void*
    }

    if (iid == "vmi.sdk.ICommandContributor") {
        return m_meuEspecialistaDeComandos;
    }

    return nullptr; // "Não oferecemos esse serviço"
}
```

**Passo 3: O Core / Extension Handlers**  

Quando o Core carrega a `DLL/.so` do plugin, ele não sabe o que o plugin faz. Ele tem um *Helper* elegante no SDK, o `getExtension<T>()`, que automatiza a pergunta para a recepcionista.

```cpp
// "Olá Plugin, você tem o IViewContributor?"
if (auto* views = instance->plugin()->getExtension<IViewContributor>()) {
    // "Opa, ele tem! Vou pegar as telas dele e desenhar."
    registry.registerViews(views->views());
}
```

#### 6.3.3. Por que isso permite estender os plugins "infinitamente"?  

A magia real dessa abordagem reside em dois princípios arquiteturais de alto nível, **Inversão de Dependência** e **Open/Closed Principle (OCP)**.  

* **Fim da Herança Quebrada:** Se você adiciona uma funcionalidade nova no sistema (ex: `IHardwareScanner`), você não precisa alterar a interface base `IPlugin`.  
Consequentemente, nenhum plugin antigo, como o de **Login** ou **About** irão quebrar.  
Eles simplesmente continuarão retornando `nullptr` se alguém perguntar se eles sabem **"escanear"**.  
* **Composição Isolada:** Um plugin gigantesco não precisa herdar 20 interfaces. Ele pode ter 20 arquivos diferentes, cada um focado em uma tarefa mínima e isolada. A classe central do Plugin só precisa instanciar esses 20 arquivos e rotear a string de ID para eles.  
* **Segurança de Memória (`void*` vs `static_cast`):** Como a passagem de fronteira entre o Plugin e o Core é feita através de um ponteiro genérico bruto `void*` e depois moldada `static_cast` de volta para uma interface puramente virtual, as chances de corrupção de memória por desalinhamento de tabela virtual `VTable` caem drasticamente.

Em resumo, o mecanismo de `extensions` transforma os plugins em uma espécie de "Hub USB". Você pode plugar qualquer dispositivo (interface) no futuro, se a porta (ID) existir, a comunicação acontece, se não existir, o sistema segue a vida silenciosamente.

---  

### 6.4 Barramento de Eventos (EventBus)  

Sistema Pub/Sub thread-safe e fortemente tipado.

* **Type Erasure:** Converte callbacks tipados em identificadores genéricos para remover acoplamento de hierarquia.
* **Deadlock Prevention:** Callbacks são executados fora do escopo do lock de escrita.

[Detalhamento do EventBus](EventBus.md)

![EventBus](images/diagrams/Class_EventBus.png)


### 6.5 Pipeline de Interatividade (Command Pattern e Action)  

A espinha dorsal de interatividade do Spectrum 3.

* **Action Dispatcher:** Orquestra a execução e insere comandos na `QUndoStack` para suporte nativo a Undo/Redo.
* **MenuModel:** Transforma o estado flat do registro de comandos em um modelo hierárquico para o QML.

![CommandPattern](images/diagrams/CommandPipeline.png)


### 6.6 Serviços de Infraestrutura  

* **Service Registry:** Repositório seguro para resolução de serviços via IID.
* **Preferences Engine:** Agrega descritores de preferências em árvores de categorias para renderização dinâmica na UI.
* **Auth & Network:** Fluxos assíncronos que utilizam o `IHttpService` e notificam o sistema via `EventBus`.
* **Dialog Service:** Orquestração assíncrona de diálogos QML via sinalização C++, desacoplando a lógica de negócio da renderização visual.

![Infraestrutura](images/diagrams/ServiceRegistry.png)



## 7. Engine de Preferências e Configurações

A **Engine de Preferências** foi projetada como um sistema descentralizado e extensível, permitindo que tanto o núcleo da aplicação quanto plugins externos contribuam com configurações de forma padronizada. A arquitetura garante que a lógica de apresentação seja independente da persistência de dados.

### Pilares da Arquitetura

#### 1. Extensibilidade via SDK (IPreferencesContributor)  

Para suportar a arquitetura baseada em plugins, o sistema expõe o contrato `IPreferencesContributor`. Através deste contrato, qualquer módulo pode injetar `PreferenceDescriptors` no sistema sem conhecer os detalhes da UI ou do backend de armazenamento. Isso garante que novos recursos do sistema possam expor suas próprias configurações de forma plug-and-play.

#### 2. Orquestração Dinâmica (PreferencesRegistry)  

O `PreferencesRegistry` atua como o cérebro da engine. Ele é responsável por agregar todos os descritores contribuídos e organizá-los em uma estrutura de árvore composta por `CategoryNodes` e `SubCategoryNodes`.  
* **Gestão de Árvore:** Centraliza a hierarquia das configurações, permitindo que a interface seja construída de forma recursiva e dinâmica.  
* **Desacoplamento:** A UI lê apenas a estrutura organizada, o "quê" e "onde", sem precisar conhecer a origem de cada configuração.

#### 3. Abstração de Persistência (SettingsService & Backends)  

O sistema isola a lógica de I/O através de uma camada de serviço. O `SettingsService` atua como um *wrapper* que encapsula o backend físico, utilizando o padrão **Bridge** para suportar diferentes implementações de armazenamento, como o `QSettingsBackend` e pode no futuro utilizar por exemplo `SQLiteBackend`.  

* **Consistência:** Garante que a gravação dos dados ocorra de forma centralizada e atômica.
* **Portabilidade:** Facilita a troca do formato de armazenamento (JSON, XML, SQLite ou Registro do Windows) sem impacto nos módulos que consomem as configurações.

#### 4. Interface Reativa  

A camada de apresentação em **QML** consome a árvore de categorias gerada pelo Registry para renderizar os painéis de configuração em tempo de execução.  

* **Renderização Baseada em Metadados:** A UI não é **"hardcoded"**; ela se adapta aos plugins carregados no sistema.  
* **Fluxo de Dados:** A UI lê a estrutura do Registry, mas interage diretamente com o `SettingsService` para a gravação de valores, garantindo uma separação clara entre a **definição da configuração** e o **valor da configuração**.

![Preferences Engine](images/diagrams/PreferencesEngine.png)


## 8. Gerenciamento de Sessão Guiado por Políticas (Policy-Driven Authentication)

O Spectrum 3 opera com uma arquitetura de "Casca" (Shell), o que significa que funcionalidades centrais, incluindo a Autenticação, são injetadas dinamicamente via plugins. Para garantir a segurança, o ciclo de vida da sessão é governado por um sistema de Políticas de Execução.

### 8.1. O Arquivo de Licença e Configuração Segura

A aplicação consome um arquivo de configuração assinado digitalmente, similar a um token JWT, durante a inicialização. Este arquivo contém os metadados invioláveis que ditam as regras de funcionamento do Core.  
A principal diretiva de segurança verificada nesta etapa é a chave `authenticationRequired`, que informa à máquina de estados se o software tem permissão para operar num modo aberto (ex: ambiente de demonstração) ou se exige controle de acesso.  

### 8.2. Matriz de Resolução de Estado (Evaluating Policy)

Logo após o boot e antes de instanciar a interface gráfica principal (Engine MainUI), o SessionManager cruza a diretiva da licença com a presença real do IAuthService no ServiceRegistry. Este cruzamento gera quatro cenários possíveis:

+ Obrigatório e Presente **(authRequired = true | Plugin = OK)**: O fluxo de segurança padrão. A aplicação transita para o estado de Autenticação e exige credenciais válidas antes de libertar o uso do software.

+ Obrigatório e Ausente **(authRequired = true | Plugin = NULL)**: Cenário de violação de integridade. Se um utilizador mal-intencionado apagar a DLL/SO do plugin de autenticação para tentar burlar o login, o Core detecta a discrepância com a licença e aborta a inicialização, transitando para um Erro Fatal na Splashscreen.

+ Opcional e Presente **(authRequired = false | Plugin = OK)**: O plugin foi instalado e está ativo. A aplicação transita para o estado de Autenticação normalmente, aproveitando a infraestrutura existente para identificar o operador, mesmo não sendo uma exigência contratual restrita.

+ Opcional e Ausente **(authRequired = false | Plugin = NULL)**: O modo White-Label / Demonstração. O sistema reconhece que não há obrigatoriedade de login e que o módulo não está instalado. A etapa de autenticação é ignorada de forma segura, transitando diretamente para o estado Ativo, interface principal.

### 8.3. Ciclo de Vida da Máquina de Estados (FSM)

O fluxo do SessionManager obedece aos seguintes estados:

+ **Initializing:** O Core está inicializa os serviços e a carregar as bibliotecas dinâmicas (.so/.dll). A Splashscreen está visível.  
+ **EvaluatingPolicy:** O ponto de verificação de segurança onde a matriz acima é avaliada.  
+ **Authenticating:** Estado de bloqueio. A interface principal aguarda até que o AuthService valide as credenciais fornecidas pelo utilizador e emita o evento loginSuccess().  
+ **Active:** O usuário está autenticado, ou a autenticação foi ignorada por política. O ambiente de trabalho principal do Spectrum 3 é libertado para uso. Um comando de logout() devolve o sistema ao estado Authenticating.  
+ **FatalError:** Estado terminal. O sistema foi bloqueado por falha na verificação de integridade da política de segurança.  

![](images/diagrams/SessionManager.png)