#!/usr/bin/env python3
"""
Script de teste para verificar a conexão com a Gemini API.

Uso:
    GEMINI_API_KEY=... python3 lambda/test_zai_api.py
    GEMINI_API_KEY=... GEMINI_MODEL=gemini-1.5-flash python3 lambda/test_zai_api.py
"""

from google import genai
from google.genai import types
import os
import json

# API Key via ambiente (evita vazar credencial no repo)
API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
MODEL = (os.getenv("GEMINI_MODEL") or "gemini-3-flash-preview").strip()
THINKING_LEVEL = (os.getenv("GEMINI_THINKING_LEVEL") or "LOW").strip().upper()
ENABLE_GOOGLE_SEARCH = (os.getenv("GEMINI_ENABLE_GOOGLE_SEARCH") or "1").strip().lower() in (
    "1",
    "true",
    "yes",
)
SYSTEM_PROMPT = (
    "Você é uma assistente muito útil. "
    "Responda em PT-BR e em até 400 caracteres, texto corrido."
)


def _build_generate_content_config() -> types.GenerateContentConfig:
    cfg = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.6,
        max_output_tokens=1024,
    )

    if THINKING_LEVEL in ("LOW", "MEDIUM", "HIGH"):
        cfg.thinking_config = types.ThinkingConfig(thinking_level=THINKING_LEVEL)

    if ENABLE_GOOGLE_SEARCH:
        cfg.tools = [types.Tool(google_search=types.GoogleSearch())]

    return cfg


def test_gemini():
    print("=" * 60)
    print(f"Teste 1: Gemini API (model={MODEL})")
    print("=" * 60)

    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model=MODEL,
            contents="Olá! Responda apenas: Conexão OK!",
            config=_build_generate_content_config(),
        )

        text = (getattr(response, "text", "") or "").strip()
        print("✅ Sucesso!")
        print(f"Resposta: {text}")
        return True

    except Exception as e:
        details = {
            "exception_type": type(e).__name__,
            "message": str(e),
        }
        print("❌ Erro (detalhado):")
        print(json.dumps(details, ensure_ascii=False, indent=2))
        return False


def test_streaming():
    """Testa modo streaming"""
    print("\n" + "=" * 60)
    print("Teste 2: Streaming")
    print("=" * 60)

    try:
        client = genai.Client(api_key=API_KEY)

        response = client.models.generate_content_stream(
            model=MODEL,
            contents="Conte até 5 em português, separando por vírgula.",
            config=_build_generate_content_config(),
        )

        print("Streaming: ", end="")
        for chunk in response:
            if getattr(chunk, "text", None):
                print(chunk.text, end="", flush=True)

        print("\n✅ Streaming funcionou!")
        return True

    except Exception as e:
        details = {
            "exception_type": type(e).__name__,
            "message": str(e),
        }
        print("❌ Erro no streaming (detalhado):")
        print(json.dumps(details, ensure_ascii=False, indent=2))
        return False


if __name__ == "__main__":
    print("\n🚀 Iniciando testes da Gemini API\n")

    if not API_KEY:
        raise SystemExit(
            "Defina GEMINI_API_KEY no ambiente antes de rodar o teste."
        )
    
    results = []
    
    results.append(("Gemini", test_gemini()))

    if results[0][1]:
        results.append(("Streaming", test_streaming()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    for name, success in results:
        status = "✅ OK" if success else "❌ FALHOU"
        print(f"  {name}: {status}")
    
    print("\n" + "=" * 60)
    if results[0][1]:
        print("🎉 A Gemini API está funcionando!")
        print("   Configure GEMINI_API_KEY na Lambda e use GEMINI_MODEL se quiser trocar o modelo.")
    else:
        print("❌ O teste falhou. Verifique:")
        print("   1. Se a GEMINI_API_KEY está correta")
        print("   2. Se o modelo configurado em GEMINI_MODEL existe/está habilitado")
