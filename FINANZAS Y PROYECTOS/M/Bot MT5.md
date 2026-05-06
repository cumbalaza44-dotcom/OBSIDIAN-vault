Tú editas en iOS
  → plugin sync push cada 3 min (ya existe)
    → cron pull en VPS cada 5 min (nuevo, 0 tokens)
      → yo leo índice actualizado en heartbeat (1 read, ~200 tokens)
Tú editas en iOS
  → yo hago git fetch en heartbeat (gasta tokens en red + razonamiento)
  → si hay cambios, leo índice (otro read)
  