import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * Created by Evelyn Li on 10/8/2017.
 */
public class locationGrader {
    public static void main(String[] args) {
        try{
            List<String> line = Files.readAllLines(Paths.get("locationGrading.txt"), StandardCharsets.UTF_8);
            HashMap<String, LinkedList<Float>> locationGrading = new HashMap<>();
            Scanner scanner = new Scanner(System.in);
            for(int i = 0; i<400; i++){
                String[] row = line.get(i).split(",");
                Float walkingGrade = Float.parseFloat(row[3]);
                Float cyclingGrade = Float.parseFloat(row[4]);
                LinkedList<Float> value = new LinkedList<>();
                value.add(walkingGrade);
                value.add(cyclingGrade);
                locationGrading.put(row[1]+row[2], value);
                System.out.print(row[1]+row[2]);
                System.out.print(value);
                System.out.println();
            }
        } catch (java.io.IOException e) {
            return;
        }
    }



}

