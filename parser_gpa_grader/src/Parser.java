import java.io.*;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLConnection;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by win8 on 2017/10/7.
 */

public class Parser {
    LinkedList<String> result;
    String source;
    String target;

    public Parser(String s, String targ) {
        source = s;
        target = targ;
        result = new LinkedList<>();
    }

    void find() {
        Pattern p = Pattern.compile(target);
        Matcher m = p.matcher(source);
        while (m.find()) {
            result.add(m.group(1));
        }
    }

    public static void main(String[] args) throws IOException, URISyntaxException{
        File f = new File("111.txt");
        FileInputStream fis = new FileInputStream(f);
        byte[] data = new byte[(int) f.length()];
        fis.read(data);
        fis.close();
        String s = new String(data, "UTF-8");

        Parser a = new Parser(s,"value=\"(\\d*)\"");
        a.find();
        Parser b = new Parser(s,"\"([A-Z- ,(&amp);\\/]+ [A-Z]*[0-9]+[A-Z]*)\"");
        b.find();
        HashMap<String,String> course_map = new HashMap<>();
        for (int i = 0; i< a.result.size();i++) {
            course_map.put(b.result.get(i),a.result.get(i));
        }
        String url = "https://www.berkeleytime.com/grades/course_grades/";
        HashMap<String,String> contents = new HashMap<>();
        for (int j = 0 ; j < b.result.size();j++) {
            String x = a.result.get(j);
            String address = url + x;
            URL u = new URL(address);
            URLConnection con = u.openConnection();
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream(),"UTF-8"));
            String sr = null;
            StringBuilder content = new StringBuilder();
            while ((sr = in.readLine()) != null) {
                content.append(sr);
            }
            if (in !=null) {
                in.close();
            }
            File out = new File("courses/"+x+".json");
            if (!out.exists()){
                out.createNewFile();
                FileWriter writer = new FileWriter(out);
                writer.write(content.toString());
                writer.flush();
                writer.close();
                contents.put(x,content.toString());
            }
        }
    }
}