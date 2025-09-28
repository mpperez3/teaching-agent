
## Pregunta 2: Optimización con Ordenación por Selección

Para mejorar la eficiencia en torneos con muchos equipos, se desea implementar también el algoritmo de ordenación por selección.

### Funcionamiento del algoritmo de Selección:
- En cada iteración, busca el equipo mejor clasificado entre los elementos no ordenados
- Lo coloca en la primera posición disponible de la parte ordenada
- Continúa hasta que todos los elementos estén ordenados

```java
public static void sortBySelection(TeamRanking[] rankings)
// Modifica: rankings  
// Produce: ordena el array de equipos de mejor a peor clasificado usando ordenación por selección
```

---

## Pregunta 3: Análisis de Rendimiento y Lista Enlazada

El torneo ha crecido y ahora maneja equipos mediante una estructura de lista enlazada simple. La lista se implementa con nodos que contienen la información del equipo y una referencia al siguiente nodo.

### Representación interna de la estructura:
- **Nodo**: Cada nodo contiene un objeto `TeamRanking` y una referencia `next` al siguiente nodo
- **Lista**: La lista mantiene únicamente una referencia al primer nodo (`head`)
- **Fin de lista**: El último nodo tiene `next = null`

```java
public class TeamNode {
    private TeamRanking team;
    private TeamNode next;
    
    public TeamNode(TeamRanking team) {
        this.team = team;
        this.next = null;
    }
    
    // Getters y setters
    public TeamRanking getTeam() { return this.team; }
    public void setTeam(TeamRanking team) { this.team = team; }
    
    public TeamNode getNext() { return this.next; }
    public void setNext(TeamNode next) { this.next = next; }
}
```

### Apartado A: Ordenación por Inserción en Lista Enlazada

Implementa un método que ordene una lista enlazada de equipos usando el algoritmo de inserción. Este algoritmo toma cada nodo (empezando por el segundo) y lo inserta en su posición correcta dentro de la parte ya ordenada de la lista.

```java
public static TeamNode sortByInsertion(TeamNode head)
// Produce: devuelve la referencia al primer nodo de la lista ordenada de mejor a peor clasificado
```

### Apartado B: Análisis de Complejidad

Analiza la complejidad temporal de los tres algoritmos implementados:

1. **Ordenación Burbuja**: Indica la complejidad en el mejor caso, peor caso y caso promedio
2. **Ordenación Selección**: Indica la complejidad en el mejor caso, peor caso y caso promedio  
3. **Ordenación Inserción**: Indica la complejidad en el mejor caso, peor caso y caso promedio

Justifica tus respuestas explicando qué situaciones corresponden a cada caso.

---

## Ejemplo de Funcionamiento

Dados los siguientes equipos al inicio:
- Equipo A: 15 puntos, diferencia de goles +8, goles a favor 25
- Equipo B: 18 puntos, diferencia de goles +5, goles a favor 22  
- Equipo C: 15 puntos, diferencia de goles +8, goles a favor 30
- Equipo D: 18 puntos, diferencia de goles +7, goles a favor 28

La clasificación final debería ser:
1. Equipo D (18 puntos, +7 diferencia)
2. Equipo B (18 puntos, +5 diferencia)  
3. Equipo C (15 puntos, +8 diferencia, 30 goles a favor)
4. Equipo A (15 puntos, +8 diferencia, 25 goles a favor)

---

## Restricciones de Implementación

- Código fuente siempre en inglés (nombres de variables, métodos, comentarios)
- Atributos siempre privados con modificadores de acceso explícitos
- No usar `break` excepto en estructuras `switch`
- No usar `return void`
- Implementar getters y setters para todos los atributos privados
- Usar únicamente Java 21 (API estándar)
