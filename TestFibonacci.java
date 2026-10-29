import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class TestFibonacci {

    public static void main(String[] args) {
        List<Integer> numeros = generarNumerosDePrueba(0, 35, 10);

        calentarJVM();
        
        // Resgistro de tiempos de ejecución
        RegistrarTiempo registroIterativo = new RegistrarTiempo("tiempoFibIterativo.csv");
        RegistrarTiempo registroRecursivo =new RegistrarTiempo("tiempoFibRecursivo.csv");
        long tInicio, tFin;

        for (int n : numeros) {
            Fibonacci.fibIterativo(n);
            tInicio = Fibonacci.tInicioIt;
            tFin = Fibonacci.tFinIt;
            registroIterativo.registrarTiempo(n, tFin - tInicio);

            Fibonacci.fibRecursivoAux(n);
            tInicio = Fibonacci.tInicioRec;
            tFin = Fibonacci.tFinRec;
            registroRecursivo.registrarTiempo(n, tFin - tInicio);
        }

        registroIterativo.finalizar();
        registroRecursivo.finalizar();
    }

    // Se crea una lista con de numeros mesclados para realizar las pruebas
    private static List<Integer> generarNumerosDePrueba(int minimo, int maximo, int cantidadDeRepeticiones) {
        List<Integer> valores = new ArrayList<>();

        for (int ronda = 0; ronda < cantidadDeRepeticiones; ronda++) {
            List<Integer> rondaActual = new ArrayList<>();

            for (int n = minimo; n <= maximo; n++) {
                rondaActual.add(n);
            }

            Collections.shuffle(rondaActual);

            if (!valores.isEmpty()
                    && valores.get(valores.size() - 1).equals(rondaActual.get(0))
                    && rondaActual.size() > 1) {
                Collections.swap(rondaActual, 0, 1);
            }

            valores.addAll(rondaActual);
        }

        return valores;
    }

    private static void calentarJVM() {
        for (int repeticion = 0; repeticion < 10; repeticion++) {
            for (int n = 0; n <= 20; n++) {
                Fibonacci.fibIterativo(n);
                Fibonacci.fibRecursivoAux(n);
            }
        }
    }
}
