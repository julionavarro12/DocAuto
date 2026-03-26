#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

IGNORE_FILES = {"README.md", "index.md"}

def extract_h1(md_path):
    try:
        content = md_path.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"[AVISO] Não foi possível ler '{md_path}': {e}")
    return md_path.stem.replace("-", " ").replace("_", " ").title()

def build_nav_block(docs_dir):
    md_files = sorted(docs_dir.glob("*.md"))
    lines = ["nav:\n", '  - Home: index.md\n']
    found = False
    for md_path in md_files:
        if md_path.name in IGNORE_FILES:
            print(f"  - {md_path.name} (ignorado)")
            continue
        title = extract_h1(md_path)
        lines.append(f'  - "{title}": {md_path.name}\n')
        print(f"  + {md_path.name} → \"{title}\"")
        found = True
    if not found:
        print(f"[AVISO] Nenhum arquivo .md encontrado em '{docs_dir}'.")
    return "".join(lines)

def update_nav_in_file(config_path, new_nav_block):
    content = config_path.read_text(encoding="utf-8")
    nav_pattern = re.compile(r"^nav:\s*\n(?:[ \t]+.*\n|\s*-\s*\n)*", re.MULTILINE)
    if nav_pattern.search(content):
        new_content = nav_pattern.sub(new_nav_block, content)
    else:
        new_content = new_nav_block + "\n" + content
    config_path.write_text(new_content, encoding="utf-8")

    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="docs")
    parser.add_argument("--config", default="mkdocs.yml")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir).resolve()
    config_path = Path(args.config).resolve()

    if not docs_dir.is_dir():
        print(f"[ERRO] Pasta não encontrada: {docs_dir}")
        sys.exit(1)
    if not config_path.exists():
        print(f"[ERRO] mkdocs.yml não encontrado: {config_path}")
        sys.exit(1)

    print(f"\n[INFO] Lendo arquivos em: {docs_dir}")
    nav_block = build_nav_block(docs_dir)
    update_nav_in_file(config_path, nav_block)
    print(f"\n[OK] mkdocs.yml atualizado → {config_path}\n")

if __name__ == "__main__":
    main()
