#!/usr/bin/env python3
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR.parent / "docs"
MKDOCS_FILE = BASE_DIR.parent / "mkdocs.yml"
IGNORE_FILES = {"README.md"}


def pegar_titulo_arquivo(arquivo_md):
    try:
        conteudo = arquivo_md.read_text(encoding="utf-8")
        resultado = re.search(r"^#\s+(.+)$", conteudo, re.MULTILINE)

        if resultado:
            return resultado.group(1).strip()
    except Exception as erro:
        print(f"[AVISO] Erro ao ler {arquivo_md.name}: {erro}")

    return arquivo_md.stem.replace("-", " ").replace("_", " ").title()


def montar_nav():
    linhas_nav = []
    arquivos_md = sorted(DOCS_DIR.glob("*.md"))

    linhas_nav.append("nav:\n")

    if (DOCS_DIR / "index.md").exists():
        linhas_nav.append("  - Home: index.md\n")

    for arquivo in arquivos_md:
        if arquivo.name in IGNORE_FILES or arquivo.name == "index.md":
            print(f"  - {arquivo.name} (ignorado)")
            continue

        titulo = pegar_titulo_arquivo(arquivo)
        linhas_nav.append(f'  - "{titulo}": {arquivo.name}\n')
        print(f'  + {arquivo.name} -> "{titulo}"')

    return "".join(linhas_nav)


def atualizar_mkdocs(nova_nav):
    conteudo = MKDOCS_FILE.read_text(encoding="utf-8")

    padrao_nav = re.compile(r"(?s)^nav:\n.*?(?=^\w|\Z)", re.MULTILINE)

    if re.search(r"^nav:\n", conteudo, re.MULTILINE):
        conteudo = re.sub(padrao_nav, nova_nav + "\n", conteudo)
    else:
        conteudo = nova_nav + "\n" + conteudo

    MKDOCS_FILE.write_text(conteudo, encoding="utf-8")


def main():
    if not DOCS_DIR.exists():
        print(f"[ERRO] Pasta docs não encontrada em: {DOCS_DIR}")
        return

    if not MKDOCS_FILE.exists():
        print(f"[ERRO] Arquivo mkdocs.yml não encontrado em: {MKDOCS_FILE}")
        return

    print(f"[INFO] Lendo arquivos da pasta: {DOCS_DIR}")
    nova_nav = montar_nav()
    atualizar_mkdocs(nova_nav)
    print("[OK] mkdocs.yml atualizado com sucesso.")


if __name__ == "__main__":
    main()