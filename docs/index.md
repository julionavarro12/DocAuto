# 📄 Docs Pipeline (MkDocs + CI/CD)

Este projeto automatiza a geração e publicação de documentação utilizando **MkDocs**, com pipeline de CI/CD integrado ao **GitHub Actions**.

A ideia principal é simples:
👉 todo arquivo `.md` dentro da pasta `docs/` vira automaticamente uma página da documentação
👉 o menu (`nav`) é gerado automaticamente
👉 e o site é buildado e publicado no GitHub Pages

---

## 🚀 Tecnologias utilizadas

* Python 3.10
* MkDocs
* Material for MkDocs
* GitHub Actions (CI/CD)
* Docker (opcional)

---

## 📁 Estrutura do projeto

```bash
.
├── docs/
│   ├── index.md          # Página inicial
│   ├── teste.md          # Exemplo de página
│   ├── img/              # Imagens do site
│   └── stylesheets/
│       └── extra.css     # CSS customizado
│
├── scripts/
│   └── generate_nav.py   # Geração automática do menu
│
├── mkdocs.yml           # Configuração do MkDocs
├── requirements.txt     # Dependências Python
├── dockerfile           # (Opcional) container para build
└── .github/workflows/   # Pipeline CI/CD
```

---

## ⚙️ Como funciona

### 🔹 1. Escrita da documentação

Você só precisa criar arquivos `.md` dentro de `docs/`:

```bash
docs/
  index.md
  api.md
  arquitetura.md
```

---

### 🔹 2. Geração automática do menu

O script:

```bash
python scripts/generate_nav.py
```

* lê todos os arquivos `.md`
* extrai o título (`# Título`)
* atualiza automaticamente o `nav` no `mkdocs.yml`

---

### 🔹 3. Build da documentação

```bash
mkdocs build
```

Gera a pasta:

```bash
site/
```

---

### 🔹 4. Deploy automático (CI/CD)

A pipeline faz:

1. instala dependências
2. executa `generate_nav.py`
3. roda `mkdocs build`
4. publica no GitHub Pages

---

## 🌐 Acesso ao site

A documentação fica disponível em:

```
https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/
```

---

## ▶️ Rodando localmente

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o servidor local:

```bash
mkdocs serve
```

Acesse:

```
http://127.0.0.1:8000
```

---

## 🐳 Usando com Docker (opcional)

Build da imagem:

```bash
docker build -t docs-pipeline .
```

Rodar:

```bash
docker run -p 8000:8000 docs-pipeline
```

---

## 🎨 Customização

### CSS customizado

Arquivo:

```bash
docs/stylesheets/extra.css
```

Adicionado via:

```yaml
extra_css:
  - stylesheets/extra.css
```

---

### Logo e favicon

```yaml
theme:
  logo: img/logo.svg
  favicon: img/favicon.png
```

Arquivos devem estar em:

```bash
docs/img/
```

---

## ⚠️ Problemas comuns

### ❌ Site sem layout / quebrado

* Falta do `docs/index.md`
* CSS customizado incorreto
* caminhos errados em `logo` ou `favicon`

---

### ❌ CSS não carrega

* arquivo fora de `docs/`
* caminho errado no `mkdocs.yml`

---

### ❌ Deploy não atualiza

* verificar se GitHub Pages está configurado para usar **GitHub Actions**

---

## 📌 Boas práticas

* Sempre ter um `index.md`
* Evitar CSS global que sobrescreva o tema
* Manter arquivos dentro de `docs/`
* Usar CI para garantir consistência

---


