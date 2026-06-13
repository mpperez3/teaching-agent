
public class Carta {

    private int numero;
    private String palo;

    public Carta(int numero, String palo) {
        this.numero = numero;
        this.palo = palo;
    }

    public int getNumero() {
        return this.numero;
    }

    public String getPalo() {
        return this.palo;
    }

    public boolean soyMayor(Carta c) {

        if (palo.compareTo(c.palo) > 0) {
            return true;
        } else {
            return (palo.compareTo(c.palo) == 0 && numero > c.numero);
        }

    }
}
