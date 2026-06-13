
import java.util.LinkedList;
import java.util.List;



public class MatrixSum {

    private static void selectionSort(List<ValueCol> list) {
        for (int j = 0; j < list.size() - 1; j++) {
            int minorPosition = j;
            ValueCol valueColMinor = list.get(j);
//buscar la columna menor
            for (int k = j + 1; k < list.size(); k++) {
                if (list.get(k).getColumn() < valueColMinor.getColumn()) {
                    minorPosition = k;
                    valueColMinor = list.get(k);
                }
            }
            if (minorPosition != j) {
                list.remove(valueColMinor);
                list.add(j, valueColMinor);
            }
        }
    }

    private static void allSort(List<ValueCol>[] aux) {
//ordeno todas las listas seleccionando el menor en cada momento
        for (int i = 0; i < aux.length; i++) {
            selectionSort(aux[i]);
        }
    }
//matrices cuadradas

    public static List<ValueCol>[] sum(List<ValueCol>[] matrix1, List<ValueCol>[] matrix2) {
        allSort(matrix1);
        allSort(matrix2);
        List<ValueCol>[] result = new List[matrix1.length];
//Añadimos la matriz 1 y luego modificamos
        for (int i = 0; i < result.length; i++) {
            result[i] = new LinkedList<>();
        }
        for (int i = 0; i < result.length; i++) {
            List<ValueCol> list1 = matrix1[i];
            List<ValueCol> list2 = matrix2[i];
            int index1 = 0;
            int index2 = 0;
            while (index1 < list1.size() && index2 < list2.size()) {
                if (list1.get(index1).getColumn() < list2.get(index2).getColumn()) {
                    result[i].addLast(list1.get(index1));
                    index1++;
                } else if (list1.get(index1).getColumn() > list2.get(index2).getColumn()) {
                    result[i].addLast(list2.get(index2));
                    index2++;
                } else {//son iguales
                    int sum = list1.get(index1).getValue() + list2.get(index2).getValue();
                    if (sum != 0) {
                        result[i].addLast(new ValueCol(list1.get(index1).getColumn(), sum));
                    }
                    index1++;
                    index2++;
                }
            }
            while (index1 < list1.size()) {
                result[i].addLast(list1.get(index1));
                index1++;
            }
            while (index2 < list2.size()) {
                result[i].addLast(list2.get(index2));
                index2++;
            }
        }
        return result;
    }
}
