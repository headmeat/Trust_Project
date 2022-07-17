package trust.reliability;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;
import java.util.concurrent.TimeUnit;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.FileChannel.MapMode;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;

/*
 * All files must be located at Desktop.
 */

public class Merge {
	public static void main( String... args ) throws Exception
    {
		createRels("mergedFiles.txt", 11003);
		
		/*
		System.out.println(Arrays.toString(TwitterLookup.getUserName(new String[]{"807095",
				"30354991",
				"138203134",
				"759251",
				"2467791"})));*/
    }
	
	public static void insertNodes(String fileName, int portNo) throws Exception {
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/"+fileName));
		String t;
		
		try( Database greeter = new Database( "bolt://localhost:"+portNo, "neo4j", "1234" )) {
			String[] str_nodes = greeter.getNodes();
			long[] nodes = new long[str_nodes.length];
			long max_id = greeter.maxID()+1;
			List<Long> lst = new ArrayList<>();
			int cnt = 0;
			
			System.out.println("MAX_ID:"+max_id);
			
			for(int i=0;i<nodes.length;i++) {
				nodes[i] = Long.parseLong(str_nodes[i]);
			}
			
			Arrays.sort(nodes);

			while((t=br.readLine())!=null) {
				Long id = Long.parseLong(t.split(" ")[1]);
				
				if(Arrays.binarySearch(nodes, id)<0 && !lst.contains(id)) {
					cnt++;
					greeter.insertNodeB(max_id++, id);
					lst.add(id);
				}
			}
			System.out.println("Inserted "+cnt+" nodes.");
			br.close();
		}
	}
	
	public static void createRels(String fileName, int portNo) throws Exception {
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/"+fileName));
		String t;
		
		try( Database greeter = new Database( "bolt://localhost:"+portNo, "neo4j", "1234" )) {
			String[] str_nodes = greeter.getNodes();
			long[] nodes = new long[str_nodes.length];
			
			for(int i=0;i<str_nodes.length;i++) {
				nodes[i] = Long.parseLong(str_nodes[i]);
			}
			
			Arrays.sort(nodes);
			
			while((t=br.readLine())!=null) {
				String[] ids = t.split(" ");
				long first = Long.parseLong(ids[0]), second = Long.parseLong(ids[1]);
				
				if(Arrays.binarySearch(nodes, first)>=0 
						&& Arrays.binarySearch(nodes, second)>=0) {
					greeter.createRelB(first, second);
				}
			}
			
			br.close();
		}
	}
	
	public static void collectTweets() throws Exception {
		//String[] fnames = new String[] {"fashion.txt", "mergedFiles.txt"};	
		//mergeFiles(fnames, "mergedFiles2");
		/*
		CSVReader reader = new CSVReader(new FileReader("C:/Users/PC/Desktop/tweets_java.csv"));
		String[] lines;
		int cnt = 0;
		while((lines=reader.readNext())!=null) {
			for(String cell:lines) {
				System.out.print(cell+" ");
			}
			System.out.println();
			if(cnt++ == 10) break;
		}
		System.exit(0);
		*/
		CSVWriter csv = new CSVWriter(new FileWriter("C:/Users/PC/Desktop/tweets_java.csv"));
		//System.out.println(Arrays.toString(TwitterLookup.getFriends("939091")));
		//System.out.println(TwitterLookup.verifyID("939091"));
		
		csv.writeNext(new String[]{"userId", "created_at", "id", "text", "rt", "like", "reply", "quote"});
		
		try ( Database greeter = new Database( "bolt://localhost:11003", "neo4j", "1234" ) ){
			String[] nodes = greeter.getNodes();
			for(int i=0;i<nodes.length;i++) {
				nodes[i] = nodes[i].substring(1,nodes[i].length()-1);
				System.out.println("Processing, "+nodes[i]);
				//if(nodes[i].equals("136329115")) continue;
				TwitterLookup.getTweets(nodes[i], null, csv);
				System.out.println(i+" users processed.");
			}
		}

		//TwitterLookup.getTweets("939091", null, csv);
		//System.out.println(TwitterLookup.getTweets("939091", null, csv));
	}
	
	public static boolean mergeFiles(String[] fnames, String targetName) throws Exception {
		FileWriter fw = new FileWriter("C:/Users/PC/Desktop/"+targetName+".txt");
		
		for(String fname:fnames) {
			fname = "C:/Users/PC/Desktop/files/"+fname;
			String t;
			
			BufferedReader br = new BufferedReader(new FileReader(fname));
			
			while((t=br.readLine())!=null) fw.write(t+"\n");
			
			br.close();
		}
		
		fw.close();
		
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/"+targetName+".txt"));
		
		String t;
		
		while((t=br.readLine())!=null) {
			if(t.split(" ").length>2) {
				System.out.println(t);
				br.close();
				return false;
			}
		}
		
		br.close();
		return true;
	}
	
	public static void pickIds(String filename) throws Exception {
		int cnt = 0;
		filename = "C:/Users/PC/Desktop/"+filename+".txt";
		BufferedReader br = new BufferedReader(new FileReader(filename));
		HashSet<String> hash = new HashSet<String>();
		FileWriter fw = new FileWriter("C:/Users/PC/Desktop/topic/followers.txt");
		
		String t;
		
		while((t=br.readLine())!=null) {
			if((++cnt)%1000000==0) System.out.println(cnt);
			
			String[] ids = t.split(" ");

			//hash.add(ids[0]);
			hash.add(ids[1]);
		}
		
		System.out.println("Hash Size: "+hash.size());
		
		for(String item:hash) {
			fw.write(item+"\n");
		}
		
		br.close();
		fw.close();
	}
}
