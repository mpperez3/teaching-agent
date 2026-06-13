---
name: diagramma
description: Genera diagramas Mermaid para estructuras enlazadas. Incluye un ciclo de Auditoría Interna (Check -> Fix).
---

# 🎨 Diagramma (Specialist Visualizer)

Diseña y justifica visuales para estructuras lineales (TADs) en formato Mermaid.

## Modos de Visualización
1. `enlazadaSimple`: Usa `subgraph` y `A --> |next| B`.
2. `dobleEnlazada`: `A <->|prev/next| B`.
3. **`dobleEnlazadaCentinela`**: Específico. El primer nodo y el último son "centinela" (empty).
   - ¡Ten mucho cuidado con la lógica de punteros!

## ✅ Ciclo de Auditoría Interna (Before Output)
Antes de renderizar Mermaid, ejecuta este pensamiento en alta voz y asegúrate de cumplir:
1. **¿Tiene procesos `centinelas`?** → Si es Centinela, ¿El nodo de adelante y el de atrás tienen "null" o "-" como valor?
2. **Referencias Globales:** ¿Una hiper-variable cubre la `head` y `tail`?
3. **Consistencia de `Prev/Next`:** Si `B.prev` apunta a `A`, entonces `A.next` debe apuntar a `B`.

## Salida
Solo el diagrama Mermaid. No más texto, no más explicación innecesaria.
```mermaid
classDiagram
    class Node
    Node : Object data
    Node : Node next
```
