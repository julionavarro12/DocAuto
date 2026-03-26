> Geração Automática de Documentação de Código | Versão 1.0 | Linux
> 
> 
> **Autor:** Júlio Oliveira
> 

---

## Sumário

1. [Visão Geral](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#1-vis%C3%A3o-geral)
2. [Pré-requisitos](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#2-pr%C3%A9-requisitos)
3. [Instalação](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#3-instala%C3%A7%C3%A3o)
4. [Comandos Básicos](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#4-comandos-b%C3%A1sicos)s
5. [Estrutura de Configuração](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#5-estrutura-de-configura%C3%A7%C3%A3o)
6. [Sistema de Tags](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#6-sistema-de-tags)
7. [Tags Avançadas e Boas Práticas](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#7-tags-avan%C3%A7adas-e-boas-pr%C3%A1ticas)
8. [Exemplos de Documentação](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#8-exemplos-de-documenta%C3%A7%C3%A3o)
9. [Sistema de Grupos](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#9-sistema-de-grupos)
10. [Integração com CMake](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#10-integra%C3%A7%C3%A3o-com-cmake)
11. [Formatos de Saída](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#11-formatos-de-sa%C3%ADda)
12. [Troubleshooting](https://claude.ai/chat/c4399509-8088-4035-ac37-cf745d7903a7#12-troubleshooting)

---

## 1. Visão Geral

Doxygen é uma ferramenta de geração automática de documentação que analisa código-fonte e comentários estruturados para produzir documentação navegável em múltiplos formatos.

### Linguagens Suportadas

`C` `C++` `Java` `Python` `PHP` `C#` `Objective-C` `Fortran` `VHDL` `IDL`

### Características Principais

- Extração de documentação diretamente do código-fonte
- Geração automática de HTML, LaTeX, XML, RTF e Man pages
- Suporte a diagramas de classe e dependências via Graphviz
- Análise de estrutura de classes, herança e colaboração
- Integração nativa com CMake e outros sistemas de build

### Componentes Internos

| Componente | Função |
| --- | --- |
| `Parser` | Analisa a sintaxe do código-fonte |
| `Comment Processor` | Interpreta e valida as tags Doxygen |
| `Symbol Table` | Armazena todas as entidades do código |
| `Documentation Model` | Estrutura interna da documentação |
| `Output Generator` | Gera os formatos de saída configurados |

### Fluxo de Processamento

```
Código Fonte
    │
    ▼
Parser
    │
    ▼
Extrator de Comentários
    │
    ▼
Modelo Interno
    │
    ▼
Geradores de Output
    │
    ├── HTML
    ├── LaTeX
    ├── XML
    └── RTF
```

---

## 2. Pré-requisitos

Antes de instalar o Doxygen, verifique se os itens abaixo estão presentes no sistema.

### Software obrigatório

| Pacote | Versão mínima | Finalidade |
| --- | --- | --- |
| `doxygen` | 1.9+ | Ferramenta principal de geração |
| `gcc` ou `g++` | qualquer | Compilar projetos C/C++ documentados |
| `make` | qualquer | Executar builds e geração via Makefile |
| `cmake` | 3.14+ | Sistema de build utilizado com Qt Creator |

> **Sobre o CMake:** o Qt Creator utiliza CMake como sistema de build padrão para projetos C/C++. A integração do Doxygen ao CMake permite gerar a documentação diretamente pelo Qt Creator, sem precisar abrir um terminal separado.
> 

> **Dica:** Você pode instalar a extensão do Doxygen no seu editor para melhorar ou ajudar na estruturação da sintaxe dos comentários.
> 

### Software opcional (recomendado)

| Pacote | Finalidade |
| --- | --- |
| `graphviz` | Geração de diagramas de classe e dependência |
| `texlive` | Geração de PDF via LaTeX (`GENERATE_LATEX = YES`) |

### Verificar o que já está instalado

```bash
# Verificar cada dependência
doxygen --version
gcc --version
make --version
cmake --version
dot -V              # Graphviz (opcional)
```

### Permissões necessárias

A instalação de pacotes requer privilégios de superusuário (`sudo`). A geração de documentação em si não exige `sudo` — basta ter permissão de escrita no diretório de saída (`OUTPUT_DIRECTORY`).

---

## 3. Instalação

### Ubuntu / Debian

```bash
# Atualizar lista de pacotes
sudo apt update

# Instalação mínima
sudo apt install doxygen cmake

# Instalação completa (com diagramas)
sudo apt install doxygen cmake graphviz

# Instalação completa (com diagramas + saída PDF)
sudo apt install doxygen cmake graphviz texlive-full

# Verificar versão instalada
doxygen --version
cmake --version
```

> **Verificação pós-instalação:** Execute `doxygen --version`. A saída deve exibir a versão instalada, ex: `1.9.8`. Se o comando não for reconhecido, o pacote não foi instalado corretamente — tente repetir o comando de instalação.
> 

---

## 4. Comandos Básicos

### Gerar o Arquivo de Configuração

```bash
# Cria um Doxyfile com todos os parâmetros e valores padrão
doxygen -g

# Cria com nome customizado
doxygen -g MeuDoxyfile
```

### Executar a Geração de Documentação

```bash
# Gera documentação usando o Doxyfile do diretório atual
doxygen Doxyfile

# Especificando um arquivo de configuração diferente
doxygen /caminho/para/MeuDoxyfile
```

### Abrir a Documentação Gerada

```bash
# Abrir no navegador padrão (Linux)
xdg-open docs/doxygen/html/index.html
```

### Resumo dos Comandos

| Comando | Descrição |
| --- | --- |
| `doxygen -g` | Cria o Doxyfile padrão |
| `doxygen Doxyfile` | Gera a documentação |
| `doxygen --version` | Exibe a versão instalada |
| `doxygen -h` | Exibe ajuda |

---

## 5. Estrutura de Configuração

O arquivo `Doxyfile` contém todos os parâmetros de geração. Ele pode ficar em qualquer lugar do projeto — o que define como os caminhos são resolvidos é **de onde você executa o comando `doxygen`**.

### Onde o Doxyfile pode ficar

**Na raiz do projeto** — opção mais comum e simples. Os caminhos relativos funcionam direto, sem ajuste:

```markdown
meu-projeto/
├── Doxyfile          ← aqui
├── src/
├── include/
└── docs/ @brief Validates the license file presence and authenticity
 * @return Status enum indicating validation result
 *
 * Performs license validation by:
 * 1. Locating the SDK library directory
 * 2. Looking for license file (devguide.lic) in that directory
 * 3. Reading the license key from the file
 * 4. Computing SHA-256 hash of the key
 * 5. Comparing against expected hash (LICENSE_HASH)
 *
 * **Expected license file format:**
 * - Plain text file containing the license key
 * - Key is trimmed of whitespace
 * - Example content: "VMI-2026-DEVGUIDE"
 *
 * **Possible return values:**
 * - Status::Valid: License is valid
 * - Status::FileNotFound: License file missing or inaccessible
 * - Status::InvalidKey: File exists but contains invalid key
 *
 * @note Logs detailed debug information using Security category
 * @see libraryDir()
 * @see statusMessage()
```

```
# Doxyfile com caminhos relativos à raiz
INPUT            = src include
OUTPUT_DIRECTORY = docs/doxygen
```

```bash
# Executado na raiz — tudo funciona direto
doxygen Doxyfile
```

---

**Em um subdiretório** (ex: `docs/`) — funciona, mas os caminhos precisam compensar o nível a mais:

```
meu-projeto/
├── src/
├── include/
└── docs/
    └── Doxyfile      ← aqui
```

```
# Doxyfile precisa subir um nível para encontrar o código
INPUT            = ../src ../include
OUTPUT_DIRECTORY = .
```

```bash
# Executado de dentro de docs/
cd docs
doxygen Doxyfile
```

---

**Com caminhos absolutos** — funciona independente de onde o comando é executado:

```
INPUT            = /home/usuario/meu-projeto/src
OUTPUT_DIRECTORY = /home/usuario/meu-projeto/docs/doxygen
```

> **Recomendação:** deixe o Doxyfile na raiz do projeto. É a convenção adotada pela maioria dos projetos open source e evita confusão com caminhos relativos.
> 

---

### Doxyfile do Projeto VMIS

Este é o Doxyfile configurado com a identidade visual VMI Security:

```
PROJECT_NAME           = "InfinityXR"
PROJECT_LOGO           = ./img/logo-vmi-whiteyellow-1.svg
PROJECT_VERSION        = 1.0
PROJECT_BRIEF          = "Descrição resumida do projeto"

INPUT                  = src include
RECURSIVE              = YES

OUTPUT_DIRECTORY       = docs/doxygen

GENERATE_HTML          = YES
GENERATE_LATEX         = NO

EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = YES
EXTRACT_STATIC         = YES

# ── Identidade Visual VMAII Security ─────────────────────────────────
HTML_EXTRA_STYLESHEET  = vmi_custom.css
HTML_COLORSTYLE_HUE    = 35
HTML_COLORSTYLE_SAT    = 200
HTML_COLORSTYLE_GAMMA  = 80
GENERATE_TREEVIEW      = YES

# ── Diagramas (desabilitados) ─────────────────────────────────────────
HAVE_DOT               = NO
UML_LOOK               = NO
CALL_GRAPH             = NO
CALLER_GRAPH           = NO

CLASS_GRAPH            = NO
COLLABORATION_GRAPH    = NO
GROUP_GRAPHS           = NO
INCLUDE_GRAPH          = NO
INCLUDED_BY_GRAPH      = NO
DIRECTORY_GRAPH        = NO
```

> **Sobre o `vmi_custom.css`:** coloque o arquivo na mesma pasta do Doxyfile (raiz do projeto). Ele aplica as cores e tipografia da identidade VMAII — cinza escuro, dourado `#E8A020` e fonte sem serifa — ao HTML gerado.
> 

### Parâmetros Importantes

| Parâmetro | Função |
| --- | --- |
| `INPUT` | Diretórios analisados |
| `OUTPUT_DIRECTORY` | Diretório de saída |
| `RECURSIVE` | Leitura recursiva dos subdiretórios |
| `EXTRACT_ALL` | Documenta mesmo sem comentários |
| `EXTRACT_PRIVATE` | Inclui membros privados |
| `GENERATE_HTML` | Gera saída HTML |
| `HTML_EXTRA_STYLESHEET` | CSS customizado para identidade visual |
| `HAVE_DOT` | Ativa diagramas com Graphviz |
| `CALL_GRAPH` | Gera grafo de chamadas de funções |

> **Dica:** `EXTRACT_ALL = YES` é útil para explorar código legado sem comentários. Para projetos novos, prefira `EXTRACT_ALL = NO` para documentar apenas o que foi explicitamente anotado — isso força boas práticas.
> 

---

## 6. Sistema de Tags

Doxygen utiliza **tags semânticas** para estruturar a documentação.

### Tags Fundamentais

| Tag | Descrição |
| --- | --- |
| `@brief` | Descrição resumida (uma linha) |
| `@details` | Descrição detalhada |
| `@param` | Descrição de parâmetro de entrada |
| `@param[in]` | Parâmetro somente de entrada |
| `@param[out]` | Parâmetro somente de saída |
| `@param[in,out]` | Parâmetro de entrada e saída |
| `@return` | Valor retornado |
| `@note` | Observação adicional |
| `@warning` | Aviso importante |
| `@todo` | Tarefa pendente |

### Tags Estruturais

| Tag | Função |
| --- | --- |
| `@file` | Documentação de arquivo |
| `@class` | Documentação de classe |
| `@struct` | Documentação de struct |
| `@namespace` | Documentação de namespace |
| `@enum` | Documentação de enumeração |

---

## 7. Tags Avançadas e Boas Práticas

### Tags Avançadas

| Tag | Descrição |
| --- | --- |
| `@see` | Referência a elemento relacionado |
| `@since` | Versão em que foi introduzido |
| `@version` | Versão atual do elemento |
| `@author` | Autor do código |
| `@date` | Data de criação ou modificação |
| `@deprecated` | Marca elemento como obsoleto |
| `@throws` / `@exception` | Exceção que pode ser lançada |
| `@pre` | Pré-condição para uso correto |
| `@post` | Pós-condição garantida após execução |
| `@invariant` | Condição sempre verdadeira |
| `@relates` | Associa função a uma classe |
| `@overload` | Indica sobrecarga de função |
| `@code` / `@endcode` | Bloco de código inline na documentação |
| `@verbatim` / `@endverbatim` | Texto literal sem formatação |

### Exemplo com Tags Avançadas

```cpp
/**
 * @brief Divide dois números reais.
 *
 * @details
 * Executa a divisão de `a` por `b`. A função valida
 * previamente se o divisor é diferente de zero.
 *
 * @param[in] a  Dividendo.
 * @param[in] b  Divisor (deve ser diferente de zero).
 *
 * @return Resultado da divisão.
 *
 * @throws std::invalid_argument Se `b` for igual a zero.
 *
 * @pre  b != 0
 * @post O resultado é matematicamente correto para b != 0
 *
 * @see soma(), subtracao()
 * @since 1.2
 * @author João Silva
 *
 * @warning Não use esta função com valores de ponto flutuante
 *          muito próximos de zero sem verificação prévia.
 */
double divisao(double a, double b);
```

### Boas Práticas

**Use `@brief` sempre em uma única linha:**

```cpp
// ✅ Correto
/// @brief Calcula a média dos elementos do vetor.

// ❌ Evitar — @brief em múltiplas linhas quebra a visualização
/// @brief Calcula a média dos elementos
/// do vetor passado como parâmetro.
```

**Prefira `@param[in/out]` para deixar a intenção clara:**

```cpp
// ✅ Mais informativo
/// @param[in]  src   Buffer de origem (somente leitura)
/// @param[out] dest  Buffer de destino (será preenchido)

// ❌ Menos informativo
/// @param src   Buffer de origem
/// @param dest  Buffer de destino
```

**Use `@deprecated` com alternativa:**

```cpp
/**
 * @brief Soma dois inteiros (versão antiga).
 * @deprecated Use a função somaSegura() que valida overflow.
 */
int soma(int a, int b);
```

**Documente exceções com `@throws`:**

```cpp
/**
 * @throws std::out_of_range Se o índice for inválido.
 * @throws std::runtime_error Se o arquivo não puder ser lido.
 */
```

---

## 8. Exemplos de Documentação

### Documentação de Função

```cpp
/**
 * @brief Realiza a soma de dois inteiros.
 *
 * @details
 * Esta função executa uma operação aritmética simples e retorna
 * o resultado da soma dos dois operandos.
 *
 * @param[in] a  Operando esquerdo.
 * @param[in] b  Operando direito.
 *
 * @return Resultado da soma de a e b.
 *
 * @see subtracao(), multiplicacao()
 */
int soma(int a, int b);
```

### Documentação de Classe

```cpp
/**
 * @class Calculadora
 * @brief Implementa operações matemáticas básicas.
 *
 * @details
 * A classe Calculadora fornece métodos para operações
 * aritméticas simples sobre inteiros.
 *
 * @author Maria Oliveira
 * @since 1.0
 *
 * @code
 * Calculadora calc;
 * int resultado = calc.soma(3, 4); // resultado = 7
 * @endcode
 */
class Calculadora {
public:
    /**
     * @brief Soma dois valores inteiros.
     * @param[in] a  Primeiro operando.
     * @param[in] b  Segundo operando.
     * @return Soma de a e b.
     */
    int soma(int a, int b);

    /**
     * @brief Divide dois valores.
     * @param[in] a  Dividendo.
     * @param[in] b  Divisor.
     * @throws std::invalid_argument Se b for zero.
     * @return Resultado da divisão.
     */
    double divisao(double a, double b);
};
```

### Documentação de Arquivo

```cpp
/**
 * @file calculadora.h
 * @brief Declarações da classe Calculadora.
 * @author Maria Oliveira
 * @date 2025-01-15
 * @version 1.2
 */
```

### Documentação de Enum

```cpp
/**
 * @enum StatusOperacao
 * @brief Representa o resultado de uma operação.
 */
enum StatusOperacao {
    SUCESSO = 0,      ///< Operação concluída com sucesso.
    ERRO_DIVISAO = 1, ///< Tentativa de divisão por zero.
    ERRO_OVERFLOW = 2 ///< Resultado excede o limite do tipo.
};
```

---

## 9. Sistema de Grupos

Doxygen permite organizar entidades em **módulos lógicos** com `@defgroup` e `@ingroup`.

> **Atenção:** `@defgroup` deve aparecer em um comentário separado, normalmente em um arquivo dedicado (`.dox`), fora de funções ou classes. Isso mantém a definição dos grupos desacoplada do código-fonte.
> 

---

### Como funciona na prática

**Não é necessário criar nada dentro de cada pasta do projeto.** O processo é simples e tem apenas duas partes:

**1 — Criar os arquivos `.dox`** em um único lugar (`docs/groups/`), um por módulo. Eles só definem o nome e a descrição do grupo:

```
docs/
└── groups/
    ├── sdk.dox       ← define o grupo "SDK"
    ├── core.dox      ← define o grupo "Core"
    ├── plugins.dox   ← define o grupo "Plugins"
    └── app.dox       ← define o grupo "App"
```

**2 — Nos headers (`.h`) do projeto**, adicionar apenas uma linha indicando a qual grupo aquele arquivo pertence:

```cpp
/**
 * @file IPlugin.h
 * @ingroup sdk_contracts   ← só isso
 */
```

O Doxygen varre o código automaticamente. Os `.dox` ensinam o que existe, os headers dizem onde cada arquivo se encaixa.

```
docs/groups/sdk.dox  →  define que "sdk_contracts" existe
IPlugin.h            →  diz "@ingroup sdk_contracts"
Doxygen              →  lê os dois e monta a documentação agrupada
```

---

### Estrutura recomendada para projetos grandes

```
InfinityXR/
├── CMakeLists.txt
├── cmake/
│   └── Doxygen.cmake
│
├── docs/
│   ├── doxygen/                    ← saída gerada pelo Doxygen
│   │   └── html/
│   │       └── index.html
│   │
│   └── groups/                     ← definições dos grupos (.dox)
│       ├── sdk.dox
│       ├── core.dox
│       ├── plugins.dox
│       └── app.dox
│
├── src/
│   ├── sdk/
│   ├── libs/
│   ├── Plugins/
│   └── app/
│
└── tests/
```

> **Importante:** a pasta `docs/groups/` contém os arquivos `.dox` que você versiona. A pasta `docs/doxygen/` é gerada pelo Doxygen e **não deve ser versionada** — adicione-a ao `.gitignore`.
> 

---

### Conteúdo dos arquivos .dox

**`docs/groups/sdk.dox`**

```cpp
/**
 * @defgroup sdk SDK Público
 * @brief Contratos e tipos públicos disponíveis para desenvolvimento de plugins.
 *
 * @details
 * Este grupo contém todas as interfaces e tipos que formam o contrato
 * público do InfinityXR. Plugins devem depender apenas deste grupo,
 * nunca de `infinity_core` diretamente.
 */

/**
 * @defgroup sdk_contracts Contratos
 * @ingroup sdk
 * @brief Interfaces que definem os serviços e pontos de extensão do sistema.
 */

/**
 * @defgroup sdk_types Tipos
 * @ingroup sdk
 * @brief Tipos de dados utilizados nas interfaces do SDK.
 */
```

**`docs/groups/core.dox`**

```cpp
/**
 * @defgroup core Núcleo (infinity_core)
 * @brief Implementação interna do kernel, serviços e interface do sistema.
 */

/**
 * @defgroup core_kernel Kernel
 * @ingroup core
 * @brief Gerenciamento de plugins, extensões e ciclo de vida da aplicação.
 */

/**
 * @defgroup core_services Serviços
 * @ingroup core
 * @brief Implementações de serviços como HTTP, configurações e diálogos.
 */

/**
 * @defgroup core_messaging Mensageria
 * @ingroup core
 * @brief Sistema de eventos e comunicação entre componentes via EventBus.
 */

/**
 * @defgroup core_ui Interface
 * @ingroup core
 * @brief Modelos de menu, registro de views e gerenciamento de sessão.
 */
```

**`docs/groups/plugins.dox`**

```cpp
/**
 * @defgroup plugins Plugins
 * @brief Plugins carregados dinamicamente pelo kernel do InfinityXR.
 */

/**
 * @defgroup plugin_about Plugin About
 * @ingroup plugins
 * @brief Exibe informações sobre a aplicação e sua versão.
 */

/**
 * @defgroup plugin_auth Plugin Authentication
 * @ingroup plugins
 * @brief Gerencia autenticação de usuários e controle de sessão.
 */
```

**`docs/groups/app.dox`**

```cpp
/**
 * @defgroup app Aplicação
 * @brief Bootstrap, serviços de sistema e ponto de entrada do InfinityXR.
 */

/**
 * @defgroup app_bootstrap Bootstrap
 * @ingroup app
 * @brief Sequência de inicialização e instaladores de serviços do sistema.
 */

/**
 * @defgroup app_services Serviços da Aplicação
 * @ingroup app
 * @brief Serviços utilitários como ScreenHelper e SystemSignalHandler.
 */
```

---

### Como os headers referenciam os grupos

```cpp
// src/sdk/include/Infinity/sdk/contracts/IPlugin.h

/**
 * @file IPlugin.h
 * @ingroup sdk_contracts
 * @brief Interface base para todos os plugins do InfinityXR.
 */

/**
 * @class IPlugin
 * @ingroup sdk_contracts
 * @brief Define o contrato que todo plugin deve implementar.
 */
class IPlugin {
public:
    virtual ~IPlugin() = default;
    virtual void initialize(const PluginContext &context) = 0;
};
```

---

### Garantir que o CMake inclua os .dox na geração

```
doxygen_add_docs(documentation
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/docs/groups
    COMMENT "Gerando documentação do InfinityXR..."
)
```

---

### O que não versionar

```
# Saída gerada pelo Doxygen
docs/doxygen/
build/docs/
```

---

## 10. Integração com CMake

O CMake é um sistema de build — ele organiza como seu projeto é compilado. O Doxygen não tem nada a ver com compilação, mas é possível registrar a geração de documentação como uma **tarefa extra** dentro do CMake.

### Sem integração vs. com integração

**Sem integração** — dois comandos manuais e separados:

```bash
cmake --build .       # compila o projeto
doxygen Doxyfile      # gera a documentação (na mão)
```

**Com integração** — tudo pelo CMake:

```bash
cmake --build .              # compila o projeto
cmake --build . --target doc # gera a documentação
```

---

### Como configurar

```
find_package(Doxygen REQUIRED)

if(DOXYGEN_FOUND)
    set(DOXYGEN_IN  ${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile)
    set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/docs/doxygen)

    add_custom_target(doc
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_IN}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Gerando documentação com Doxygen..."
        VERBATIM
    )
else()
    message(WARNING "Doxygen não encontrado — documentação não será gerada.")
endif()
```

| Linha | Descrição |
| --- | --- |
| `find_package(Doxygen)` | Verifica se o Doxygen está instalado |
| `DOXYGEN_IN` | Caminho do Doxyfile (na raiz do projeto) |
| `DOXYGEN_OUT` | Onde a documentação será gerada |
| `add_custom_target(doc ...)` | Cria o alvo `doc` chamável pelo CMake |
| `WORKING_DIRECTORY` | Define de onde o Doxygen é executado |
| `VERBATIM` | Garante que os argumentos não sejam alterados |

---

### Como usar

```bash
# 1. Configure o projeto (apenas na primeira vez)
cmake -B build

# 2. Compile normalmente
cmake --build build

# 3. Gere a documentação
cmake --build build --target doc
```

A documentação será gerada em `docs/doxygen/html/index.html`.

---

## 11. Formatos de Saída

| Formato | Uso |
| --- | --- |
| `HTML` | Documentação web navegável |
| `LaTeX` | Geração de PDF |
| `RTF` | Documentos rich text (Word) |
| `XML` | Integração com outras ferramentas |
| `Man pages` | Documentação Unix |

### Estrutura de Saída

```
docs/
└── doxygen/
    └── html/
        ├── index.html
        ├── classes.html
        └── files.html
```

---

## 12. Troubleshooting

### Documentação não é gerada para alguns arquivos

**Sintoma:** Arquivos `.cpp` ou `.h` não aparecem na documentação.

```
# Verifique se o caminho está correto no Doxyfile
INPUT = src include   # certifique-se de que esses diretórios existem

# Ative leitura recursiva
RECURSIVE = YES

# Inclua as extensões necessárias
FILE_PATTERNS = *.cpp *.h *.hpp *.c
```

---

### Diagramas não aparecem no HTML

**Sintoma:** A documentação HTML é gerada, mas sem diagramas de classe ou dependência.

1. Verifique se o Graphviz está instalado: `dot -V`
2. Confirme as configurações no Doxyfile:

```
HAVE_DOT    = YES
DOT_PATH    = /usr/bin
```

---

### `EXTRACT_ALL = NO` e funções sem comentários somem

**Sintoma:** Funções sem bloco `/** */` não aparecem na documentação.

**Explicação:** Este é o comportamento esperado com `EXTRACT_ALL = NO`.

**Solução:** Use `EXTRACT_ALL = YES` para incluir tudo, ou adicione comentários nas funções que deseja documentar.

---

### Warning: "documented symbol X not found"

**Sintoma:** Doxygen exibe avisos sobre símbolos não encontrados.

```cpp
// ❌ Problema: parâmetro no código é 'valor', não 'v'
/// @param v  O valor de entrada.
void processa(int valor);

// ✅ Correto
/// @param valor  O valor de entrada.
void processa(int valor);
```

---

### Caracteres especiais quebram a documentação HTML

**Sintoma:** Símbolos como `<`, `>`, `&` aparecem incorretamente no HTML gerado.

| Caractere | Usar |
| --- | --- |
| `<` | `\<` ou `&lt;` |
| `>` | `\>` ou `&gt;` |
| `&` | `\&` ou `&amp;` |
| `@` literal | `\@` |

---

### Documentação gerada está desatualizada

**Sintoma:** Mudanças no código não refletem na documentação.

**Solução:** O Doxygen não tem cache inteligente. Como o projeto possui pastas próprias dentro de `docs/`, apague apenas a subpasta gerada pelo Doxygen para não afetar outros arquivos:

```bash
rm -rf docs/doxygen/
doxygen Doxyfile
```

> **Por que não `rm -rf docs/`?** O projeto mantém arquivos versionados em `docs/groups/` com as definições dos grupos `.dox`. Apagar `docs/` inteiro removeria esses arquivos. Sempre apague apenas `docs/doxygen/`, que é a saída gerada.
> 

---

*Documentação gerada com base na versão 1.9+ do Doxygen. Autor: Júlio Oliveira.*

> Geração Automática de Documentação de Código | Versão 1.0 | Linux
> 
> 
> **Autor:** Júlio Oliveira
> 

---

## Sumário

1. [Visão Geral](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
2. [Pré-requisitos](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
3. [Instalação](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
4. [Comandos Básicos](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
5. [Estrutura de Configuração](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
6. [Sistema de Tags](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
7. [Tags Avançadas e Boas Práticas](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
8. [Exemplos de Documentação](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
9. [Sistema de Grupos](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
10. [Integração com CMake](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
11. [Formatos de Saída](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)
12. [Troubleshooting](https://www.notion.so/Doxygen-Documenta-o-T-cnica-322fd350abae80b093b1c4d53c2e33b1?pvs=21)

---

## 1. Visão Geral

Doxygen é uma ferramenta de geração automática de documentação que analisa código-fonte e comentários estruturados para produzir documentação navegável em múltiplos formatos.

### Linguagens Suportadas

`C` `C++` `Java` `Python` `PHP` `C#` `Objective-C` `Fortran` `VHDL` `IDL`

### Características Principais

- Extração de documentação diretamente do código-fonte
- Geração automática de HTML, LaTeX, XML, RTF e Man pages
- Suporte a diagramas de classe e dependências via Graphviz
- Análise de estrutura de classes, herança e colaboração
- Integração n.ativa com CMake e outros sistemas de build

### Componentes Internos

| Componente | Função |
| --- | --- |
| `Parser` | Analisa a sintaxe do código-fonte |
| `Comment Processor` | Interpreta e valida as tags Doxygen |
| `Symbol Table` | Armazena todas as entidades do código |
| `Documentation Model` | Estrutura interna da documentação |
| `Output Generator` | Gera os formatos de saída configurados |

### Fluxo de Processamento

```
Código Fonte
    │
    ▼
Parser
    │
    ▼
Extrator de Comentários
    │
    ▼
Modelo Interno
    │
    ▼
Geradores de Output
    │
    ├── HTML
    ├── LaTeX
    ├── XML
    └── RTF
```

---

## 2. Pré-requisitos

Antes de instalar o Doxygen, verifique se os itens abaixo estão presentes no sistema.

### Software obrigatório

| Pacote | Versão mínima | Finalidade |
| --- | --- | --- |
| `doxygen` | 1.9+ | Ferramenta principal de geração |
| `gcc` ou `g++` | qualquer | Compilar projetos C/C++ documentados |
| `make` | qualquer | Executar builds e geração via Makefile |
| `cmake` | 3.14+ | Sistema de build utilizado com Qt Creator |

> **Sobre o CMake:** o Qt Creator utiliza CMake como sistema de build padrão para projetos C/C++. A integração do Doxygen ao CMake permite gerar a documentação diretamente pelo Qt Creator, sem precisar abrir um terminal separado.
> 

Observação: Você pode instalar a extensão do Doxygen, para melhorar ou ajudar na estruturação da sintaxe da estrutura do doxygen 

### Software opcional (recomendado)

| Pacote | Finalidade |
| --- | --- |
| `graphviz` | Geração de diagramas de classe e dependência |
| `texlive` | Geração de PDF via LaTeX (saída `GENERATE_LATEX = YES`) |

### Verificar o que já está instalado

```bash
# Verificar cada dependência
doxygen --version
gcc --version
make --version
cmake --version
dot -V              # Graphviz (opcional)
```

### Permissões necessárias

A instalação de pacotes requer privilégios de superusuário (`sudo`). A geração de documentação em si não exige `sudo` — basta ter permissão de escrita no diretório de saída (`OUTPUT_DIRECTORY`).

---

## 3. Instalação

### Ubuntu / Debian

```bash
# Atualizar lista de pacotes
sudo apt update

# Instalação mínima
sudo apt install doxygen cmake

# Instalação completa (com diagramas)
sudo apt install doxygen cmake graphviz

# Instalação completa (com diagramas + saída PDF)
sudo apt install doxygen cmake graphviz texlive-full

# Verificar versão instalada
doxygen --version
cmake --version
```

> **Verificação pós-instalação:** Execute `doxygen --version`. A saída deve exibir a versão instalada, ex: `1.9.8`. Se o comando não for reconhecido, o pacote não foi instalado corretamente — tente repetir o comando de instalação.
> 

---

## 4. Comandos Básicos

### Gerar o Arquivo de Configuração

```bash
# Cria um Doxyfile com todos os parâmetros e valores padrão
doxygen -g

# Cria com nome customizado
doxygen -g MeuDoxyfile
```

### Executar a Geração de Documentação

```bash
# Gera documentação usando o Doxyfile do diretório atual
doxygen Doxyfile

# Especificando um arquivo de configuração diferente
doxygen /caminho/para/MeuDoxyfile
```

### Abrir a Documentação Gerada

```bash
# Abrir no navegador padrão (Linux)
xdg-open docs/html/index.html
```

### Resumo dos Comandos

| Comando | Descrição |
| --- | --- |
| `doxygen -g` | Cria o Doxyfile padrão |
| `doxygen Doxyfile` | Gera a documentação |
| `doxygen --version` | Exibe a versão instalada |
| `doxygen -h` | Exibe ajuda |

---

## 5. Estrutura de Configuração

O arquivo `Doxyfile` contém todos os parâmetros de geração. Ele pode ficar em qualquer lugar do projeto — o que define como os caminhos são resolvidos é **de onde você executa o comando `doxygen`**.

### Onde o Doxyfile pode ficar

**Na raiz do projeto** — opção mais comum e simples. Os caminhos relativos funcionam direto, sem ajuste:

```
meu-projeto/
├── Doxyfile          ← aqui
├── src/
├── include/
└── docs/
```

```
# Doxyfile com caminhos relativos à raiz
INPUT            = src include
OUTPUT_DIRECTORY = docs
```

```bash
# Executado na raiz — tudo funciona direto
doxygen Doxyfile
```

---

**Em um subdiretório** (ex: `docs/`) — funciona, mas os caminhos precisam compensar o nível a mais:

```
meu-projeto/
├── src/
├── include/
└── docs/
    └── Doxyfile      ← aqui
```

```
# Doxyfile precisa subir um nível para encontrar o código
INPUT            = ../src ../include
OUTPUT_DIRECTORY = .
```

```bash
# Executado de dentro de docs/
cd docs
doxygen Doxyfile
```

---

**Com caminhos absolutos** — funciona independente de onde o comando é executado:

```
INPUT            = /home/usuario/meu-projeto/src
OUTPUT_DIRECTORY = /home/usuario/meu-projeto/docs
```

> **Recomendação:** deixe o Doxyfile na raiz do projeto. É a convenção adotada pela maioria dos projetos open source e evita confusão com caminhos relativos.
> 

---

### Exemplo Completo de Doxyfile

```
PROJECT_NAME           = "Projeto Exemplo"
PROJECT_VERSION        = 1.0
PROJECT_BRIEF          = "Descrição resumida do projeto"

INPUT                  = src include
RECURSIVE              = YES

OUTPUT_DIRECTORY       = docs

GENERATE_HTML          = YES
GENERATE_LATEX         = NO

EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = YES
EXTRACT_STATIC         = YES

# Ativar diagramas com Graphviz
HAVE_DOT               = YES
UML_LOOK               = YES
CALL_GRAPH             = YES
CALLER_GRAPH           = YES
```

### Parâmetros Importantes

| Parâmetro | Função |
| --- | --- |
| `INPUT` | Diretórios analisados |
| `OUTPUT_DIRECTORY` | Diretório de saída |
| `RECURSIVE` | Leitura recursiva dos subdiretórios |
| `EXTRACT_ALL` | Documenta mesmo sem comentários |
| `EXTRACT_PRIVATE` | Inclui membros privados |
| `GENERATE_HTML` | Gera saída HTML |
| `HAVE_DOT` | Ativa diagramas com Graphviz |
| `CALL_GRAPH` | Gera grafo de chamadas de funções |

> **Dica:** `EXTRACT_ALL = YES` é útil para explorar código legado sem comentários. Para projetos novos, prefira `EXTRACT_ALL = NO` para documentar apenas o que foi explicitamente anotado — isso força boas práticas.
> 

---

## 6. Sistema de Tags

Doxygen utiliza **tags semânticas** para estruturar a documentação.

### Tags Fundamentais

| Tag | Descrição |
| --- | --- |
| `@brief` | Descrição resumida (uma linha) |
| `@details` | Descrição detalhada |
| `@param` | Descrição de parâmetro de entrada |
| `@param[in]` | Parâmetro somente de entrada |
| `@param[out]` | Parâmetro somente de saída |
| `@param[in,out]` | Parâmetro de entrada e saída |
| `@return` | Valor retornado |
| `@note` | Observação adicional |
| `@warning` | Aviso importante |
| `@todo` | Tarefa pendente |

### Tags Estruturais

| Tag | Função |
| --- | --- |
| `@file` | Documentação de arquivo |
| `@class` | Documentação de classe |
| `@struct` | Documentação de struct |
| `@namespace` | Documentação de namespace |
| `@enum` | Documentação de enumeração |

---

## Tags Avançadas e Boas Práticas

### Tags Avançadas

| Tag | Descrição |
| --- | --- |
| `@see` | Referência a elemento relacionado |
| `@since` | Versão em que foi introduzido |
| `@version` | Versão atual do elemento |
| `@author` | Autor do código |
| `@date` | Data de criação ou modificação |
| `@deprecated` | Marca elemento como obsoleto |
| `@throws` / `@exception` | Exceção que pode ser lançada |
| `@pre` | Pré-condição para uso correto |
| `@post` | Pós-condição garantida após execução |
| `@invariant` | Condição sempre verdadeira |
| `@relates` | Associa função a uma classe |
| `@overload` | Indica sobrecarga de função |
| `@code` / `@endcode` | Bloco de código inline na documentação |
| `@verbatim` / `@endverbatim` | Texto literal sem formatação |

### Exemplo com Tags Avançadas

```cpp
/**
 * @brief Divide dois números reais.
 *
 * @details
 * Executa a divisão de `a` por `b`. A função valida
 * previamente se o divisor é diferente de zero.
 *
 * @param[in] a  Dividendo.
 * @param[in] b  Divisor (deve ser diferente de zero).
 *
 * @return Resultado da divisão.
 *
 * @throws std::invalid_argument Se `b` for igual a zero.
 *
 * @pre  b != 0
 * @post O resultado é matematicamente correto para b != 0
 *
 * @see soma(), subtracao()
 * @since 1.2
 * @author João Silva
 *
 * @warning Não use esta função com valores de ponto flutuante
 *          muito próximos de zero sem verificação prévia.
 */
double divisao(double a, double b);
```

### Boas Práticas

**Use `@brief` sempre em uma única linha:**

```cpp
// ✅ Correto
/// @brief Calcula a média dos elementos do vetor.

// ❌ Evitar — @brief em múltiplas linhas quebra a visualização
/// @brief Calcula a média dos elementos
/// do vetor passado como parâmetro.
```

**Prefira `@param[in/out]` para deixar a intenção clara:**

```cpp
// ✅ Mais informativo
/// @param[in]  src   Buffer de origem (somente leitura)
/// @param[out] dest  Buffer de destino (será preenchido)

// ❌ Menos informativo
/// @param src   Buffer de origem
/// @param dest  Buffer de destino
```

**Use `@deprecated` com alternativa:**

```cpp
/**
 * @brief Soma dois inteiros (versão antiga).
 * @deprecated Use a função somaSegura() que valida overflow.
 */
int soma(int a, int b);
```

**Documente exceções com `@throws`:**

```cpp
/**
 * @throws std::out_of_range Se o índice for inválido.
 * @throws std::runtime_error Se o arquivo não puder ser lido.
 */
```

---

## Exemplos de Documentação

### Documentação de Função

```cpp
/**
 * @brief Realiza a soma de dois inteiros.
 *
 * @details
 * Esta função executa uma operação aritmética simples e retorna
 * o resultado da soma dos dois operandos.
 *
 * @param[in] a  Operando esquerdo.
 * @param[in] b  Operando direito.
 *
 * @return Resultado da soma de a e b.
 *
 * @see subtracao(), multiplicacao()
 */
int soma(int a, int b);
```

### Documentação de Classe

```cpp
/**
 * @class Calculadora
 * @brief Implementa operações matemáticas básicas.
 *
 * @details
 * A classe Calculadora fornece métodos para operações
 * aritméticas simples sobre inteiros.
 *
 * @author Maria Oliveira
 * @since 1.0
 *
 * @code
 * Calculadora calc;
 * int resultado = calc.soma(3, 4); // resultado = 7
 * @endcode
 */
class Calculadora {
public:
    /**
     * @brief Soma dois valores inteiros.
     * @param[in] a  Primeiro operando.
     * @param[in] b  Segundo operando.
     * @return Soma de a e b.
     */
    int soma(int a, int b);

    /**
     * @brief Divide dois valores.
     * @param[in] a  Dividendo.
     * @param[in] b  Divisor.
     * @throws std::invalid_argument Se b for zero.
     * @return Resultado da divisão.
     */
    double divisao(double a, double b);
};
```

### Documentação de Arquivo

```cpp
/**
 * @file calculadora.h
 * @brief Declarações da classe Calculadora.
 * @author Maria Oliveira
 * @date 2025-01-15
 * @version 1.2
 */
```

### Documentação de Enum

```cpp
/**
 * @enum StatusOperacao
 * @brief Representa o resultado de uma operação.
 */
enum StatusOperacao {
    SUCESSO = 0,      ///< Operação concluída com sucesso.
    ERRO_DIVISAO = 1, ///< Tentativa de divisão por zero.
    ERRO_OVERFLOW = 2 ///< Resultado excede o limite do tipo.
};
```

---

## Sistema de Grupos

Doxygen permite organizar entidades em **módulos lógicos** com `@defgroup` e `@ingroup`.

> **Atenção:** `@defgroup` deve aparecer em um comentário separado, normalmente em um arquivo dedicado (`.dox`), fora de funções ou classes. Isso mantém a definição dos grupos desacoplada do código-fonte.
> 

---

### Como funciona na prática

**Não é necessário criar nada dentro de cada pasta do projeto.** O processo é simples e tem apenas duas partes:

**1 — Criar os arquivos `.dox`** em um único lugar (`docs/groups/`), um por módulo. Eles só definem o nome e a descrição do grupo: 

```
docs/
└── groups/
    ├── sdk.dox       ← define o grupo "SDK"
    ├── core.dox      ← define o grupo "Core"
    ├── plugins.dox   ← define o grupo "Plugins"
    └── app.dox       ← define o grupo "App"
```

**2 — Nos headers (`.h`) do projeto**, adicionar apenas uma linha indicando a qual grupo aquele arquivo pertence:

```cpp
/**
 * @file IPlugin.h
 * @ingroup sdk_contracts   ← só isso
 */
```

O Doxygen varre o código automaticamente. Os `.dox` ensinam o que existe, os headers dizem onde cada arquivo se encaixa.

```
docs/groups/sdk.dox  →  define que "sdk_contracts" existe
IPlugin.h            →  diz "@ingroup sdk_contracts"
Doxygen              →  lê os dois e monta a documentação agrupada
```

---

### Estrutura recomendada para projetos grandes

Em projetos com múltiplos módulos, cada grupo recebe seu próprio arquivo `.dox` dentro de `docs/groups/`. Abaixo está a estrutura baseada em um projeto real com arquitetura de plugins:

```
InfinityXR/
├── CMakeLists.txt
├── cmake/
│   └── Doxygen.cmake
│
├── docs/
│   ├── doxygen-awesome/            ← tema visual (CSS/JS)
│   │   ├── doxygen-awesome.css
│   │   ├── doxygen-awesome-sidebar-only.css
│   │   └── doxygen-awesome-darkmode-toggle.js
│   │
│   └── groups/                     ← definições dos grupos (.dox)
│       ├── sdk.dox                 ← contratos públicos e tipos do SDK
│       ├── core.dox                ← kernel, services, messaging, ui
│       ├── plugins.dox             ← sistema de plugins
│       └── app.dox                 ← bootstrap e entrada da aplicação
│
├── src/
│   ├── sdk/
│   │   └── include/Infinity/sdk/
│   │       ├── contracts/          ← IPlugin, IAuthService, IEventBus...
│   │       └── types/              ← ActionDescriptor, CommandId...
│   │
│   ├── libs/
│   │   └── infinity_core/
│   │       ├── include/Infinity/core/
│   │       │   ├── interaction/
│   │       │   ├── kernel/
│   │       │   ├── messaging/
│   │       │   ├── services/
│   │       │   └── ui/
│   │       └── src/
│   │
│   ├── Plugins/
│   │   ├── About/
│   │   └── Authentication/
│   │
│   └── app/
│       ├── bootstrap/
│       ├── services/
│       ├── modules/
│       └── views/
│
└── tests/
```

---

### Conteúdo dos arquivos .dox

Cada arquivo `.dox` define um grupo e sua descrição. Os headers do projeto então usam `@ingroup` para se associar ao grupo correto.

**`docs/groups/sdk.dox`** — contratos públicos e tipos expostos para plugins:

```cpp
/**
 * @defgroup sdk SDK Público
 * @brief Contratos e tipos públicos disponíveis para desenvolvimento de plugins.
 *
 * @details
 * Este grupo contém todas as interfaces e tipos que formam o contrato
 * público do InfinityXR. Plugins devem depender apenas deste grupo,
 * nunca de `infinity_core` diretamente.
 *
 * Subgrupos:
 * - @ref sdk_contracts — interfaces de serviços e extensões
 * - @ref sdk_types     — tipos de dados compartilhados
 */

/**
 * @defgroup sdk_contracts Contratos
 * @ingroup sdk
 * @brief Interfaces que definem os serviços e pontos de extensão do sistema.
 */

/**
 * @defgroup sdk_types Tipos
 * @ingroup sdk
 * @brief Tipos de dados utilizados nas interfaces do SDK.
 */
```

---

**`docs/groups/core.dox`** — implementação interna do núcleo da aplicação:

```cpp
/**
 * @defgroup core Núcleo (infinity_core)
 * @brief Implementação interna do kernel, serviços e interface do sistema.
 *
 * @details
 * Biblioteca interna do InfinityXR. Não deve ser acessada diretamente
 * por plugins — use os contratos do @ref sdk.
 */

/**
 * @defgroup core_kernel Kernel
 * @ingroup core
 * @brief Gerenciamento de plugins, extensões e ciclo de vida da aplicação.
 */

/**
 * @defgroup core_services Serviços
 * @ingroup core
 * @brief Implementações de serviços como HTTP, configurações e diálogos.
 */

/**
 * @defgroup core_messaging Mensageria
 * @ingroup core
 * @brief Sistema de eventos e comunicação entre componentes via EventBus.
 */

/**
 * @defgroup core_ui Interface
 * @ingroup core
 * @brief Modelos de menu, registro de views e gerenciamento de sessão.
 */
```

---

**`docs/groups/plugins.dox`** — plugins carregados dinamicamente:

```cpp
/**
 * @defgroup plugins Plugins
 * @brief Plugins carregados dinamicamente pelo kernel do InfinityXR.
 *
 * @details
 * Cada plugin implementa @ref IPlugin e pode contribuir com comandos,
 * views e preferências através das interfaces do @ref sdk.
 */

/**
 * @defgroup plugin_about Plugin About
 * @ingroup plugins
 * @brief Exibe informações sobre a aplicação e sua versão.
 */

/**
 * @defgroup plugin_auth Plugin Authentication
 * @ingroup plugins
 * @brief Gerencia autenticação de usuários e controle de sessão.
 */
```

---

**`docs/groups/app.dox`** — ponto de entrada e bootstrap da aplicação:

```cpp
/**
 * @defgroup app Aplicação
 * @brief Bootstrap, serviços de sistema e ponto de entrada do InfinityXR.
 *
 * @details
 * Responsável por inicializar o kernel, registrar os instaladores
 * de serviços e subir a interface principal da aplicação.
 */

/**
 * @defgroup app_bootstrap Bootstrap
 * @ingroup app
 * @brief Sequência de inicialização e instaladores de serviços do sistema.
 */

/**
 * @defgroup app_services Serviços da Aplicação
 * @ingroup app
 * @brief Serviços utilitários como ScreenHelper e SystemSignalHandler.
 */
```

---

### Como os headers referenciam os grupos

Após definir os grupos nos `.dox`, os headers do projeto usam `@ingroup` para se associar:

```cpp
// src/sdk/include/Infinity/sdk/contracts/IPlugin.h

/**
 * @file IPlugin.h
 * @ingroup sdk_contracts
 * @brief Interface base para todos os plugins do InfinityXR.
 */

/**
 * @class IPlugin
 * @ingroup sdk_contracts
 * @brief Define o contrato que todo plugin deve implementar.
 */
class IPlugin {
public:
    virtual ~IPlugin() = default;

    /**
     * @brief Inicializa o plugin com o contexto da aplicação.
     * @param[in] context  Contexto de inicialização fornecido pelo kernel.
     */
    virtual void initialize(const PluginContext &context) = 0;
};
```

```cpp
// src/libs/infinity_core/include/Infinity/core/kernel/pluginmanager.h

/**
 * @file pluginmanager.h
 * @ingroup core_kernel
 * @brief Gerenciador central do ciclo de vida dos plugins.
 */

/**
 * @class PluginManager
 * @ingroup core_kernel
 * @brief Carrega, inicializa e descarrega plugins em tempo de execução.
 */
class PluginManager { ... };
```

---

### Garantir que o CMake inclua os .dox na geração

No `cmake/Doxygen.cmake`, adicione o diretório `docs/groups/` como fonte para o Doxygen processar os arquivos `.dox`:

```
# Inclui tanto o código-fonte quanto os arquivos .dox dos grupos
doxygen_add_docs(documentation
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/docs/groups
    COMMENT "Gerando documentação do InfinityXR..."
)
```

---

### O que não versionar

Adicione ao `.gitignore`:

```
# Saída gerada pelo Doxygen
docs/html/
docs/latex/
build/docs/
```

---

## Integração com CMake

O CMake é um sistema de build — ele organiza como seu projeto é compilado. O Doxygen não tem nada a ver com compilação, mas é possível registrar a geração de documentação como uma **tarefa extra** dentro do CMake.

Isso significa que, em vez de precisar lembrar de rodar `doxygen Doxyfile` separadamente, você ensina o CMake a fazer isso por você sob o comando `--target doc`.

### Sem integração vs. com integração

**Sem integração** — dois comandos manuais e separados:

```bash
cmake --build .       # compila o projeto
doxygen Doxyfile      # gera a documentação (na mão)
```

**Com integração** — tudo pelo CMake:

```bash
cmake --build .              # compila o projeto
cmake --build . --target doc # gera a documentação
```

O CMake simplesmente **chama o Doxygen por baixo dos panos** — não muda nada no funcionamento do Doxygen em si.

---

### Como configurar

Adicione o bloco abaixo no seu `CMakeLists.txt`:

```
find_package(Doxygen REQUIRED)

if(DOXYGEN_FOUND)
    set(DOXYGEN_IN  ${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile)
    set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/docs)

    add_custom_target(doc
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_IN}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Gerando documentação com Doxygen..."
        VERBATIM
    )
else()
    message(WARNING "Doxygen não encontrado — documentação não será gerada.")
endif()
```

O que cada parte faz:

| Linha | Descrição |
| --- | --- |
| `find_package(Doxygen)` | Verifica se o Doxygen está instalado no sistema |
| `DOXYGEN_IN` | Caminho do Doxyfile (na raiz do projeto) |
| `DOXYGEN_OUT` | Onde a documentação será gerada |
| `add_custom_target(doc ...)` | Cria o alvo `doc` que pode ser chamado pelo CMake |
| `WORKING_DIRECTORY` | Define de onde o Doxygen é executado (importante para caminhos relativos) |
| `VERBATIM` | Garante que os argumentos não sejam alterados pelo CMake |

---

### Como usar

```bash
# 1. Configure o projeto (apenas na primeira vez)
cmake -B build

# 2. Compile normalmente
cmake --build build

# 3. Gere a documentação
cmake --build build --target doc
```

A documentação será gerada em `build/docs/html/index.html`.

---

### Quando vale usar essa integração?

Vale quando o projeto é grande e você quer automatizar tudo em um único pipeline — compilar, testar e gerar documentação com comandos padronizados. Em projetos pequenos ou pessoais, rodar `doxygen Doxyfile` diretamente é mais simples e suficiente.

---

## Formatos de Saída

| Formato | Uso |
| --- | --- |
| `HTML` | Documentação web navegável |
| `LaTeX` | Geração de PDF |
| `RTF` | Documentos rich text (Word) |
| `XML` | Integração com outras ferramentas |
| `Man pages` | Documentação Unix |

### Estrutura de Saída

```
docs/
├── html/
│   ├── index.html
│   ├── classes.html
│   └── files.html
└── latex/
    ├── refman.tex
    └── Makefile
```

---

## Troubleshooting

### Documentação não é gerada para alguns arquivos

**Sintoma:** Arquivos `.cpp` ou `.h` não aparecem na documentação.

**Causas e soluções:**

```
# Verifique se o caminho está correto no Doxyfile
INPUT = src include   # certifique-se de que esses diretórios existem

# Ative leitura recursiva
RECURSIVE = YES

# Inclua as extensões necessárias
FILE_PATTERNS = *.cpp *.h *.hpp *.c
```

---

### Diagramas não aparecem no HTML

**Sintoma:** A documentação HTML é gerada, mas sem diagramas de classe ou dependência.

**Causas e soluções:**

1. Verifique se o Graphviz está instalado: `dot -V`
2. Confirme as configurações no Doxyfile:

```
HAVE_DOT    = YES
DOT_PATH    = /usr/bin   # caminho padrão do executável 'dot' no Linux
```

---

### `EXTRACT_ALL = NO` e funções sem comentários somem

**Sintoma:** Funções sem bloco `/** */` não aparecem na documentação.

**Explicação:** Este é o comportamento esperado com `EXTRACT_ALL = NO`.

**Solução:** Use `EXTRACT_ALL = YES` para incluir tudo, ou adicione comentários nas funções que deseja documentar. Para projetos novos, `EXTRACT_ALL = NO` é recomendado pois força a prática de documentar.

---

### Warning: "documented symbol X not found"

**Sintoma:** Doxygen exibe avisos sobre símbolos não encontrados.

**Causas comuns:**

- Nome de parâmetro no `@param` diferente do código:

```cpp
// ❌ Problema: parâmetro no código é 'valor', não 'v'
/// @param v  O valor de entrada.
void processa(int valor);

// ✅ Correto
/// @param valor  O valor de entrada.
void processa(int valor);
```

---

### Caracteres especiais quebram a documentação HTML

**Sintoma:** Símbolos como `<`, `>`, `&` aparecem incorretamente no HTML gerado.

**Solução:** Use as entidades HTML equivalentes dentro dos comentários:

| Caractere | Usar |
| --- | --- |
| `<` | `\<` ou `&lt;` |
| `>` | `\>` ou `&gt;` |
| `&` | `\&` ou `&amp;` |
| `@` literal | `\@` |

---

### Documentação gerada está desatualizada

**Sintoma:** Mudanças no código não refletem na documentação.

**Solução:** O Doxygen não tem cache inteligente. Sempre apague o diretório de saída antes de regenerar:

```bash
rm -rf docs/
doxygen Doxyfile
```

---

*Documentação gerada com base na versão 1.9+ do Doxygen. Autor: Júlio Oliveira.*