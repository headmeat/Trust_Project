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
import java.util.stream.Collectors;

import org.json.JSONObject;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.FileChannel.MapMode;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;

/*
 * All files must be located at Desktop.
 * File name only for out2In without file extensions.
 */

public class Merge {
	public static void main( String... args ) throws Exception
    {
		filterCollect(new String[]{"for_god_sakes", "wahtahwt70686"}, "third");
    }
	
	public static void filterCollect(String[] prev, String curr) throws Exception {
		String t;
		HashSet<String> nodes;
		Set<String> set = new HashSet<>();
		
		for(int i=0;i<prev.length;i++) {
			BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/"+prev[i]+".csv"));
			System.out.println("reading "+(i+1)+"st file.");
			br.readLine();
			int cnt = 0;
			while((t=br.readLine())!=null) {
				cnt++;
				String id = t.split(",")[0];

				try {
					set.add(id.substring(1,id.length()-1));
				}catch(Exception e) {
					System.out.println(cnt);
				}
			}
			
			br.close();
		}
		
		System.out.println("Collected nodes count is "+set.size()+".");
		System.out.println("Start reading csv.");
		
		try( Database greeter = new Database( "bolt://localhost:11003", "neo4j", "1234" )) {
			nodes = new HashSet<>(Arrays.asList(greeter.getNodes()));
			int org = nodes.size();
			
			System.out.println("Before removing nodes: "+nodes.size());
			
			for(String node:set) {
				if(nodes.contains(node)) nodes.remove(node);
			}
			
			System.out.println("After removing nodes: "+nodes.size());
			System.out.println("Removed "+(org-nodes.size())+" nodes.");
		}
		/*
		String[] left_nodes = new String[nodes.size()];
		//Convert from hashset to arraylist.
		List<String> lst = new ArrayList<>(nodes);

		for(int i=0;i<lst.size();i++) {
			left_nodes[i] = lst.get(i);
		}
		*/
		System.out.println("About to collect "+nodes.size()+" nodes.");

		collectTweets(nodes.toArray(new String[0]), curr+new Random().nextInt(99999));
		//collectTweets(left_nodes, curr+new Random().nextInt(99999));
	}
	
	public static void createNodes(String fileName, int portNo) throws Exception {
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/csvs/"+fileName+".txt"));
		String t;
		
		try( Database greeter = new Database( "bolt://localhost:"+portNo, "neo4j", "1234" )) {
			Set<Long> nodes =  new HashSet<>();
			String[] str_nodes = greeter.getNodes();
			long max_id = greeter.maxID()+1;
			int cnt = 0;
			
			System.out.println("MAX_ID:"+max_id);
			
			System.out.println("str_nodes.length: "+str_nodes.length);
			
			for(int i=0;i<str_nodes.length;i++) {
				nodes.add(Long.parseLong(str_nodes[i]));
			}
			
			System.out.println("nodes.size(): "+nodes.size());
			
			while((t=br.readLine())!=null) {
				Long id = Long.parseLong(t.split(" ")[1]);
				
				if(!nodes.contains(id)) {
					if(cnt++%1000==0) System.out.println((cnt-1)+" users inserted.");
					greeter.insertNodeB(max_id++, id);
					nodes.add(id);
				}
			}
			
			System.out.println("Inserted "+cnt+" nodes.");
			br.close();
		}
	}
	
	//추가 검증 필요(사용 자제)
	public static void createNodes2(String fileName, int portNo) throws Exception {
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/"+fileName+".txt"));
		String t;
		
		try( Database greeter = new Database( "bolt://localhost:"+portNo, "neo4j", "1234" )) {
			long max_id = greeter.maxID()+1;
			int cnt = 0;
			
			System.out.println("MAX_ID:"+max_id);

			while((t=br.readLine())!=null) {
				Long id = Long.parseLong(t.split(" ")[0]);

				greeter.insertNodeB(max_id, id);
			}
			System.out.println("Inserted "+cnt+" nodes.");
			br.close();
		}
	}
	
	public static void createRels(String fileName, int start_at) throws Exception {
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/csvs/"+fileName+".txt"));
		String t;
		
		try( Database greeter = new Database( "bolt://localhost:"+11007, "neo4j", "1234" )) {
			String[] str_nodes = greeter.getNodes();
			Set<Long> nodes = new HashSet<>();
			
			
			int cnt = 0;
			
			for(int i=0;i<str_nodes.length;i++) {
				nodes.add(Long.parseLong(str_nodes[i]));
			}
			
			for(;cnt<start_at;cnt++) br.readLine();

			while((t=br.readLine())!=null) {
				String[] ids = t.split(" ");
				long first = Long.parseLong(ids[0]), second = Long.parseLong(ids[1]);
				
				if(cnt++ % 10000 == 0) System.out.println(cnt-1);
				
				if(nodes.contains(first)
						&& nodes.contains(second)) {
					greeter.createRelB(first, second);
				}
			}
			
			br.close();
		}
	}
	
	public static void addYears(String fileName) throws Exception {
		try( Database greeter = new Database( "bolt://localhost:11007", "neo4j", "1234" )) {
			String[] nodes = greeter.getNodesWO("year");
			
			System.out.println("Nodes length: "+nodes.length);
			
			TwitterLookup.getUsers(nodes, fileName);
		}
	}
	
	public static void collectTweets(int portNo, String fileName) throws Exception {
		CSVWriter csv = new CSVWriter(new FileWriter("C:/Users/PC/Desktop/"+fileName+".csv"));
		int cnt = 0;
		
		csv.writeNext(new String[]{"userId", "created_at", "id", "text", "rt", "like", "reply", "quote"});

		String[] nodes;
		
		try ( Database greeter = new Database( "bolt://localhost:"+portNo, "neo4j", "1234" ) ){
			nodes = greeter.getNodes();
		}
		
		for(int i=0;i<nodes.length;i++) {
			try {
				//nodes[i] = nodes[i].substring(1,nodes[i].length()-1);
				System.out.println("Processing, "+nodes[i]);

				TwitterLookup.getTweets(nodes[i], null, csv);
				if(cnt++%50 == 0) System.out.println(i+" users processed.");
			}catch(Exception e) {
				e.printStackTrace();
			}
		}
	}
	
	public static void collectTweets(String[] users, String fileName) throws Exception {
		CSVWriter csv = new CSVWriter(new FileWriter("C:/Users/PC/Desktop/"+fileName+".csv"));
		int cnt = 0;
		
		csv.writeNext(new String[]{"userId", "created_at", "id", "text", "rt", "like", "reply", "quote"});
		
		for(int i=0;i<users.length;i++) {
			try {
				//nodes[i] = nodes[i].substring(1,nodes[i].length()-1);
				System.out.println("Processing, "+users[i]);

				TwitterLookup.getTweets(users[i], null, csv);
				if(cnt++%50 == 0) System.out.println(i+" users processed.");
			}catch(Exception e) {
				e.printStackTrace();
			}
		}
	}
	
	public static boolean out2In(String fileName) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Desktop/"+fileName+".txt"));
		FileWriter fw = new FileWriter("C:/Users/PC/Desktop/"+fileName+"_reversed.txt");
		String t;int cnt = 0;
		
		try {
			while((t=br.readLine())!=null) {
				String[] ids = t.split(" ");
				if(cnt++%1000000==0) {
					System.out.println(cnt+" lines reversed/processed.");
					System.out.println(ids[0]+" "+ids[1]);
					fw.flush();
				}
				fw.write(ids[1]+" "+ids[0]+"\n");
			}

			fw.flush();
			br.close();fw.close();
			
			return true;
		}catch(Exception e) {
			e.printStackTrace();
			return false;
		}
	}
	
	public static boolean mergeFiles(String[] fnames, String targetName) throws Exception {
		FileWriter fw = new FileWriter("C:/Users/PC/Desktop/"+targetName+".txt");
		
		for(String fname:fnames) {
			fname = "C:/Users/PC/Desktop/"+fname+".txt";
			String t;
			int cnt = 0;
			
			BufferedReader br = new BufferedReader(new FileReader(fname));
			
			while((t=br.readLine())!=null) {
				fw.write(t+"\n");
				
				if(cnt++ % 1000000 == 0) System.out.println("Processed "+cnt+" lines.");
			}
			
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
