# Voz da Biblioteca do Gato Preto (XTTS-v2, PT-BR)

Voz de narração usada nos audiolivros do canal **Biblioteca do Gato Preto**.

Não é um modelo treinado. É o modelo público **XTTS-v2** (Coqui) clonando a voz a partir de um áudio de referência.
Este repositório traz a referência, uma amostra e um script para narrar.

## Arquivos

| Arquivo | O que é |
|---|---|
| `voz/referencia-pt.wav` | Áudio de referência que o XTTS clona (frases em português emendadas) |
| `voz/amostra-aprovada.wav` | Exemplo de como a voz soa |
| `narrar.py` | Narra um `.txt` e grava um `.wav` |

## Como usar

Python 3.11 e, de preferência, placa NVIDIA.

```
pip install coqui-tts torch numpy
python narrar.py meu-texto.txt saida.wav
```

Na primeira vez o modelo XTTS-v2 (~1,8 GB) é baixado sozinho.

Ajustes que usamos: velocidade 1.00, uma frase por vez, sem o ponto final no texto enviado ao modelo
(em português ele às vezes lê "ponto"). O resultado fica em torno de 140 palavras por minuto.

## Origem da voz

Voz sintética: criada no Voice Design do ElevenLabs, clonada no XTTS-v2 e depois refeita com uma referência em português
para tirar o sotaque. Não é a voz de nenhuma pessoa real.

## Licença

O modelo XTTS-v2 segue a [Coqui Public Model License](https://coqui.ai/cpml) (uso **não comercial**).
Os áudios deste repositório são do canal Biblioteca do Gato Preto.
