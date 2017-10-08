import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;

/**
 * Created by Gary.G.Titor on 2017-10-08.
 */
public class Grader {
    public final double AVEGPA = 3.4372048399999757;
    public final double STDGPA = 0.35503200396665213;
    String course_name;
    String pro_name;
    double final_gpa;

    public static void main(String[] args){
     try{
        Grader frenkel = new Grader("PHYSICS 137B","MCKINSEY, D");
        System.out.println(frenkel.getgpa());
     } catch (Exception a){
         System.out.println("No This Class-Professor Combination");
     }
    }

    public Grader(String cname,String pname) {
        course_name = cname;
        pro_name = pname;
        String id = name_to_id(course_name);
        HashMap<String, Double> pro_avi = id_to_promap(id);
        final_gpa = pro_avi.get(pro_name);
    }

    public double getgpa(){
        return final_gpa;
    }

    private String name_to_id(String name){
        if(name.contains("&")){
            int k = name.indexOf("&");
            name = name.substring(0,k) + "&amp" + name.substring(k+1);
        }
        try {
            String ad = "map.txt";
            BufferedReader br = new BufferedReader(new FileReader(ad));
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = br.readLine();
            }
            String everything = sb.toString();
            br.close();
            Parser b = new Parser(everything," "+name+":(\\d*)");
            b.find();
            String id = (new ArrayList<String>(b.result)).get(0);
            return id;
        } catch (Exception a) {
            //do nothing here!
            return "";
        }
    }

    public HashMap<String,Double> id_to_promap(String id){
        String ad = "courses/" + id + ".json";
        try {
            BufferedReader br = new BufferedReader(new FileReader(ad));
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = br.readLine();
            }
            String everything = sb.toString();
            br.close();
            Parser a = new Parser(everything,"\"([A-Z -]*, [A-Z])\"");
            a.find();
            Parser b = new Parser(everything," \"grade_id\": (\\d*)");
            b.find();
            ArrayList<String> professors = new ArrayList<>(a.result);
            ArrayList<String> sections = new ArrayList<>(b.result);
            HashMap<String,LinkedList<String>> pro_sec = new HashMap<>();
            for (int i=0;i<professors.size();i++){
                String pro = professors.get(i);
                String sec = sections.get(i);
                if (!pro_sec.containsKey(pro)){
                    pro_sec.put(pro,new LinkedList<>());
                }
                pro_sec.get(pro).addLast(sec);
            }
            HashMap<String,Double> pro_avi = new HashMap<>();
            HashMap<Double,String> avi_pro = new HashMap<>();
            for (String pro:pro_sec.keySet()){
                LinkedList<String> seclist = pro_sec.get(pro);
                double av = 0.0;
                int num = 0;
                for (String sec:seclist){
                    av  +=  sec_to_gpa(sec);
                    num += 1;
                }
                double avi_gpa = av/num;
                pro_avi.put(pro,avi_gpa);
                avi_pro.put(avi_gpa,pro);
            }
            return pro_avi;
        } catch (Exception a){
            //do nothing here!
            return null;
        }
    }

    public double sec_to_gpa(String sec){
        try {
            String id = "sections/" + sec + ".json";
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
            double result = (sec_gpa-AVEGPA)/(2*STDGPA);
            return result;
        } catch (Exception a) {
            //do nothing here!
            return 0.0;
        }
    }
}
