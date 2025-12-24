# 🎰 Mega Sena Gerenciador

Uma aplicação GUI Python para gerenciar jogos da Mega Sena, garantindo que não haja duplicatas e facilitando a geração de novos jogos únicos! 🚀

## 📋 O que faz?

- Carrega jogos existentes de um arquivo (`numeros_existentes.txt`)
- Detecta e destaca jogos duplicados e inválidos
- Exibe estatísticas dos jogos (total, OK, duplicados, inválidos, por tamanho)
- Gera novos jogos únicos de 6 números, evitando duplicatas com os existentes
- Permite salvar os novos jogos diretamente no arquivo existente
- Interface gráfica intuitiva com tabelas para visualização

## 🛠️ Como usar?

### Pré-requisitos

- Python 3.x instalado
- Tkinter (geralmente vem com Python)
- Arquivo `numeros_existentes.txt` com jogos antigos (um por linha, formato: 01-02-03-04-05-06 ou 01-02-03-04-05-06-07)

### Passos

1. **Prepare o arquivo**: Crie ou edite `numeros_existentes.txt` com seus jogos antigos.
2. **Execute a aplicação**:
   ```bash
   python mega_sena.py
   ```
3. **Gerencie seus jogos**:
   - Visualize os jogos existentes na tabela superior
   - Veja as estatísticas no topo
   - Digite a quantidade de novos jogos desejados
   - Clique em "Gerar novos" para pré-visualizar
   - Clique em "Salvar novos" para adicionar ao arquivo existente
   - Use "🔄 Refresh" para recarregar os dados

### Exemplo de formato dos jogos

```
01-15-23-34-45-60
05-12-18-27-39-55
01-02-03-04-05-06-07
```

## 🎯 Funcionalidades

- **Validação rigorosa**: Jogos devem ter 6 ou 7 números únicos entre 1 e 60
- **Detecção de duplicados**: Identifica jogos repetidos automaticamente
- **Geração segura**: Usa `secrets.SystemRandom()` para números verdadeiramente aleatórios
- **Interface amigável**: Tabelas com cores alternadas e status visuais
- **Gestão integrada**: Tudo em um único arquivo de dados

## 📊 Estatísticas

A aplicação mostra em tempo real:

- Total de jogos
- Jogos válidos (OK)
- Jogos duplicados
- Jogos inválidos
- Contagem por tamanho (6 ou 7 números)

Divirta-se gerenciando seus jogos e boa sorte! 🍀
