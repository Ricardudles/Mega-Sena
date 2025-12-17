import secrets
from collections import defaultdict
from pathlib import Path

ARQUIVO_EXISTENTES = "numeros_existentes.txt"
ARQUIVO_NOVOS = "numeros_novos.txt"
QUANTIDADE_NOVOS_JOGOS = 16


def parse_linha(linha: str):
    linha = linha.strip().rstrip(",")
    partes = linha.replace("+", "-").split("-")
    numeros = sorted(int(p) for p in partes)
    if len(numeros) != 6:
        raise ValueError(f"Linha inválida: {linha}")
    if any(n < 1 or n > 60 for n in numeros):
        raise ValueError(f"Número fora do intervalo 1–60: {linha}")
    return tuple(numeros)


def carregar_jogos_existentes():
    caminho = Path(ARQUIVO_EXISTENTES)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo '{ARQUIVO_EXISTENTES}' não encontrado.")

    jogos = []
    with caminho.open(encoding="utf-8") as f:
        for linha in f:
            if linha.strip():
                jogos.append(parse_linha(linha))

    return jogos


def detectar_duplicados(jogos):
    contador = defaultdict(int)
    for jogo in jogos:
        contador[jogo] += 1

    duplicados = {jogo: qtd for jogo, qtd in contador.items() if qtd > 1}
    return duplicados


def gerar_novos_jogos(jogos_existentes):
    existentes_set = set(jogos_existentes)
    novos = set()
    rng = secrets.SystemRandom()

    while len(novos) < QUANTIDADE_NOVOS_JOGOS:
        jogo = tuple(sorted(rng.sample(range(1, 61), 6)))

        if jogo in existentes_set:
            continue

        if jogo in novos:
            continue

        novos.add(jogo)

    return sorted(novos)


def salvar_novos_jogos(jogos):
    with open(ARQUIVO_NOVOS, "w", encoding="utf-8") as f:
        for jogo in jogos:
            linha = "-".join(f"{n:02d}" for n in jogo)
            f.write(linha + "\n")


def main():
    print("📂 Lendo arquivo de números existentes...")
    jogos_existentes = carregar_jogos_existentes()

    print(f"🔢 Total de jogos lidos: {len(jogos_existentes)}")

    print("\n🔍 Verificando duplicados...")
    duplicados = detectar_duplicados(jogos_existentes)

    if duplicados:
        print("⚠️ DUPLICADOS ENCONTRADOS:")
        for jogo, qtd in duplicados.items():
            print(f"  {jogo} → {qtd} vezes")
    else:
        print("✅ Nenhum jogo duplicado encontrado.")

    print("\n🎲 Gerando novos jogos...")
    novos_jogos = gerar_novos_jogos(jogos_existentes)

    print(f"✅ {len(novos_jogos)} novos jogos gerados com sucesso.")

    salvar_novos_jogos(novos_jogos)

    print(f"\n💾 Arquivo '{ARQUIVO_NOVOS}' criado com sucesso.")


if __name__ == "__main__":
    main()
