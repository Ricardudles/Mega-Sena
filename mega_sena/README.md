# 🎰 Mega Sena Generator

Um script Python simples e divertido para gerar novos jogos da Mega Sena, garantindo que não haja duplicatas com jogos existentes! 🚀

## 📋 O que faz?

- Lê jogos existentes de um arquivo
- Verifica se há duplicados nos jogos antigos
- Gera 16 novos jogos únicos e aleatórios
- Salva os novos jogos em outro arquivo

## 🛠️ Como usar?

### Pré-requisitos

- Python 3.x instalado
- Arquivo `numeros_existentes.txt` com jogos antigos (um por linha, formato: 01-02-03-04-05-06)

### Passos

1. **Prepare o arquivo**: Crie ou edite `numeros_existentes.txt` com seus jogos antigos.
2. **Execute o script**:
   ```bash
   python mega_sena.py
   ```
3. **Confira os resultados**: Os novos jogos estarão em `numeros_novos.txt`.

### Exemplo de formato dos jogos

```
01-15-23-34-45-60
05-12-18-27-39-55
```

## 🎯 Dicas

- Cada jogo deve ter exatamente 6 números entre 1 e 60
- Números separados por hífen (-)
- Uma linha por jogo
- O script usa geração segura de números aleatórios (nada de sorte falsa aqui! 😉)

Divirta-se jogando e boa sorte! 🍀
