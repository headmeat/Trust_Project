package trust.reliability;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.FileChannel.MapMode;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;

public class Main2 {
	public static void main( String... args ) throws Exception
    {
		File file=new File("C:/Users/headm/Downloads/twitter-2010.txt");
		FileInputStream fr=new FileInputStream(file);   //reads the file
    	BufferedReader br=new BufferedReader(new InputStreamReader(fr));  //creates a buffering character input stream
    	FileInputStream fr2=new FileInputStream(file);   //reads the file
    	BufferedReader br2=new BufferedReader(new InputStreamReader(fr));
    	
    	fr.getChannel().position(0);
    	br = new BufferedReader(new InputStreamReader(fr));
    	
		Queue<String> follower = new LinkedList<>();//팔로워
		Queue<String> followee = new LinkedList<>();//팔로잉 당하는 사람
		
		try ( Database greeter = new Database( "bolt://localhost:7687", "neo4j", "1234" ) ){
			String[] test = greeter.getNodes();
			List<String> list = Arrays.asList(test);
	    	int c=0;
	    	String t;
	    	String[] ids;
	    	
			fr.getChannel().position(0);
	    	br = new BufferedReader(new InputStreamReader(fr));
	    	
			while((t=br.readLine())!=null)	{
				ids = t.split(" ");
				
				if((++c)%100000000==0)
					System.out.println("last while loop count: "+c);
				
				if(list.contains(ids[0])&&list.contains(ids[1]))
					greeter.createRel(ids[0], ids[1]);
			}
		}
    }
}