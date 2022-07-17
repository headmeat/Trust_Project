package trust.reliability;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import com.opencsv.CSVReader;

public class Check {
	public static String checkCSV(String id, int i) throws FileNotFoundException, IOException {//csv �씫�뼱�꽌 id瑜� t_id濡� 諛붽퓭二쇰뒗 �뿭�븷
		//0: csv_id -> t_id, 1: t_id -> csv_id
		if(id==null) return null;

		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Downloads/twitter-2010-ids.csv"));//id �뙆�씪
		String t;
		
		while((t = br.readLine()) != null) {
			String[] s = t.split(",");
			
			if(id.equals(s[i]))
				return s[(i==1)?0:1];
		}
		
		return null;
	}
	
	public static String[] checkCSV(String[] csv_ids) throws IOException, FileNotFoundException {
		if(csv_ids==null) return null;
		
		BufferedReader br = new BufferedReader(new FileReader("C:/Users/PC/Downloads/twitter-2010-ids.csv"));//id �뙆�씪
		String t;
		List<String> csv_ids_ = new ArrayList<String>(Arrays.asList(csv_ids));
		int size = csv_ids_.size();
		String[] t_ids = new String[size];
		int fin_cnt = 0;
		
		while((t=br.readLine())!=null) {
			String[] ids = t.split(",");
			
			if(csv_ids_.contains(ids[0])) {
				t_ids[csv_ids_.indexOf(ids[0])] = ids[1];
				if(++fin_cnt == size) break;
			}
		}

		return t_ids;
	}
	
	public static String getNodeID(String id) throws FileNotFoundException {
		if(id==null)
			return null;
		
		Iterator iterator = new CSVReader(new FileReader("C:/Users/headm/Downloads/twitter-2010-ids.csv"), ',').iterator();
		
		while(iterator.hasNext()) {
			String[] s = (String[]) iterator.next();
			
			if(id.equals(s[1]))
				return s[0];
		}
		
		return null;
	}
}