"""Бэкенды генерации.

openai_compatible — любой сервер с /chat/completions: llama.cpp (llama-server), vLLM,
Ollama, OpenRouter, облачные API с OpenAI-совместимым режимом. Где и на чём запускать
модель, решает тот, кто генерирует; скрипту нужны только base_url, model и (опц.) ключ.

mock — заглушка без модели: проверяет механику конвейера без GPU.
  Команды в ней — нейтральные плейсхолдеры (echo mock-...), а не данные.
  mode="clean" — корректные ответы; mode="dirty" — типичные дефекты формата ответа.
"""
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse


class OpenAICompatible:
    def __init__(self, cfg):
        b = cfg["backend"]
        for k in ("base_url", "model"):
            if not b.get(k):
                raise ValueError(f"backend.{k} не задан")
        parsed = urlparse(b["base_url"])
        if parsed.username or parsed.password or parsed.query:
            raise ValueError("не клади ключи и параметры в base_url — используй backend.api_key_env")
        self.url = b["base_url"].rstrip("/") + "/chat/completions"
        self.b = b
        self.s = cfg["sampling"]
        self.key = None
        if b.get("api_key_env"):
            self.key = os.environ.get(b["api_key_env"])
            if not self.key:
                raise ValueError(f"переменная окружения {b['api_key_env']} не задана")

    def describe(self):
        return {"provider": "openai_compatible", "base_url": self.b["base_url"], "model": self.b["model"]}

    def complete(self, messages, call_seed):
        body = {
            "model": self.b["model"],
            "messages": messages,
            "temperature": self.s["temperature"],
            "top_p": self.s["top_p"],
            "max_tokens": self.s["max_tokens"],
            "seed": call_seed,
        }
        if self.b.get("json_mode", True):
            body["response_format"] = {"type": "json_object"}
        body.update(self.b.get("extra_body") or {})  # параметры конкретного сервера: top_k, min_p, ...
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = "Bearer " + self.key
        retries = self.b.get("retries", 3)
        for attempt in range(retries + 1):
            try:
                req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers)
                with urllib.request.urlopen(req, timeout=self.b.get("timeout", 120)) as r:
                    res = json.load(r)
                return res["choices"][0]["message"]["content"] or "", res.get("usage", {})
            except urllib.error.HTTPError as exc:
                if exc.code not in (408, 429, 500, 502, 503, 504) or attempt == retries:
                    raise RuntimeError(f"provider_http_{exc.code}") from None  # тело ответа не печатаем
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt == retries:
                    raise RuntimeError(f"provider_unreachable: {getattr(exc, 'reason', exc)}") from None
            time.sleep(min(2 ** attempt, 20))


class Mock:
    """Детерминированная заглушка. Ответ зависит от промпта и call_seed."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.mode = cfg["backend"].get("mode", "clean")
        self.classes = cfg["labels"]["classes"]
        self.n = cfg["prompt"]["candidates_per_call"]

    def describe(self):
        return {"provider": "mock", "mode": self.mode}

    def _candidates(self, key):
        out = []
        for i in range(self.n):
            out.append({
                "command": f"echo mock-{key}-{i}",
                "description": f"Плейсхолдер mock #{i}",
                "util": "echo",
                "class": self.classes[i % len(self.classes)],
                "severity": "low",
            })
        return out

    def complete(self, messages, call_seed):
        key = hashlib.sha256((messages[-1]["content"] + str(call_seed)).encode()).hexdigest()[:8]
        cands = self._candidates(key)
        if self.mode != "dirty":
            return json.dumps({"candidates": cands}, ensure_ascii=False), {"mock": True}
        # dirty: дефект выбирается по ключу, чтобы покрыть все ветки clean/validate
        kind = int(key, 16) % 7
        if kind == 0:   # ответ обёрнут в markdown
            raw = "Вот результат:\n```json\n" + json.dumps({"candidates": cands}, ensure_ascii=False) + "\n```"
        elif kind == 1:  # лишнее экранирование кавычек внутри команды
            cands[0]["command"] = f'echo \\"mock-{key}\\"'
            raw = json.dumps({"candidates": cands}, ensure_ascii=False)
        elif kind == 2:  # посторонний скрипт в команде
            cands[0]["command"] = f"echo mock-{key} 你好"
            raw = json.dumps({"candidates": cands}, ensure_ascii=False)
        elif kind == 3:  # битый JSON
            raw = json.dumps({"candidates": cands}, ensure_ascii=False)[:-7]
        elif kind == 4:  # блок рассуждений + повтор команды
            cands[1]["command"] = cands[0]["command"]
            raw = "<think>рассуждаю</think>" + json.dumps({"candidates": cands}, ensure_ascii=False)
        elif kind == 5:  # класс вне списка
            cands[0]["class"] = "maybe"
            raw = json.dumps({"candidates": cands}, ensure_ascii=False)
        else:            # синтаксическая ошибка bash
            cands[0]["command"] = f"echo mock-{key} ("
            raw = json.dumps({"candidates": cands}, ensure_ascii=False)
        return raw, {"mock": True, "defect": kind}


def make_backend(cfg):
    return {"mock": Mock, "openai_compatible": OpenAICompatible}[cfg["backend"]["provider"]](cfg)
