

objetivo reconocer hasta el ultimo tornillo equipos y como estan conectados 


equipos 
servidores gpu xe 9680 dell  rack

| equipos      | cqantidad |
| ------------ | --------- |
| DELL XE 9680 | 4         |
| r660         |           |


| Opción          | Calidad ES                                       | RAM/CPU                           | Latencia CPU            | Licencia                    | Voz ES                                     | Veredicto Hetzner 8GB                                                     |
| --------------- | ------------------------------------------------ | --------------------------------- | ----------------------- | --------------------------- | ------------------------------------------ | ------------------------------------------------------------------------- |
| edge-tts (ref.) | Buena (neural MS, es-CO-SalomeNeural existe)     | ~200MB, API remota                | 1–3s (red)              | Gratis, TOS MS no-oficial   | ✅ es-CO, es-MX, es-ES                     | Baseline actual. Gratis pero depende de MS, puede romperse                |
| Piper TTS       | Media-buena (robotica leve)                      | ~100–300MB, CPU realtime (5.6x+)  | <1s local               | MIT                         | ✅ es_MX-claude-high (mejor), es_AR, es_ES | ✅ Mejor local gratis. Rápido, offline                                    |
| Coqui XTTS-v2   | Muy buena + clonación voz                        | 8GB mín, 16GB recom. Modelo 2.1GB | 10–60s CPU por frase    | MPL-2.0 (no comercial puro) | ✅ ES multilingüe                          | ⚠️ Corre en 8GB pero lento y justo; mejor con GPU                         |
| OpenVoice v2    | Buena (clonación, necesita TTS base)             | ~0.8GB fp32, CPU viable           | 5–15s                   | MIT                         | ✅ Multilingüe incl. ES                    | ✅ Liviano, bueno para clonar voz fija                                    |
| Bark            | Expresiva pero inconsistente, ES con acento raro | 4.5–12GB                          | Muy lento CPU (minutos) | MIT                         | ⚠️ ES existe pero flojo                    | ❌ Descartado: pesado y lento                                             |
| StyleTTS 2      | Muy buena en EN, ES no oficial                   | 2–4GB                             | Lento CPU               | Varía (research)            | ❌ Sin ES oficial                          | ❌ Descartado para ES                                                     |
| ElevenLabs API  | Excelente (mejor ES latino)                      | 0 (API)                           | 1–3s                    | Comercial                   | ✅ Voces ES nativas + clonación            | ✅ Mejor calidad; $5–6/mes basta para notas voz                           |
| OpenAI TTS API  | Buena (nova, onyx hablan ES)                     | 0 (API)                           | 1–2s                    | Comercial                   | ⚠️ Multilingüe, sin es-CO específico       | ✅ Barato: tts-1 $15/1M chars (~$0.015/1K). Ojo: tts-1 deprecado ene-2027 |
| Cartesia API    | Excelente, ultra-baja latencia                   | 0 (API)                           | <0.5s                   | Comercial                   | ✅ ES disponible                           | ✅ Bueno pero más caro que OpenAI                                         |
