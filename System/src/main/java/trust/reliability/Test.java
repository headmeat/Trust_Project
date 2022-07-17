package trust.reliability;

import java.util.Arrays;
import java.util.LinkedList;
import java.io.FileWriter;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public class Test {
	public static void main(String[] args) throws Exception {
		//sports, music
		Queue<String> sports = new LinkedList<>(Arrays.asList(new String[]{"1108050829393707008", "173677727", "2279776304", "353178677", "4349708549", "23083404", "32453930", "28665877", "24485503", "173677727"})); 
		Queue<String> music = new LinkedList<>(Arrays.asList(new String[]{"154101116", "1852644804", "335141638", "816412233488015360", "16409683", "2150327072", "207923746", "34507480", "754006735468261376", "255388236"}));
		List<String> gizon = new ArrayList<String>();
		FileWriter fw = new FileWriter("sports.txt");
		
		int sports_cnt = 0;
		int music_cnt = 0;
		int cnt = 0;int prev = 0;
		
		while(!sports.isEmpty() ) {
			String id = sports.poll();
			System.out.println("Sports: "+id);
			gizon.add(id);
			String[] friends;boolean sw = true;
			
			while(sw) {
				try {
					friends = TwitterLookup.getFriends(id);
					
					if(cnt++ > 7000) {
						fw.close();
						System.out.println("Ending program since 7000 users following has been collected.");
						System.exit(0);
					}else if(cnt % 100 == 0) System.out.println(cnt+" users processed.");
					
					System.out.println(friends.length+" friends found for "+id);
					
					if(friends.length>0) {
						for(String friend:friends) {
							if(sports_cnt<5) {
								sports.add(friend);
								sports_cnt++;
							}
							
							fw.write(friend+" "+id+"\n");
						}
					}
					
					System.out.println();
					sports_cnt = 0;
					fw.flush();
					sw = false;prev = 0;
				}catch(Exception e) {
					prev++;
					if(prev == 2) {
						id = sports.poll();
						continue;
					}
					
					System.out.println("Exception occurred:\n");
					e.printStackTrace();
					System.out.println("Holding thread run till "+LocalDateTime.now().plusMinutes(15).plusSeconds(10));
					Thread.sleep(15 * 60 * 1000+10000);
				}
			}
		}
	}
}