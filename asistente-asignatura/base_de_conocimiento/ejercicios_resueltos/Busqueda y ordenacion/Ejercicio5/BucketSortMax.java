
import java.util.LinkedList;
import java.util.List;


public class BucketSortMax {

    private static void selectionSortMax(List<Double> list) {
        for (int j = 0; j < list.size() - 1; j++) {
            int maxPosition = j;
            double valueMax = list.get(j);
//buscar el elemento mayor
            for (int k = j + 1; k < list.size(); k++) {
                if (list.get(k).compareTo(valueMax) > 0) {
                    maxPosition = k;
                    valueMax = list.get(k);
                }
            }
            if (maxPosition != j) {
                list.remove(valueMax);
                list.add(j, valueMax);
            }
        }
    }

    public static void bucketSortMax(double[] arr) {
// 1. Crear un array de listas (cubetas)
        List<Double>[] buckets = new LinkedList[arr.length];
        for (int i = 0; i < arr.length; i++) {
            buckets[i] = new LinkedList<>();
        }
// 2. Distribuir los elementos en cubetas
        for (double num : arr) {
            int index = (int) (arr.length - (num * arr.length)); // Asumiendo que num está entre 0 y 1
            buckets[index].addLast(num);
        }
// 3. Ordenar cada cubeta individualmente
        for (int i = 0; i < arr.length; i++) {
            selectionSortMax(buckets[i]);
        }
// ordenar el array
        int i = 0;
        for (List<Double> l : buckets) {
            for (Double elem : l) {
                arr[i++] = elem;
            }
        }
    }
}
