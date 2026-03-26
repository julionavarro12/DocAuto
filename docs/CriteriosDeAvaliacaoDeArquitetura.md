# Critérios de Avaliação de Arquitetura

Este documento define os critérios formais para avaliação arquitetural do sistema **Spectrum 3 (v2)**.  
Seu objetivo é garantir consistência técnica, sustentabilidade, extensibilidade e alta performance ao longo do ciclo de vida do software.  

Ele deve ser utilizado em:  

* Code reviews  
* Auditorias técnicas  
* Avaliações de releases  
* Análise de novos módulos/plugins  

---  

## Modelo de Avaliação

### Escala de Pontuação

Cada item deve ser avaliado com base na seguinte escala:

| Pontuação | Nível       | Descrição                                             |
| --------- | ----------- | ----------------------------------------------------- |
| 0         | Inexistente | Não implementado ou completamente inadequado          |
| 1         | Fraco       | Implementação deficiente, riscos evidentes            |
| 2         | Aceitável   | Funciona, mas com limitações ou inconsistências       |
| 3         | Bom         | Implementação sólida com pequenas melhorias possíveis |
| 4         | Excelente   | Implementação robusta, consistente e bem aplicada     |

---

### Criticidade

Cada item possui um nível de impacto:

* **Crítico** → Pode comprometer estabilidade, segurança ou evolução do sistema  
* **Alto** → Impacta fortemente manutenção e escalabilidade  
* **Médio** → Impacta organização e clareza  
* **Baixo** → Refinamentos e boas práticas  

---  

## 1. Arquitetura e Design do Sistema  

**Criticidade predominante: Crítico / Alto**  

### Avaliar:  

* Adoção de padrão arquitetural consistente  
* Separação entre:  
  * Domínio  
  * Infraestrutura  
  * Interface (UI)  
* Isolamento entre lógica de negócio e UI  
* Definição clara de responsabilidades  
* Uso de contratos (interfaces puras)  
* Presença de pontos de extensão (plugins, módulos)  

### Métricas / Evidências:  

* Existência de dependências cíclicas (inaceitável)  
* Número de camadas violadas  
* Interfaces desacopladas de implementações  
* Facilidade de substituição de módulos  

---  

## 2. Estrutura do Projeto e Organização de Código  

**Criticidade predominante: Alto**  

### Avaliar:  

* Organização clara de diretórios  
* Separação entre:  
  * core  
  * módulos  
  * plugins  
  * UI  
* Isolamento entre bibliotecas e aplicações  
* Consistência estrutural entre módulos  
* Separação entre interface e implementação  

### Métricas / Evidências:  

* Navegação intuitiva no código  
* Ausência de dependências cruzadas indevidas  
* Tempo médio para localizar um componente  
* Padronização de naming e layout  

---  

## 3. Sistema de Build (CMake)  

**Criticidade predominante: Alto**  

### Avaliar:  

* Uso de CMake moderno (targets)  
* Isolamento de dependências  
* Modularização do build  
* Uso de:  
  * `target_link_libraries`  
  * `target_include_directories`  
  * `target_compile_features`  
* Uso de interface libraries  
* Namespaced targets  

### Métricas / Evidências:  

* Build incremental eficiente  
* Facilidade para adicionar novos módulos  
* Ausência de dependências globais (`include_directories`)  
* Clareza e legibilidade dos CMakeLists  

---  

## 4. Princípios de Engenharia de Software  

**Criticidade predominante: Crítico**  

### SOLID  

* Single Responsibility  
* Open/Closed  
* Liskov Substitution  
* Interface Segregation  
* Dependency Inversion  

### Outros princípios  

* DRY  
* KISS  
* Separation of Concerns  
* Encapsulamento  

### Métricas / Evidências:  

* Classes com responsabilidades únicas  
* Baixo acoplamento entre módulos  
* Uso de interfaces ao invés de concretos  
* Existência de Dependency Injection  

---  

## 5. Uso de C++ Moderno  

**Criticidade predominante: Crítico**  

### Avaliar:  

* Uso correto de:  
  * `std::unique_ptr`  
  * `std::shared_ptr`  
  * `std::weak_ptr`  
* RAII consistente  
* Move semantics  
* `const-correctness`  
* Uso de `constexpr` e `noexcept`  
* Controle de ownership  

### Métricas / Evidências:  

* Ausência de vazamentos de memória  
* Clareza de ownership  
* Redução de cópias desnecessárias  
* Uso consistente de referências vs ponteiros  

---  

## 6. Integração com Qt  

**Criticidade predominante: Alto**  

### 6.1 Qt Core e Objetos  

* Uso adequado de `QObject`  
* Gerenciamento de ownership  
* Uso de `QPointer` quando necessário  

### 6.2 Signals/Slots  

* Uso consciente (evitar excesso)  
* Avaliação de custo  
* Evitar acoplamento implícito  

### 6.3 Concorrência  

* Uso de:  
  * QtConcurrent  
  * QThread  
  * Thread pools  
* Segurança em multithreading  

### 6.4 Containers e Tipos  

* Uso adequado de:  
  * QString  
  * QByteArray  
  * QVector / QList  
  * QHash / QMap  

### 6.5 Integração com QML  

* Separação UI vs lógica  
* Evitar lógica complexa em QML  
* Uso correto de bindings  

### 6.6 QML / JavaScript  

* Uso adequado de:  
  * Optional chaining (`?.`)  
  * Nullish coalescing (`??`)  
* Evitar binding loops  
* Uso de ferramentas como Synchronizer (Qt 6.10+)  

### Métricas / Evidências:  

* Ausência de binding loops  
* Baixo acoplamento entre C++ e QML  
* Threads seguras  
* Uso eficiente de sinais  

---  

## 7. Complexidade Estrutural e Cognitiva  

**Criticidade predominante: Alto**  

### Avaliar:  

* Complexidade ciclomática  
* Tamanho de classes e funções  
* Profundidade de hierarquia  
* Clareza de leitura  

### Métricas / Evidências:  

* Funções pequenas e focadas  
* Classes coesas  
* Baixa profundidade de herança  
* Fluxo de execução compreensível  

---  

## 8. Performance e Eficiência  

**Criticidade predominante: Alto**  

### Avaliar:  

* Complexidade algorítmica  
* Custo de abstrações  
* Cópias desnecessárias  
* Alocação de memória  
* Overhead de virtual calls  

### Métricas / Evidências:  

* Uso de profiling  
* Baixo número de alocações críticas  
* Uso de move semantics  
* Eficiência em containers  

---  

## 9. Testabilidade  

**Criticidade predominante: Crítico**  

### Avaliar:  

* Isolamento de dependências  
* Uso de interfaces  
* Facilidade de mock  

### Expansão:  

* Testes unitários  
* Testes de integração  
* Testes de UI (Qt/QML)  
* Testes de concorrência  

### Métricas / Evidências:  

* Cobertura de testes (%)  
* Tempo de execução dos testes  
* Facilidade de escrita de testes  
* Uso de frameworks (ex: Catch2, QTest)  

---  

## 10. Manutenibilidade e Evolução  

**Criticidade predominante: Crítico**  

### Avaliar:  

* Facilidade de adicionar funcionalidades  
* Impacto de mudanças  
* Risco de regressões  
* Clareza arquitetural  

### Métricas / Evidências:  

* Tempo para implementar mudanças  
* Número de módulos afetados por alteração  
* Existência de pontos de extensão  

---  

## 11. Robustez e Confiabilidade  

**Criticidade predominante: Crítico**  

### Avaliar:  

* Tratamento de erros  
* Validação de entradas  
* Consistência de estado  
* Segurança de memória  

### Métricas / Evidências:  

* Cobertura de cenários de erro  
* Uso de mecanismos de fallback  
* Testes de falha  

---  

## 12. Observabilidade e Diagnóstico  

**Criticidade predominante: Alto**  

### Avaliar:  

* Logging estruturado  
* Níveis de log (debug, info, warning, error)  
* Capacidade de diagnóstico em produção  

### Métricas / Evidências:  

* Clareza dos logs  
* Facilidade de rastrear problemas  
* Uso de tracing ou métricas  

---  

## 13. Governança Arquitetural  

**Criticidade predominante: Crítico**  

### Definição de Processo  

Este documento deve ser aplicado em:  

* Pull Requests críticos  
* Releases principais  
* Inclusão de novos módulos/plugins  

### Responsáveis  

* Arquitetos de software  
* Revisores técnicos  

### Critérios de Bloqueio  

O sistema **não deve ser aprovado** se:  

* Itens críticos possuem nota ≤ 1  
* Existem dependências cíclicas  
* Há violação grave de ownership/memória  
* Não há separação entre domínio e UI  

---  

## Resultado Final  

### Cálculo sugerido  

* Média ponderada por criticidade:  

  * Crítico = peso 4  
  * Alto = peso 3  
  * Médio = peso 2  
  * Baixo = peso 1  

### Classificação

| Score Final | Nível     |  
| ----------- | --------- |  
| 0 – 1.5     | Crítico   |  
| 1.6 – 2.5   | Fraco     |  
| 2.6 – 3.2   | Aceitável |  
| 3.3 – 3.7   | Bom       |  
| 3.8 – 4.0   | Excelente |  

---  

## Observação Final  

Este documento deve evoluir continuamente conforme:  

* Novas versões de C++ e Qt  
* Mudanças arquiteturais do sistema  
* Lições aprendidas em produção  