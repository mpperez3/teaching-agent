## Ejercicio 1 [Lista + Cola]

Se ha decidido diseñar el TAD `Office` que representa una oficina. Una oficina se define como una colección de empleados. Cada empleado de la oficina está identificado por un código y tiene que trabajar sobre una cola de dossiers que tiene asignados. Para ello se ha decidido diseñar el TAD `Office` , con las operaciones que se indican a continuación:

```java
public interface Office extends Iterable<Employee> { 
    public int numEmployees();                                                  
	// Produce: devuelve el número de Employees de la Office. 
    
    public Employee get(int code) throws IllegalArgumentException; 
    // Produce: devuelve el empleado con el código que se pasa como parámetro. Si no existe, lanza la excepción 		IllegalArgumentException.  
    
    public void add(int code); 
    // Modifica: this 
    // Produce: añade un empleado a la oficina con el código que se pasa como parámetro y una cola de 	
    // Dossiers vacía. 
    
    public boolean remove(int code); 
    // Modifica: this 
    // Produce: si el empleado tiene dossier en su cola, retorna false; en otro caso, elimina un empleado de la oficina y retorna true. 
    
    public boolean setDossier(Dossier x); 
    // Modifica: this 
    // Produce: si la oficina está vacía, devuelve falso; en otro caso, asigna el dossier x al empleado con	la cola de Dossiers de menor tamaño y retorna true. Si varios empleados tienen el mismo número de dossiers en su cola y son los de menor tamaño se le asigna a cualquiera de ellos. 
        
    public boolean removeDossier(Employee e); 
    // Modifica: this 
    // Produce: si la cola de Dossiers del empleado e está vacía retorna false; en otro caso, elimina un Dossier de la cola de Dossiers del empleado e y retorna true. 
}
```

Para implementar la interfaz `Office` se ha decidido utilizar la siguiente clase cuya estructura de datos es una Lista :

```java
public class OfficeImp implements Office { 
    private Lista<Employee> listEmployees; 
}
```

Así como las clases `Employee` y `Dossier` :

```java
public class Employee { 
    private int code;
    private Queue<Dossier> dossiers; 
    
    public Employee(int c) { 
        code = c; 
        dossiers = new LinkedQueue<>(); 
    } 
    public int getCode() { 
        return code; 
    } 
    public Queue<Dossier> getDossiers() { 
        return dossiers; 
    } 
    // Otros métodos 
    // ....
} 
    
```

```java
public class Dossier { 
    private int number; 
    private String text; 
    
    public Dossier(int n, String t) { 
        number = n; 
        text = t; 
    } 
    public int getNumber() { 
        return number; 
    } 
    public String getText() { 
        return text; 
    } 
}
```



Se pide:

1. Continuar con la implementación de la clase `OfficeImp` escribiendo el código de la operación `setDossier` :

```java
public boolean setDossier(Dossier x) 
// Modifica: this 
// Produce: si la oficina está vacía, devuelve falso; en otro caso asigna el dossier x al empleado con la cola de dossiers de menor tamaño y retorna true. Si varios empleados tienen el mismo número de dossiers en su cola y son los de menor tamaño se le asigna a cualquiera de ellos.
```



2. Haciendo uso de la interfaz `Office` , resuelve el siguiente método:

```java
public static Lista<Integer> listDossiers(int code, Office office) 
// Produce: devuelve una lista con los números de dossier que están en la cola del empleado con el código que se pasa como parámetro.
```



## Ejercicio 2 [Lista + Pila]

Los compiladores de lenguajes de bloques utilizan lo que se denomina una **tabla de símbolos** . Estas tablas se caracterizan porque, cuando el compilador entra en un nuevo bloque B, todos los objetos que se declaran en él esconden las apariciones de objetos con el mismo nombre que aparecen en los bloques que envuelvan a B, y cuando el compilador sale del bloque, todos los objetos que estaban escondidos vuelven a ser visibles.

Una posible implementación del TDA `SymbolTable` es considerar que es una pila de listas. Cada lista guarda elementos que son pares `<identifier, type>` , donde identificador es una cadena de caracteres que representa el nombre de la variable y característica es una cadena de caracteres que representa el tipo de la variable en cuestión. En esta lista no puede haber dos variables con el mismo identificador.

La interfaz del TAD `SymbolTable` es la siguiente:

```java
public interface TSimbol { 
    public void in(); 
    // Modifica: this 
    // Produce:  añade una lista vacía en la cima de la tabla de símbolos 
    
    public void out(); 
    // Modifica: this 
    // Produce:  elimina la lista que está en la cima de la tabla de símbolos. 
    
    public boolean declare(String identifier, String type); 
    // Modifica: this 
    // Produce:  si el par (identifier, type) ya existe en la cima de la tabla de símbolos devuelve falso; en otro caso lo añade a la lista de la cima y devuelve verdadero. 
    
    public String get(String identifier);
    // Produce:  devuelve el tipo de la variable cuyo nombre es 'identifier' o 'NO_DECLARADO" si no se encuentra. Empieza a buscarlo a partir de la cima de la tabla de símbolos. 
}
```

Para implementar la interfaz `TSimbol` se ha decidido utilizar la siguiente clase cuya estructura de datos es una pila de listas de pares :

```java
public class TSimbolImp implements TSimbol { 
    private Stack<List<Pair>> table; 
} 

```

La clase `Pair` se muestra a continuación:

```java
 public class Pair { 
	 private String identifier, type; 
     
     public Par(String identifier, String type) {
		this.identifier = identifier; 
        this.type = type; 
     } 
     public String getIdentificador() { 
         return identifier; 
     } 
     public String getType() { 
         return type; 
     } 
 }
```

Se pide continuar con la implementación de la clase `TSimbolImp` escribiendo el código de las operaciones:

```java
public boolean declare(String identifier, String type); 
// Modifica: this 
// Produce:  si el par (identifier, type) ya existe en la lista de la cima de la Tabla de símbolos devuelve falso; en otro caso, lo añade a la lista de la cima y devuelve verdadero. 

public String consultar(String identifier); 
// Produce:  devuelve el tipo de la variable cuyo nombre es 'identifier' o 'NO_DECLARADO" si no se encuentra. Empieza a buscarlo a partir de la cima de la tabla de símbolos.
```



## Ejercicio 3 [Pila+Conjunto]

Dada la interfaz `Set<E>` :

```java
public interface Set<E> extends Iterable<E> { 
    public int size(); 
    public boolean contains(E e); 
    public void add(E e); 
    public void remove(E e); 
}
```

Implementada mediante la clase `ImpSet<E>` :

```java
public class ImpSet<E> implements Set<E> { 
    public ImpSet() // crea un conjunto vacío 
}
```

Y dada la interfaz `MultiSet<E>`:

```java
public interface MultiSet<E> { 
    public boolean containedInAllSets(E e); 
    // Produce: devuelve cierto si el elemento e está en todos los conjuntos. 
    
    public void removeFromAllSets(E e);
    // Modifica: this 
    // Produce: quita un elemento de todos los conjuntos de la pila. 
    
    public Set<E> moveAll(); 
    // Modifica: this 
    // Produce: Crea un único conjunto con todos los elementos de los conjuntos de la pila. 
    
    public void removeEmptySets(); 
    // Modifica: this 
    // Produce: quita todos los conjuntos vacíos de la pila. 
    
    public void addSet(); 
    // Modifica: this 
    // Produce: añade un conjunto vacío a la pila. 
    
    public void addElement(E e); 
    // Modifica: this 
    // Produce: añade un elemento a la cima de la pila. 
}
```

```

```

Esta última implementada mediante una `StackSet<E>`, es decir:

```java
public class ImpMultiSet<E> implements MultiSet<E> { 
    private Stack<Set<E>> sets; 
}
```



Se pide:

1. Implementar, haciendo uso de la estructura de datos indicada, la operación del TAD `Multiset<E>`:	

```java
public Set<E> moveAll()
```



2. Implementar, haciendo uso de la estructura de datos indicada, la operación del TAD `Multiset<E>`:	

```java
public void removeEmptySets()
```



## Ejercicio 4 

Un restaurante dispone de una carta, la cual se presenta como cola de platos . De cada plato se indica el nombre, precio y la pila de ingredientes que se emplean en su elaboración. De cada ingrediente se muestra el nombre, la cantidad que se usa en el plato y el coste.

Las clase `Dish` e `Ingredient` se muestran a continuación:

```java
public class Dish { 
    private String name; 
    private double price; 
    private Stack<Ingredient> ingredients; 
    
    public Dish (String name, double price, Stack<Ingredient> ingredients) { 
        this.name = name;
        this.price = price;
        this.ingredients = ingredients;
    } 
    public String getName() { 
        return this.name;
    }
    public double getPice() {
        return this.price;
    }
    public Stack<Ingredient> getIngredients() {
        return this.ingredients;
    } 
    public void setPrice(double price) {
        this.price = price;
    } 
    public void setIngredients(Stack<Ingrediente> ingredients) {
        this.ingredients = ingredients;
    }
}
```

```java
public class Ingredient { 
    private String name; 
    private int amount; 
    private double price; 
    
    public Ingredient(String name, int amount, double price) { 
        this.name = name; 
        this.amount = amount; 
        this.price = price; 
    } 
   public String getName() { 
        return this.name; 
    } 
    public int getAmount() { 
        return this.amount; 
    } 
    public double getPrice() { 
        return this.price;
    }
```

Debido a la subida de precios, el restaurante ha decidido modificar la carta de manera que va a **quitar de aquellos platos cuyo precio supere los 50€ el ingrediente utilizado en mayor cantidad (solo hay uno**). El nuevo precio del plato debe quedar reflejado en la carta.

Se pide Implementar el siguiente método:

```java
private static double deleteMostExpensiveIngredient(Stack<Ingredient> ingredients)
```



## Ejercicio 5 [Listas]

Una matriz dispersa es una matriz de gran tamaño en la que la mayor parte de sus elementos son cero. Para optimizar el almacenamiento de estas matrices en memoria se ha diseñado un TAD que solo almacena los valores distintos de cero. La interfaz de dicho TAD se muestra a continuación:

```java
public interface IntegerMatrix { 
    public int numFilas(); 
    // Produce: devuelve el número de filas de la matriz. public int numCols(); 
    // Produce: devuelve el número de columnas de la matriz. 
    
    public int recupera(int i, int j) throws IndexOutOfBoundsException; 
    // Produce: si i<=0 o i>n o j<=0 o j>m lanza la excepcion IndexOutOfBoundException en caso contrario devuelve el valor 	almacenado en la fila i, columna j.
    
    public void asigna(int i, int j, int nuevoValor) throws IndexOutOfBoundsException; 
    // Modifica: this 
    // Produce: si i<=0 o i>n o j<=0 o j>m lanza la excepcion IndexOutOfBoundException en caso contrario asigna nuevoValor en la 	posicion dada por la fila i, columna j. 
}
```

Para su implementación se va a utilizar una lista que contiene los números de fila con datos distintos de cero en la matriz y para cada fila se guarda una lista que contiene los pares número de columna y el valor distinto de cero almacenado en la matriz.

```pseudocode
Dada la matriz:												Se guardaría como:

1   2   0   0   3   4	0								1 → (1,1), (2,2), (5,3), (6,4) 
0   5   0   6   0   0	0								2 → (2,5), (4,6) 
0   7   8   9   0   0	0								3 → (2,7), (3,8), (4,9) 
1   0   0   2   0   0	0								4 → (1,1), (4,2) 
0   3   0   0   4   5	0								5 → (2,3), (5,4), (6,5) 
0   0   6   0   7   8	0								6 → (3,6), (5,7), (6,8) 
0   0   0   0   0   0   9								7 → (7,9)
```

La clase que implementa dicha interfaz se llama `IntegerMatrixList` , y se muestra a continuación:

```java
public class IntegerMatrixList implements IntegerMatrix { 
	private int numRows;
    private int numCols;
    private List<RowElement> rows; 
}
```

La clase `RowElement` se define como:

```java
public class RowElement { 
    private int row; 
    private List<ColumnElement> columns; 
    
    public RowElement(int row) { 
        this.row = row;
        this.columns = new LinkedList<>(); 
    }
    public int getRow() {
        return this.row;
    } 
    public List<ColumnElement> getColumnas() { 
        return this.columns; 
    } 
}
```

La clase `ColumnElement` se define como:

```java
public class ColumnElement { 
    private int column; 
    private int value; 
    
    public ColumnElement(int column, int  value) { 
        this.column = column; 
		this.value = value; 
	} 
    public int getColumn() { 
        return this.column; 
    } 
    public int getValue() { 
        return this.value; 
    } 
}
```

Se pide que, haciendo uso de la estructura de datos de la clase `IntegerMatrixList` , se implemente el método recupera de la interfaz `IntegerMatrix` .

```java
public int get(int i, int j) throws IndexOutOfBoundsException 
// Produce: si i<=0 o i>n o j<=0 o j>m lanza la excepcion IndexOutOfBoundException en caso contrario devuelve el valor almacenado en la fila i, columna j.
```



## Ejercicio 6 [Lista]

Un estudiante de informática pertenece a un club de baloncesto de su localidad y el presidente le ha pedido que diseñe una aplicación para el mantenimiento de los/as socios/as del club. El estudiante ha decidido definir una clase llamada `Suscriber` para almacenar la información de cada uno de los/as abonados/as al club, y un TAD llamado `Club` , que almacena un conjunto ordenado de abonados/as sin repetición. La clase `Suscriber` está disponible en el anexo.

```java
public interface Club extends Iterable<Suscriber> { 
    public boolean isEmpty(); 
    // Produce: cierto si el club no tiene abonados; falso, en caso contrario. 
    
    public int cardinal(); 
    // Produce: el número de abonados del club.
    
    public boolean isMember(Suscriber suscriber) throws NullPointerException; 
    // Produce: si abonado es null lanza una excepcion; en caso contrario, devuelve cierto si abonado 			pertenece al club; falso, en caso contrario. 
    
    public Suscriber get() throws ClubVacioException; 
    // Produce: lanza la excepción si el club está vacío; en otro caso, recupera un abonado cualquiera del 		club. 
    
    public boolean add(Suscriber suscriber) throws NullPointerException; 
    // Modifica: this 
    // Produce: si abonado es null lanza una excepcion; en otro caso, si abonado no está en el club lo añade 		y devuelve true; si ya es socio del club no hace nada y devuelve falso. 
    
    public boolean remove(Suscriber suscriber) throws NullPointerException; 
    // Modifica: this 
    // Produce: si abonado es null lanza una excepción; en otro caso, devuelve cierto si elimina el abonado 	abonado del club, falso en caso contrario. 
}
```

Se pide:

1. Haciendo uso de la interfaz anterior, la clase `Suscriber`, la interfaz `List<E>`y la clase `LinkedList<E>`; disponibles en el anexo, escribe el siguiente método:

   ```java
   public static List<Suscriber> getDelinquents(Club myClub) 
   // Produce: devuelve una lista con los abonados morosos del club.
   ```

   

2. Para implementar la interfaz `Club` se va a utilizar una estructura lineal enlazada simple con referencia al primer y último nodo de la estructura y sin centinela. Los abonados se guardarán en dicha estructura ordenados ascendentemente por número de abonado. 

   De esta clase se pide escribir **exclusivamente** la representación o **atributos** utilizados y el método `add()` especificado en la interfaz. Puedes hacer uso de la clase `Node<E>` del anexo.

```java
public class LinkedClub implements Club { 
    // atributos 
    // ...
    public boolean add(Suscriber suscriber) throws NullPointerException { 
    	// ...
    } 
}
```

**Importante** : si para implementar el método alta haces uso de algún otro método de la interfaz `Club` , debes implementarlo también.