# Plano da Tarefa

## Contexto

- Data: 01/02/2026
- Objetivo: validar integração da SDK do GLM 4.7 e investigar erro de “sem saldo” na API.

## Fases

1. **Descoberta** (complete)
   - Mapear arquivos relevantes.
   - Identificar ponto de integração com GLM.
2. **Checagem com Context7** (complete)
   - Revisar docs oficiais da SDK GLM 4.7.
3. **Diagnóstico** (complete)
   - Comparar integração atual com padrão esperado.
4. **Correção** (complete)
   - Ajustes necessários e validação.
5. **Registro** (complete)
   - Atualizar achados e progresso.

## Erros encontrados

- Erro ao ler arquivo de instrução: .github/instructions/exemplos-dados.instructions.md não encontrado.
- Teste local: `python` não encontrado; `python3` executou, mas `zai-sdk` não está instalada.
- Teste no venv: ZAI_API_KEY/ZHIPUAI_API_KEY não configuradas no ambiente do terminal; SDK emite warning com Python 3.14.
- Teste com ZAI_API_KEY definida retornou 429 (rate limit/saldo insuficiente).
