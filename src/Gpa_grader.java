import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

/**
 * Created by Gary.G.Titor on 2017-10-08.
 */
public class Gpa_grader {
    public static void main(String[] args) {
        final int SAMPLE = 25000;
        ArrayList<Double> allgpa= new ArrayList<>();
        int k = 0;
        int i = 0;
        while (i<SAMPLE){
            //Random ran = new Random();
            //IntStream id = ran.ints(348486,378248);
            try {
                k += 1;
                int sec_num = 348486 + k;
                String id = "sections/" + Integer.toString(sec_num) + ".json";
                BufferedReader br = new BufferedReader(new FileReader(id));
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();
                while (line != null) {
                    sb.append(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }
                String everything = sb.toString();
                br.close();
                Parser b = new Parser(everything,"\"section_gpa\": ([0-9.]*)");
                b.find();
                double sec_gpa = Double.parseDouble((new ArrayList<String>(b.result)).get(0));
                allgpa.add(sec_gpa);
                i++;
            } catch (Exception a) {
                //do nothing here!
            }
        }
        double sum = 0.0;
        for (double gpa: allgpa){
            sum += gpa;
        }
        double ave = sum / SAMPLE;
        System.out.println(ave);
        double sumvar = 0.0;
        for (double gpa:allgpa){
            sumvar += Math.pow(gpa-ave,2);
        }
        double avevar = sumvar / SAMPLE;
        System.out.println(Math.sqrt(avevar));
    }
}
