
import java.util.LinkedList;
import java.util.List;



public class Medium {

    private static void selectionSort(List<Float> list) {
        for (int j = 0; j < list.size() - 1; j++) {
            int minorPosition = j;
            Float valueMinor = list.get(j);
//buscar la columna menor
            for (int k = j + 1; k < list.size(); k++) {
                if (list.get(k).compareTo(valueMinor) < 0) {
                    minorPosition = k;
                    valueMinor = list.get(k);
                }
            }
            if (minorPosition != j) {
                list.remove(valueMinor);
                list.add(j, valueMinor);
            }
        }
    }

    public static List<Float>[] bucketSort(float[] arr) {
// 1. Crear un array de listas (cubetas)
        List<Float>[] buckets = new LinkedList[arr.length];
        for (int i = 0; i < arr.length; i++) {
            buckets[i] = new LinkedList<>();
        }
// 2. Distribuir los elementos en cubetas
        for (float num : arr) {
            int index = (int) (num * arr.length); // Asumiendo que num está entre 0 y 1
            buckets[index].addLast(num);
        }
// 3. Ordenar cada cubeta individualmente
        for (int i = 0; i < arr.length; i++) {
            selectionSort(buckets[i]);
        }
        return buckets; // Devolver array de listas ordenadas
    }

    public static float findMedium(float[] collection1, float[] collection2) {
        List<Float>[] arr1 = bucketSort(collection1);
        List<Float>[] arr2 = bucketSort(collection2);
        int i = 0, k = 0;
        int tam = collection1.length + 1;
        float[] merged = new float[tam];
        while (k < tam) {
            List<Float> list1 = arr1[i];
            List<Float> list2 = arr2[i];
            int index1 = 0;
            int index2 = 0;
// Fusionar los dos arrays en O(n)
            while (k < tam && index1 < list1.size() && index2 < list2.size()) {
                if (list1.get(index1) < list2.get(index2)) {
                    merged[k++] = list1.get(index1);
                    index1++;
                } else {
                    merged[k++] = list2.get(index2);
                    index2++;
                }
            }
// Agregar elementos restantes del primer array (si los hay)
            while (k < tam && index1 < list1.size()) {
                merged[k++] = list1.get(index1);
                index1++;
            }
// Agregar elementos restantes del segundo array (si los hay)
            while (k < tam && index2 < list2.size()) {
                merged[k++] = list2.get(index2);
                index2++;
            }
            i++;
        }
// Calcular la mediana, el tamaño de la suma de los dos arrays siempre será par
        return (merged[tam - 2] + merged[tam - 1]) / 2; // Promedio de los dos centrales
    }
}
