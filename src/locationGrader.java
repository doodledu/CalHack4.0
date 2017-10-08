import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * Created by Evelyn Li on 10/8/2017.
 */
public class locationGrader {
    static HashMap<String, LinkedList<Float>> locationGrading = new HashMap<>();
    public static void main(String[] args) {
        try{
            List<String> line = Files.readAllLines(Paths.get("locationGrading.txt"), StandardCharsets.UTF_8);

            for(int i = 0; i<400; i++){
                String[] row = line.get(i).split(",");
                LinkedList<Float> value = new LinkedList<>();
                value.add(Float.parseFloat(row[3]));
                value.add(Float.parseFloat(row[4]));
                locationGrading.put(row[1]+row[2], value);
            }
        } catch (java.io.IOException e) {
            return;
        }
    }
    public Float getLocationGrading(String origin, String destination, String transportationType){
        if (transportationType.equals("walking")) {
            return locationGrading.get(origin+destination).get(0);
        } else if (transportationType.equals("cycling")) {
            return locationGrading.get(origin+destination).get(1);
        } else {
            return 0.0f;
        }
    }



}

