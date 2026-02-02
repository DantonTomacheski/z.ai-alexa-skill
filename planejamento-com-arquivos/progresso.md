# Progresso

- Sessão iniciada.
- Nenhum teste executado ainda.
- Erro ao ler arquivo de instrução: .github/instructions/exemplos-dados.instructions.md não encontrado.
- Ajustes feitos: lambda/lambda_function.py e lambda/test_api_key.py (env vars e seleção de cliente).
- Teste local falhou: `python` não encontrado; `python3` executou, mas faltou `zai-sdk`.
- Instalação global via pip falhou (PEP 668); dependências instaladas usando o venv do projeto.
- Teste no venv falhou: ZAI_API_KEY/ZHIPUAI_API_KEY não configuradas no ambiente do terminal; warning da SDK sobre Python 3.14.
- Teste com ZAI_API_KEY definida retornou 429 (rate limit/saldo insuficiente).
