import os
import logging
import functools
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview").strip()

THINKING_LEVEL = os.getenv("GEMINI_THINKING_LEVEL", "MEDIUM").strip().upper()
ENABLE_GOOGLE_SEARCH = os.getenv("GEMINI_ENABLE_GOOGLE_SEARCH", "1").strip().lower() in (
    "1",
    "true",
    "yes",
)

SYSTEM_PROMPT = (
    "Você é uma assistente muito útil. "
    "Responda de forma clara e concisa em Português do Brasil. "
    "Toda resposta deve ter, no máximo, 4000 caracteres e o texto deve ser corrido."
)


def _truncate_4000(text: str) -> str:
    if not text:
        return ""
    return text.strip()[:4000]

@functools.lru_cache(maxsize=1)
def _get_genai_client() -> genai.Client:
    api_key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada no ambiente.")

    return genai.Client(api_key=api_key)


def _mensagem_amigavel_erro_gemini(exc: Exception) -> str:
    msg = str(exc) or type(exc).__name__
    return _truncate_4000(f"Erro ao chamar a API do Gemini: {msg}")

_history = []


def _build_generate_content_config() -> types.GenerateContentConfig:
    cfg = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.6,
        max_output_tokens=4000,
    )

    if THINKING_LEVEL in ("LOW", "MEDIUM", "HIGH"):
        cfg.thinking_config = types.ThinkingConfig(thinking_level=THINKING_LEVEL)

    if ENABLE_GOOGLE_SEARCH:
        cfg.tools = [types.Tool(google_search=types.GoogleSearch())]

    return cfg


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = (
            "Bem vindo ao assistente Gemini! Qual a sua pergunta?"
        )

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class GptQueryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GptQueryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        query = handler_input.request_envelope.request.intent.slots["query"].value
        response = generate_gpt_response(query)

        return (
            handler_input.response_builder.speak(response)
            .ask("Você pode fazer uma nova pergunta ou falar: sair.")
            .response
        )


def generate_gpt_response(query):
    try:
        if not query:
            return "Diga sua pergunta, por favor."

        client = _get_genai_client()

        # Mantém histórico leve (máx. 10 pares) entre invocações do Lambda.
        contents = []
        for item in _history[-20:]:
            contents.append(
                types.Content(
                    role=item["role"],
                    parts=[types.Part.from_text(text=item["text"])],
                )
            )
        contents.append(
            types.Content(role="user", parts=[types.Part.from_text(text=query)])
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=_build_generate_content_config(),
        )

        reply = _truncate_4000(getattr(response, "text", "") or "")

        _history.append({"role": "user", "text": query})
        _history.append({"role": "model", "text": reply})
        return reply or "Desculpe, não consegui gerar uma resposta agora."
    except Exception as e:
        logger.error("Erro na chamada Gemini: %s", str(e), exc_info=True)
        return _mensagem_amigavel_erro_gemini(e)


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Como posso te ajudar?"

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(
            handler_input
        ) or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Até logo!"

        return handler_input.response_builder.speak(speak_output).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, não consegui processar sua solicitação."

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GptQueryIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()