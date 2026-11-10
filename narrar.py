"""Narra um texto em PT-BR com a voz da Biblioteca do Gato Preto (XTTS-v2).

Uso:
  python narrar.py texto.txt saida.wav

Na 1a vez o Coqui TTS baixa o modelo XTTS-v2 (~1,8 GB) sozinho.
Ajuste aprovado: velocidade 1.00, frase por frase, sem o ponto final
(o XTTS em portugues as vezes le "ponto").
"""
import os
import re
import sys
import wave
from pathlib import Path

import numpy as np

os.environ.setdefault("COQUI_TOS_AGREED", "1")

from TTS.api import TTS  # noqa: E402

BASE = Path(__file__).resolve().parent
REFERENCIA = str(BASE / "voz" / "referencia-pt.wav")
SR = 24000
PAUSA_FRASE = 0.42
PAUSA_PARAGRAFO = 0.90


def frases(paragrafo):
    partes = re.split(r"(?<=[.!?…])\s+", paragrafo.strip())
    return [p for p in partes if p.strip()]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    texto = Path(sys.argv[1]).read_text(encoding="utf-8")
    saida = Path(sys.argv[2])

    import torch
    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(dispositivo)

    audio = []
    for paragrafo in re.split(r"\n\s*\n", texto):
        for f in frases(paragrafo):
            f = f.rstrip(".")
            wav = tts.tts(text=f, speaker_wav=REFERENCIA, language="pt", speed=1.0)
            audio.append(np.asarray(wav, dtype=np.float32))
            audio.append(np.zeros(int(SR * PAUSA_FRASE), dtype=np.float32))
        audio.append(np.zeros(int(SR * (PAUSA_PARAGRAFO - PAUSA_FRASE)), dtype=np.float32))

    pcm = (np.clip(np.concatenate(audio), -1, 1) * 32767).astype(np.int16)
    with wave.open(str(saida), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"Pronto: {saida}")


if __name__ == "__main__":
    main()
