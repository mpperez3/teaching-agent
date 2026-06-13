
public class Ejercicio2 {

    public void ordenar(Carta[] mano) {
        for (int pasada = 0; pasada < mano.length - 1; pasada++) {
            for (int j = 0; j < mano.length - pasada - 1; j++) {
                if (mano[j].soyMayor(mano[j + 1])) {
                    Carta c = mano[j + 1];
                    mano[j + 1] = mano[j];
                    mano[j] = c;
                }
            }
        }
    }
}
