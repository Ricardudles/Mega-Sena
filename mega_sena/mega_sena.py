import secrets
from collections import defaultdict
from pathlib import Path

ARQUIVO_EXISTENTES = "numeros_existentes.txt"
ARQUIVO_NOVOS = "numeros_novos.txt"
QUANTIDADE_NOVOS_JOGOS = 16


def erro(msg):
    print(f"\n❌ ERRO: {msg}")
    exit(1)


def parse_linha(linha: str, numero_linha: int):
    linha = linha.strip()

    if not linha:
        return None

    partes = linha.split("-")

    if len(partes) != 6:
        erro(f"Linha {numero_linha}: deve conter exatamente 6 números.")

    try:
        numeros = [int(p) for p in partes]
    except ValueError:
        erro(f"Linha {numero_linha}: contém valor não numérico.")

    if len(set(numeros)) != 6:
        erro(f"Linha {numero_linha}: números duplicados na mesma combinação.")

    for n in numeros:
        if n < 1 or n > 60:
            erro(f"Linha {numero_linha}: número fora do intervalo (1–60).")

    return tuple(sorted(numeros))


def carregar_jogos_existentes():
    caminho = Path(ARQUIVO_EXISTENTES)

    if not caminho.exists():
        erro(f"Arquivo '{ARQUIVO_EXISTENTES}' não encontrado.")

    jogos = []

    with caminho.open(encoding="utf-8") as f:
        for i, linha in enumerate(f, start=1):
            jogo = parse_linha(linha, i)
            if jogo:
                jogos.append(jogo)

    if not jogos:
        erro("Arquivo de números existentes está vazio.")

    return jogos


def detectar_duplicados(jogos):
    contador = defaultdict(int)
    for jogo in jogos:
        contador[jogo] += 1

    return {jogo: qtd for jogo, qtd in contador.items() if qtd > 1}


def gerar_novos_jogos(jogos_existentes):
    existentes = set(jogos_existentes)
    novos = set()
    rng = secrets.SystemRandom()

    while len(novos) < QUANTIDADE_NOVOS_JOGOS:
        jogo = tuple(sorted(rng.sample(range(1, 61), 6)))

        if jogo in existentes or jogo in novos:
            continue

        novos.add(jogo)

    return sorted(novos)


def salvar_novos_jogos(jogos):
    caminho = Path(ARQUIVO_NOVOS)

    with caminho.open("w", encoding="utf-8") as f:
        for jogo in jogos:
            f.write("-".join(f"{n:02d}" for n in jogo) + "\n")


def main():
    print("📂 Lendo números existentes...")
    jogos_existentes = carregar_jogos_existentes()
    print(f"🔢 Total de jogos válidos: {len(jogos_existentes)}")

    print("\n🔍 Verificando duplicados...")
    duplicados = detectar_duplicados(jogos_existentes)

    if duplicados:
        print("⚠️ COMBINAÇÕES DUPLICADAS ENCONTRADAS:")
        for jogo, qtd in duplicados.items():
            print(f"  {'-'.join(f'{n:02d}' for n in jogo)} → {qtd} vezes")
    else:
        print("✅ Nenhuma combinação duplicada.")

    print("\n🎲 Gerando novos jogos...")
    novos = gerar_novos_jogos(jogos_existentes)
    print(f"✅ {len(novos)} novos jogos gerados.")

    salvar_novos_jogos(novos)
    print(f"\n💾 Arquivo '{ARQUIVO_NOVOS}' criado/atualizado com sucesso.")


if __name__ == "__main__":
    main()
