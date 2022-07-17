package trust.reliability;

import org.json.JSONObject;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Record;
import org.neo4j.driver.Result;
import org.neo4j.driver.Session;
import org.neo4j.driver.Transaction;
import org.neo4j.driver.TransactionWork;
import java.io.*;
import java.util.Random;
import java.util.stream.Stream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import com.opencsv.*;
import static org.neo4j.driver.Values.parameters;

public class Database implements AutoCloseable
{
    private final Driver driver;

    public Database( String uri, String user, String password )
    {
        driver = GraphDatabase.driver( uri, AuthTokens.basic( user, password ) );
    }

    @Override
    public void close() throws Exception
    {
        driver.close();
    }
    
    public boolean checkRel(final String m, final String s)
    {
    	if((s==null)||(m==null))
    		return true;
    	
    	try( Session session = driver.session() )
    	{
    		String greeting = session.writeTransaction( new TransactionWork<String>() {
    			@Override
    			public String execute( Transaction tx )
    			{
    				Result result = tx.run("MATCH  (a:Node {id: $s}), (b:Node {id: $m}) RETURN EXISTS( (a)-[:FOLLOWS]->(b) )",
    						parameters("s", Integer.parseInt(s), "m", Integer.parseInt(m)));
    				
    				try {
    					return String.valueOf(result.single().get(0));
    				}catch(Exception e) {return null;}
    			}
    		});
    		
    		return greeting.equals("TRUE");
    	}catch(Exception e) {return false;}
    }
    
    public void insertNode(final String id, final String t_id)
    {
        try ( Session session = driver.session() )
        {
            String greeting = session.writeTransaction(new TransactionWork<String>()
            {
                @Override
                public String execute( Transaction tx )
                {
                    Result result = tx.run( "MERGE (n:Node {id:$id}) " +
                                                     "SET n.t_id = $t_id " +
                                                     "RETURN n.id + ', from node ' + id(n)",
                            //parameters("id", Integer.parseInt(id), "t_id", Integer.parseInt(t_id)));
                            parameters("id", id, "t_id", t_id));//09-26 Integer.parseInt(id) -> id
                    return result.single().get( 0 ).asString();
                }
            } );
            //System.out.println(greeting);
        }catch(Exception e) {
        	System.out.println("id/t_id:"+id+"/"+t_id);
        	e.printStackTrace();
        }
    }
    
    public void insertNodeB(final int id, final int t_id)
    {
        try ( Session session = driver.session() )
        {
            String greeting = session.writeTransaction(new TransactionWork<String>()
            {
                @Override
                public String execute( Transaction tx )
                {
                    Result result = tx.run( "MERGE (n:Node {id:$id}) " +
                                                     "SET n.t_id = $t_id " +
                                                     "RETURN n.id + ', from node ' + id(n)",
                            //parameters("id", Integer.parseInt(id), "t_id", Integer.parseInt(t_id)));
                            parameters("id", id, "t_id", t_id));//09-26 Integer.parseInt(id) -> id
                    return result.single().get( 0 ).asString();
                }
            } );
            //System.out.println(greeting);
        }catch(Exception e) {
        	System.out.println("id/t_id:"+id+"/"+t_id);
        	e.printStackTrace();
        }
    }
    
    public void insertNodeC(final int id)
    {
        try ( Session session = driver.session() )
        {
            String greeting = session.writeTransaction(new TransactionWork<String>()
            {
                @Override
                public String execute( Transaction tx )
                {
                    Result result = tx.run( "MERGE (n:Node {id:$id}) " +
                                                     "RETURN n.id + ', from node ' + id(n)",
                            //parameters("id", Integer.parseInt(id), "t_id", Integer.parseInt(t_id)));
                            parameters("id", id));//09-28 Integer.parseInt(id) -> id
                    return result.single().get( 0 ).asString();
                }
            } );
            //System.out.println(greeting);
        }catch(Exception e) {
        	System.out.println("id:"+id);
        	e.printStackTrace();
        }
    }
    
    public void createRel(final String m, final String s)//s:�뙏濡쒖썙 m:�뙏濡쒖슦 �릺�뒗 �옄
    {
    	try ( Session session = driver.session() ){
    		String greeting = session.writeTransaction( new TransactionWork<String>() {
    			@Override
    			public String execute( Transaction tx )
    			{
    				Result result = tx.run( "MATCH (a:Node {id:$s}) MATCH (b:Node {id:$m}) MERGE (a)-[:FOLLOWS]->(b)", parameters("s", s, "m", m) );
    				return s+"->"+m+" inserted.";
    			}
    		});
    		//System.out.println( greeting );
    	}
    }
    
    public void createRelB(final int m, final int s)//s:�뙏濡쒖썙 m:�뙏濡쒖슦 �릺�뒗 �옄
    {
    	try ( Session session = driver.session() ){
    		String greeting = session.writeTransaction( new TransactionWork<String>() {
    			@Override
    			public String execute( Transaction tx )
    			{
    				Result result = tx.run( "MATCH (a:Node {id:$s}) MATCH (b:Node {id:$m}) MERGE (a)-[:FOLLOWS]->(b)", parameters("s", s, "m", m) );
    				return s+"->"+m+" inserted.";
    			}
    		});
    		//System.out.println( greeting );
    	}
    }
    
    public int nodeCount() {
    	try ( Session session = driver.session() ){
    		String greeting = session.writeTransaction( new TransactionWork<String>() {
    			@Override
    			public String execute( Transaction tx )
    			{
    				Result result = tx.run( "MATCH (n:Node) RETURN COUNT(n)" );
    				
    				return String.valueOf(result.single().get(0));
    			}
    		});
    		return Integer.valueOf(greeting);
    	}
    }
    
    public boolean nodeExists(final String id) {
    	try ( Session session = driver.session() ){
    		String greeting = session.writeTransaction( new TransactionWork<String>() {
    			@Override
    			public String execute( Transaction tx )
    			{
    	    		String res="";
    				Result result = tx.run( "MATCH (n:Node {id:$id}) RETURN EXISTS(n.id)", parameters("id", Integer.parseInt(id)) );
    				
    				try {
    					return String.valueOf(result.single().get(0));
    				}catch(Exception e) {return null;}
    			}
    		});
    		
    		return greeting.equals("TRUE");
    	}catch(Exception e) {return false;}
    }
    
    public String[] getNodes() {
    	try ( Session session = driver.session() ){
    		String greeting = session.writeTransaction( new TransactionWork<String>() {
    			@Override
    			public String execute( Transaction tx )
    			{
    	    		String res="";
    				Result result = tx.run( "MATCH (n:Node) RETURN n.id" );
    				
    				while(result.hasNext()) {
    					res += result.next().get(0)+" "; //record를 다루는 법을 찾기 귀찮아서 그냥 이렇게 함.
    				}
    				
    				return res;
    			}
    		});
    		
    		return greeting.split(" ");
    	}
    }
    
    public int[] getNodesB() {
    	try ( Session session = driver.session() ){
    		String greeting = session.writeTransaction( new TransactionWork<String>() {
    			@Override
    			public String execute( Transaction tx )
    			{
    	    		String res="";
    	    		int cnt = 0;
    				Result result = tx.run( "MATCH (n:Node) RETURN n.id" );
    				
    				while(result.hasNext()) {
    					res += result.next().get(0)+" "; //record를 다루는 법을 찾기 귀찮아서 그냥 이렇게 함.
    				}
    				
    				return res;//this does not return to main since it's an anonymous function it returns to var. greeting.
    			}
    		});
    		
    		String[] cons = greeting.split(" ");
    		int len = cons.length;
    		int[] nums = new int[len];
    		
    		for(int i=0;i<len;i++) {
    			try {
    				nums[i] = Integer.parseInt(cons[i]);
    			}catch(Exception e) {
    				e.printStackTrace();
    				System.out.println(i);
    				System.out.println(cons[i]);
    				System.exit(0);
    			}
    		}
    		
    		return nums;
    	}
    }
    
    public String bSearch(String id) {
    	String line, line2, nb=null;
    	String[] ids = null;
    	int count = 0;
    	
    	File file=new File("C:/Users/headm/Downloads/twitter-2010.txt");
    	
    	try {
        	FileInputStream fr=new FileInputStream(file);   //reads the file
        	BufferedReader br=new BufferedReader(new InputStreamReader(fr));  //creates a buffering character input stream
        	FileInputStream fr2=new FileInputStream(file);   //reads the file
        	BufferedReader br2=new BufferedReader(new InputStreamReader(fr));
        	fr.getChannel().position(0);
        	br = new BufferedReader(new InputStreamReader(fr));
        	
        	//12 11 10
    		while((line = br.readLine())!=null) {
    			ids = line.split(" ");
    			count++;
    			if(count%10000000==0) System.out.println(count+": "+ids[0]+" "+ids[1]);

    			if(ids[0].equals(id)) {	//ids[1]->ids[0]
        			System.out.println("ID:"+id+" ids:"+ids[0]+" "+ids[1]);
        			if(!checkRel(ids[0], ids[1])) {
        				nb = ids[1];
        				insertNode(nb, Check.checkCSV(nb, 0));
        				createRel(id, nb);
        				
        				fr2.getChannel().position(0);
        				br2 = new BufferedReader(new InputStreamReader(fr2));
        				
        				while((line2=br2.readLine())!=null){	//ids[0]->ids[1]
        					if(Integer.parseInt(line2.split(" ")[1])>Integer.parseInt(ids[0])) {
        						break;
        					}
        					
        					if(line2.equals(ids[1]+" "+ids[0])) {
        						if(!checkRel(ids[1], ids[0])) {
        							createRel(ids[1], ids[0]);
            						break;
        						}
        					}
        				}
            			break;
        			}
    			}
    		}
    	}catch(Exception e) {}
    	return nb;
    }
    
    public String[] backtrack(String id) {
    	String nb=null, nb2=null;
    	System.out.println("id:"+id);
    	
    	if(id==null)
    		return new String[] {null, null};
    	
    	try
        {
    		insertNode(id, Check.checkCSV(id, 0));//백트랙 기준 첫 노드 삽입
    		
    		nb = bSearch(id);//1-hop 탐색
    		nb2 = bSearch(nb);//2-hop 탐색
    		
        }catch(Exception e) {e.printStackTrace();}
    	
    	return new String[]{nb, nb2};
    }
    
    public int twohops(int count, String id) {
    	String line, nb=null, nb2=null;
    	String[] ids=null;    	
    	
    	try
        {
        	File file=new File("C:/Users/headm/Downloads/twitter-2010.txt");    //Edge �뙆�씪
        	FileInputStream fr=new FileInputStream(file);   //reads the file
        	BufferedReader br=new BufferedReader(new InputStreamReader(fr));  //creates a buffering character input stream
        	fr.getChannel().position(0);
        	br = new BufferedReader(new InputStreamReader(fr));
        	
    		insertNode(id, Check.checkCSV(id, 0));
    		count++;
    		
    		do {
    			line = br.readLine();
    			ids = line.split(" ");
    			
    			if(ids[1].equals(id)) {
    				nb=ids[0];
    			}
    			System.out.println((Integer.parseInt(id)>=Integer.parseInt(ids[1]))+" "+checkRel(nb, id));
    		}while((Integer.parseInt(id)>=Integer.parseInt(ids[1]))&&(checkRel(nb, id)));
    		
    		if(nb==null) {//이게 역추적 사실
    			fr.getChannel().position(0);
            	br = new BufferedReader(new InputStreamReader(fr));
    			do {
    				ids = (String[])br.readLine().split(" ");
    				
    				if(ids[0].equals(id)) {
    					nb = ids[1];
    					if(!checkRel(id, nb)) {
    						createRel(id, nb);
    						break;
    					}
    				}
    			}while(Integer.parseInt(id)>=Integer.parseInt(ids[0]));
    		}
    		
    		count++;
    		
    		insertNode(nb, Check.checkCSV(nb, 0));
    		createRel(nb, id);
        	/*
        	do
        	{
        	line=br.readLine();//edge �뙆�씪 �븳 以� �뵫 �씫�쓬.
        	ids = line.split(" ");
        	
        	if(ids[0].equals(id)){//���긽 �씠�썐 以묒뿉 �씠�썐�씤 �냸�쓣 泥댄겕�븯�젮怨�(�븵�뮘 �닚�꽌 援щ퀎�쓣 紐삵븯�땲源�)
        		nb = ids[1];
        		System.out.println(ids[0]+" "+ids[1]);}
        	}while((TwitterLookup.verifyID(Check.checkCSV(nb)))||(nb==null)||(checkRel(id, nb)));//怨꾩젙 議댁옱 �솗�씤, id�옉 �뿰寃곕맂 �뿣吏� 嫄몃윭�깂.
        	
        	insertNode(nb, Check.checkCSV(nb));
        	createRel(ids[0], ids[1]);
        	
        	id = nb;
        	
        	fr.getChannel().position(0);
        	br = new BufferedReader(new InputStreamReader(fr));
        	
        	do
        	{
        	line=br.readLine();//edge �뙆�씪 �븳 以� �뵫 �씫�쓬.
        	ids = line.split(" ");
        	
        	if(ids[0].equals(id))//���긽 �씠�썐 以묒뿉 �씠�썐�씤 �냸�쓣 泥댄겕�븯�젮怨�(�븵�뮘 �닚�꽌 援щ퀎�쓣 紐삵븯�땲源�)
        		nb2 = ids[1];
        	}while((nb==null)||(checkRel(id, nb2)));

        	insertNode(nb2, Check.checkCSV(nb2));
        	createRel(ids[0], ids[1]);
        	
        	fr.getChannel().position(0);
        	br = new BufferedReader(new InputStreamReader(fr));
        	
        	count = twohops(count, nb);
        	*/
        	br.close();
        }catch(Exception e) {e.printStackTrace();}
        return count;
    	}
    }