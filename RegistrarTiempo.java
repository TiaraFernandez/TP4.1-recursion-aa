/***
 *  Clase para escribir los archivos de registro de tiempos de ejecución
*/

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class RegistrarTiempo {
    /* file */
    private BufferedWriter escritor;

    public RegistrarTiempo(String nombreArchivo){
        try {
            escritor = new BufferedWriter(new FileWriter(nombreArchivo, false));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void registrarTiempo(double n, long tiempo){
        try{
            escritor.write(n+","+tiempo);
            escritor.newLine();
        } catch (Exception e) {
           e.printStackTrace();
        }
    }

    public void finalizar(){
        try {
            escritor.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
