# Event Bus (Pub/Sub)

O sistema de Event Bus implementa o padrão Publisher-Subscriber de forma fortemente tipada e segura para múltiplas threads. Ele permite que diferentes módulos, plugins e serviços do sistema comuniquem-se de forma assíncrona e totalmente desacoplada, sem conhecerem a existência uns dos outros.

---

## Características de Design

### Type Erasure

Os contratos no SDK (`IEventPublisher` e `IEventSubscriber`) oferecem uma API limpa baseada em templates (`publish<E>` e `subscribe<E>`).

Internamente, o C++ converte qualquer tipo de evento `E` em um `std::type_index` e um ponteiro opaco `const void*`. Isso significa que qualquer `struct` ou classe pode ser um evento, sem a necessidade de herdar de uma classe base como `QEvent` ou `BaseEvent`, eliminando overhead e acoplamento a hierarquias rígidas.

---

### Interface Segregation Principle

Ao dividir as responsabilidades em `IEventPublisher` e `IEventSubscriber`, o sistema permite a injeção de dependências estritas. Um módulo que apenas emite dados não precisa ter acesso à API de inscrição, aumentando a segurança do design arquitetural.

---

### RAII para Ciclo de Vida

O método de inscrição retorna um objeto `EventSubscription` gerenciado pelo desenvolvedor. Quando este objeto sai de escopo e é destruído, seu destrutor invoca automaticamente o cancelamento da inscrição. O uso de `std::weak_ptr` garante que o cancelamento seja seguro mesmo se o `EventBus` original já tiver sido destruído.

---

### Prevenção de Deadlocks e Reentrância (Thread-Safety)

A implementação concreta `core::EventBus` utiliza `std::shared_mutex` para otimizar as leituras concorrentes com múltiplas threads publicando simultaneamente. Durante o `publishImpl`, o bus adquire um lock de leitura apenas para criar um snapshot da lista de callbacks. A execução real dos callbacks ocorre fora do escopo do lock, prevenindo deadlocks caso um callback decida publicar um novo evento ou remover sua própria inscrição em resposta à mensagem recebida.

---

## Código-fonte

### `IEventBus.h`

```cpp
// Spectrum/sdk/contracts/EventBus.h
#pragma once

#include <Spectrum/sdk/contracts/IEventPublisher.h>
#include <Spectrum/sdk/contracts/IEventSubscriber.h>
#include <Spectrum/sdk/spectrumsdk_export.h>

namespace vmi::sdk {

class SPECTRUMSDK_EXPORT IEventBus : public IEventPublisher, public IEventSubscriber {
public:
    virtual ~IEventBus() = default;
};

} // namespace vmi::sdk
```

---

### `IEventPublisher.h`

```cpp
// Spectrum/sdk/contracts/IEventPublisher.h
#pragma once

#include <typeindex>
#include <Spectrum/sdk/spectrumsdk_export.h>

namespace vmi::sdk {

class SPECTRUMSDK_EXPORT IEventPublisher {

public:
    virtual ~IEventPublisher() = default;

    template <typename E> void publish( const E& event ) {
        publishImpl( std::type_index( typeid( E ) ), &event );
    }

protected:
    virtual void publishImpl( std::type_index typeIdx, const void* eventData ) = 0;
};

} // namespace vmi::sdk
```

---

### `IEventSubscriber.h`

```cpp
// Spectrum/sdk/contracts/IEventSubscriber.h
#pragma once

#include <typeindex>
#include <Spectrum/sdk/types/EventSubscription.h>
#include <Spectrum/sdk/spectrumsdk_export.h>

namespace vmi::sdk {

class SPECTRUMSDK_EXPORT IEventSubscriber {

public:
    virtual ~IEventSubscriber() = default;

    template <typename E> [[nodiscard]] EventSubscription subscribe( std::function<void( const E& )> callback ) {
        // Envolve o callback tipado em um callback genérico (Type Erasure)
        auto erasedCallback = [cb = std::move( callback )]( const void* data ) {
            cb( *static_cast<const E*>( data ) );
        };
        return subscribeImpl( std::type_index( typeid( E ) ), std::move( erasedCallback ) );
    }

protected:
    virtual EventSubscription subscribeImpl( std::type_index typeIdx, std::function<void( const void* )> callback ) = 0;
};

} // namespace vmi::sdk
```

---

### `PluginEvents.h`

```cpp
// Spectrum/sdk/contracts/PluginEvents.h
#pragma once

#include <QString>
#include <Spectrum/sdk/types/PluginDescriptor.h>

namespace vmi::sdk::events {

struct PluginDiscovered {
    vmi::sdk::PluginDescriptor descriptor;
};

struct PluginLoaded {
    QString pluginId;
};

struct PluginAboutToUnload {
    QString pluginId;
};

struct PluginUnloaded {
    QString pluginId;
};

} // namespace vmi::sdk::events
```

---

### `EventSubscription.h`

```cpp
// Spectrum/sdk/types/EventSubscription.h
#pragma once

#include <functional>
#include <Spectrum/sdk/spectrumsdk_export.h>

namespace vmi::sdk {

class SPECTRUMSDK_EXPORT EventSubscription {

public:
    using UnsubscribeFunc = std::function<void()>;

    EventSubscription() = default;
    explicit EventSubscription( UnsubscribeFunc func )
        : m_unsubscribe( std::move( func ) ) {}

    ~EventSubscription() {
        if ( m_unsubscribe != nullptr ) {
            m_unsubscribe();
        }
    };

    EventSubscription( EventSubscription&& ) = default;
    EventSubscription& operator=( EventSubscription&& ) = default;
    EventSubscription( const EventSubscription& ) = delete;
    EventSubscription& operator=( const EventSubscription& ) = delete;

private:
    UnsubscribeFunc m_unsubscribe;
};

} // namespace vmi::sdk
```

---

### `eventbus.h`

```cpp
// Spectrum/core/messaging/eventbus.h
#pragma once

#include <Spectrum/sdk/contracts/IEventBus.h>
#include <shared_mutex>
#include <unordered_map>
#include <vector>
#include <memory>
#include <atomic>

namespace vmi::core {

class EventBus final : public sdk::IEventBus, public std::enable_shared_from_this<EventBus> {

public:
    [[nodiscard]] static std::shared_ptr<EventBus> create();
    ~EventBus() override = default;

protected:
    void publishImpl( std::type_index typeIdx, const void* eventData ) override;
    sdk::EventSubscription subscribeImpl( std::type_index typeIdx,
                                          std::function<void( const void* )> callback ) override;

private:
    EventBus() = default;
    void unsubscribe( std::type_index typeIdx, uint64_t id );

    struct Handler {
        uint64_t id;
        std::function<void( const void* )> callback;
    };

    std::unordered_map<std::type_index, std::vector<Handler>> m_subscribers;
    mutable std::shared_mutex m_mutex;
    std::atomic<uint64_t> m_nextId { 0 };
};

} // namespace vmi::core
```

---

### `eventbus.cpp`

```cpp
// Spectrum/core/messaging/eventbus.cpp
#include <Spectrum/core/messaging/eventbus.h>

namespace vmi::core {

std::shared_ptr<EventBus> EventBus::create() {
    return std::shared_ptr<EventBus>( new EventBus() );
}

void EventBus::publishImpl( std::type_index typeIdx, const void* eventData ) {
    std::vector<std::function<void( const void* )>> snapshot;

    {
        // Escopo do lock de leitura
        std::shared_lock lock( m_mutex );
        if ( auto it = m_subscribers.find( typeIdx ); it != m_subscribers.end() ) {
            for ( const auto& handler : it->second ) {
                snapshot.push_back( handler.callback );
            }
        }
    }

    // Executa fora do lock para evitar deadlock por reentrância
    for ( const auto& cb : snapshot ) {
        cb( eventData );
    }
}

sdk::EventSubscription EventBus::subscribeImpl( std::type_index typeIdx, std::function<void( const void* )> callback ) {
    uint64_t id = 0;

    {
        // Escopo do lock de escrita
        std::unique_lock lock( m_mutex );
        id = ++m_nextId;
        m_subscribers[typeIdx].push_back( { id, std::move( callback ) } );
    }

    std::weak_ptr<EventBus> weak_this = shared_from_this();

    return sdk::EventSubscription( [weak_this, typeIdx, id]() {
        if ( auto bus = weak_this.lock() ) {
            bus->unsubscribe( typeIdx, id );
        }
    } );
}

void EventBus::unsubscribe( std::type_index typeIdx, uint64_t id ) {
    std::unique_lock lock( m_mutex );
    if ( auto it = m_subscribers.find( typeIdx ); it != m_subscribers.end() ) {
        std::erase_if( it->second, [id]( const auto& h ) {
            return h.id == id;
        } );
    }
}

} // namespace vmi::core
```

---

## Exemplo de Uso

```cpp
// Publicando um evento pelo EventBus
if ( m_eventBus != nullptr ) {
    vmi::sdk::events::UserLoggedIn event;
    event.username = username;

    m_eventBus->publish( event );
}
```