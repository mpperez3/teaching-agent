
import java.util.LinkedList;
import java.util.List;

public class Ejercicio1 {

    private static final int MAX_CANT = 501;

    public static List<Integer> getMasFrecuentes(int[] donaciones) {
        int[] contador = new int[MAX_CANT];
        for (int i : donaciones) {
            contador[i]++;
        }
        int numMaxDonaciones = contador[1];
        List<Integer> salida = new LinkedList<>();
        for (int donacion = 2; donacion < contador.length; donacion++) {
            if (contador[donacion] > numMaxDonaciones) {
                numMaxDonaciones = contador[donacion];
                salida = new LinkedList<>();
                salida.add(donacion);
            } else if (contador[donacion] == numMaxDonaciones) {
                salida.add(donacion);
            }
        }
        return salida;
    }

    public static void OrdSeleccion(List<Integer> donacionesMasFrec) {
        for (int i = 0; i < donacionesMasFrec.size() - 1; i++) {
            int posMayor = i;
            for (int j = 0; j < donacionesMasFrec.size() - i; j++) {
                if (donacionesMasFrec.get(j) > donacionesMasFrec.get(posMayor)) {
                    posMayor = j;
                }
            }
            int ultimaPos = donacionesMasFrec.size() - i - 1;
            if (posMayor != ultimaPos) {
                Integer temp = donacionesMasFrec.set(ultimaPos, donacionesMasFrec.get(posMayor));
                donacionesMasFrec.set(posMayor, temp);
            }
        }
    }
}
