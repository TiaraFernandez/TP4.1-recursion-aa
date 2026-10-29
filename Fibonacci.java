/***
 * Ejercicio 1)1.a) del TP 4.1-Recurriones
 * Secuencia Fibonacci: F(n)= F(n-1) + F(n-2)
 * 
 * La clase tiene el metodo para calcular en n numero de la serie, una version iterativa y otra recursiva.
 * Además, registra los tiempos de ejecucion de ambos algoritmos.
*/

public class Fibonacci {
    public  static long tInicioRec, tFinRec, tInicioIt, tFinIt;
   
    /* Version ITERATIVA */
    public static int fibIterativo(int num){
        int resultado = -1;
        
        tInicioIt = System.nanoTime(); //* Registro el tiempo inicial en ns */
        if (num == 0 || num == 1) {
            resultado = num;
        }else if(num>1){
            int f1 = 0, f2 = 1;
            int actual = 0;

            for(int i=2; i<=num; i++){
                actual = f1+f2;
                f1 = f2;
                f2 = actual;
            }
            resultado = f2;
        }
        tFinIt = System.nanoTime(); //* Registro el tiempo final en ns */

        return resultado;    
    }

    /* Version RECURSIVA */
    public static int fibRecursivoAux(int num){
        int resultado;
        
        tInicioRec = System.nanoTime(); //* Registro el tiempo inicial en ns */
        resultado = fibRecursivo(num);
        tFinRec = System.nanoTime(); //* Registro el tiempo final en ns */

        return  resultado;
    }
    private static int fibRecursivo(int num){
        int resultado = -1;

        if (num == 0 || num == 1) {
            resultado = num;
        }else if(num>1){
            resultado = fibRecursivo(num-1) + fibRecursivo(num-2);
        }

        return  resultado;
    }
}
