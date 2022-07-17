package trust.reliability;

import org.json.*;

import com.opencsv.CSVWriter;

import java.io.FileWriter;
import java.io.IOException;
import java.net.URISyntaxException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.config.CookieSpecs;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

public class TwitterLookup {
	//김종훈꺼(밑에)
	//static String bearerToken = "AAAAAAAAAAAAAAAAAAAAANvzUQEAAAAAg4LLmBWA8ZgdMs%2FVe31SqfF%2FWV8%3DNjjRImreOHwckRHZjksr9NxG6rZXeKi9MAIS4Ksjz1IHWbKL20";
	//김상혁꺼(밑에)
	//static String bearerToken = "AAAAAAAAAAAAAAAAAAAAANWrUQEAAAAAM6NPSb%2BMgbXDTfRYOCLURqxSSV0%3DRYxmTtHwSAsv1EcLLFfgRYlC6u4DgdLV3kDq3EZ7hbbcGbUNfE";
	//내껄로 추정(밑에)
	//static String bearerToken = "AAAAAAAAAAAAAAAAAAAAAJGvLAEAAAAAc3bclYbPxNXFLaY%2FKIsTBKjn3eg%3DvearLoCZU7bQSHKZ77rKas66UynuNR0mYM89BdUSda3CwqsJLb";
	//SH 꺼(밑에)
	static String bearerToken =  "AAAAAAAAAAAAAAAAAAAAAFJoWQEAAAAAtGXgIPTy1xrcTE5sXcVLmRU1KZ8%3DgdvzO1icW2UsKz0r6srlwfN8Cbu1Cl6eYLLKrgQUmBpY01zG0O";
	static HashMap<String, String> hm = new HashMap<String, String>();//hm for user_id, generation_date
	static int count = 0;
	static HttpClient httpClient = HttpClients.custom()
	        .setDefaultRequestConfig(RequestConfig.custom()
	            .setCookieSpec(CookieSpecs.STANDARD).build())
	        .build();
	
	public static String[] getUserName(String[] ids) throws IOException, URISyntaxException {
	    String userResponse = null;

	    HttpClient httpClient = HttpClients.custom()
	        .setDefaultRequestConfig(RequestConfig.custom()
	            .setCookieSpec(CookieSpecs.STANDARD).build())
	        .build();

	    URIBuilder uriBuilder = new URIBuilder("https://api.twitter.com/2/users");
	    ArrayList<NameValuePair> queryParameters;
	    queryParameters = new ArrayList<>();
	    queryParameters.add(new BasicNameValuePair("ids", String.join(",", ids)));
	    queryParameters.add(new BasicNameValuePair("user.fields", "username"));
	    uriBuilder.addParameters(queryParameters);

	    HttpGet httpGet = new HttpGet(uriBuilder.build());
	    httpGet.setHeader("Authorization", String.format("Bearer %s", bearerToken));
	    httpGet.setHeader("Content-Type", "application/json");

	    HttpResponse response = httpClient.execute(httpGet);
	    HttpEntity entity = response.getEntity();
	    if (null != entity) {
	      userResponse = EntityUtils.toString(entity, "UTF-8");
	    }
	    
	    String[] ret = null;
	    
	    if(userResponse!=null) {
	    	JSONArray res = new JSONObject(userResponse).getJSONArray("data");
	    	ret = new String[res.length()];
	    	
			for(int i=0;i<res.length();i++) {
				ret[i] = res.getJSONObject(i).getString("username");
			}
	    }
	    
	    return ret;
	}
	
	public static boolean verifyID(String id) throws IOException, URISyntaxException {
		if(id==null)
			return false;
		
		String userResponse = null;
		JSONObject res;

		URIBuilder uriBuilder = new URIBuilder("https://api.twitter.com/2/users");
	    ArrayList<NameValuePair> queryParameters;
	    queryParameters = new ArrayList<>();
	    queryParameters.add(new BasicNameValuePair("ids", id));
	    queryParameters.add(new BasicNameValuePair("user.fields", "created_at,description,pinned_tweet_id"));
	    uriBuilder.addParameters(queryParameters);
	    
	    HttpGet httpGet = new HttpGet(uriBuilder.build());
	    httpGet.setHeader("Authorization", String.format("Bearer %s", bearerToken));
	    httpGet.setHeader("Content-Type", "application/json");
	    System.out.println(uriBuilder);
	    HttpResponse response = httpClient.execute(httpGet);
	    HttpEntity entity = response.getEntity();
	    if (null != entity) {
	      userResponse = EntityUtils.toString(entity, "UTF-8");
	    }
	    
		res = new JSONObject(userResponse);
		System.out.println(userResponse);
		
		try {
			if(res.getJSONArray("errors").getJSONObject(0).getString("title").equals("Not Found Error"))
				return false;
		}catch(Exception e) {System.out.println(res);}
		
		return true;
	}

	public static String[] getFriends(String id) throws Exception {
		System.out.println("Getting friends of "+id);
		String userResponse = null;
		String[] ret;
		
		URIBuilder uriBuilder = new URIBuilder("https://api.twitter.com/1.1/friends/ids.json");
	    ArrayList<NameValuePair> queryParameters;
	    queryParameters = new ArrayList<>();
	    queryParameters.add(new BasicNameValuePair("id", id));
	    queryParameters.add(new BasicNameValuePair("stringify_ids", "true"));
	    //queryParameters.add(new BasicNameValuePair("count", "100"));
	    //queryParameters.add(new BasicNameValuePair(""));
	    uriBuilder.addParameters(queryParameters);

	    HttpGet httpGet = new HttpGet(uriBuilder.build());
	    httpGet.setHeader("Authorization", String.format("Bearer %s", bearerToken));
	    httpGet.setHeader("Content-Type", "application/json");
	    
	    HttpResponse response = httpClient.execute(httpGet);
	    HttpEntity entity = response.getEntity();
	    
	    if (null != entity) userResponse = EntityUtils.toString(entity, "UTF-8");
	    else return null;
	    
	    //System.out.println(userResponse);
	    JSONArray res = null;
	    JSONObject obj = new JSONObject(userResponse);
	    System.out.println();
    	res = (JSONArray) obj.get("ids");
	    
	    ret = new String[res.length()];
	    Iterator<Object> iterator = res.iterator();
		int i=0;
		while(iterator.hasNext()) ret[i++] = (String) iterator.next();
		
		return ret;
	}
	
	public static String[] multiUsers(String[] ids) throws IOException, URISyntaxException {
		if(ids==null) return null;
		System.out.println("Running func. multiUsers(String[] ids)");
		
		String userResponse = null;
		String[] ret;
		
		if(ids.length>100) {//chunkify id list by 100, since API only allows 100 for each request.
			List<String> tmp = (List<String>)Arrays.asList(ids);
			List<String> result = new ArrayList<>();
			
			List<List<String>> chunked_tmp = chunkedLists(tmp, 100);
			
			for(List<String> lst:chunked_tmp) {
				String[] arr = lst.toArray(new String[0]);
				String[] test = multiUsers(arr);
				List<String> smth = null;
				
				if(test!=null) {
					smth = Arrays.asList(test);
				}
				
				if(smth!=null)	result.addAll(smth);
			}
			return result.toArray(new String[0]);
		}
		
		URIBuilder uriBuilder = new URIBuilder("https://api.twitter.com/2/users");
	    ArrayList<NameValuePair> queryParameters;
	    queryParameters = new ArrayList<>();
	    queryParameters.add(new BasicNameValuePair("ids", String.join(",", String.join(",", ids))));
	    queryParameters.add(new BasicNameValuePair("user.fields", "created_at,description,pinned_tweet_id"));
	    uriBuilder.addParameters(queryParameters);

	    HttpGet httpGet = new HttpGet(uriBuilder.build());
	    httpGet.setHeader("Authorization", String.format("Bearer %s", bearerToken));
	    httpGet.setHeader("Content-Type", "application/json");
	    
	    HttpResponse response = httpClient.execute(httpGet);
	    HttpEntity entity = response.getEntity();
	    
	    if (null != entity) userResponse = EntityUtils.toString(entity, "UTF-8");
	    else return null;
	    
	    //System.out.println(userResponse);
	    JSONArray res = null;
	    JSONObject obj = new JSONObject(userResponse);
	    
		try {
			res = obj.getJSONArray("data");//json 배열이 data랑 error 항목으로 구성돼서 data만 참고하면 없는 사용자를 참고하는 일은 없음.
			System.out.println(obj);
		}catch(Exception e) {
			System.out.println("<Exception>\n"+obj);
			//e.printStackTrace();
			return null;
		}
		
		ret = new String[res.length()];
		
		for(int i=0;i<res.length();i++) ret[i] = res.getJSONObject(i).getString("id");
		
		return ret;
	}
	
	public static <T> List<List<T>> chunkedLists(List<T> list, final int chunkSize) {

	  if (list == null) {
	   throw new IllegalArgumentException("Input list must not be null");
	  }

	  if (chunkSize <= 0) {
	   throw new IllegalArgumentException("Chunk Size must be > 0");
	  }

	  List<List<T>> subLists = new ArrayList<List<T>>();
	  final int listSize = list.size();
	  for (int i = 0; i < listSize; i += chunkSize) {
		  subLists.add(new ArrayList<T>(list.subList(i, Math.min(listSize, i + chunkSize))));
	  }
	  
	  return subLists;
	}
	
	public static String[] getUsers(String[] usernames, String fileName) throws IOException, URISyntaxException, InterruptedException {
	    String userResponse = null;
	    String[] ret;
	    FileWriter myWriter = new FileWriter("C:/Users/PC/Desktop/"+fileName+".txt");
	    HttpClient httpClient = HttpClients.custom()
	        .setDefaultRequestConfig(RequestConfig.custom()
	            .setCookieSpec(CookieSpecs.STANDARD).build())
	        .build();
	    
	    if(usernames.length>100) {//chunkify id list by 100, since API only allows 100 for each request.
			List<String> tmp = (List<String>)Arrays.asList(usernames);
			List<String> result = new ArrayList<>();
			
			List<List<String>> chunked_tmp = chunkedLists(tmp, 100);
			
			for(List<String> lst:chunked_tmp) {
				String[] arr = lst.toArray(new String[0]);
				System.out.println("Array: "+Arrays.toString(arr));
				String[] test = getUsers(arr, fileName);
				List<String> smth = null;
				
				if(test!=null) {
					smth = Arrays.asList(test);
				}else {
					test = getUsers(arr, fileName);
					if(test == null) continue;
				}
				
				if(smth!=null)	result.addAll(smth);
			}
			
			System.out.println("Printing hashmap.");
			System.out.println("Hashmap Size:"+hm.keySet().size());
			
			for(String key:hm.keySet()) {
				myWriter.write(key+" "+hm.get(key)+"\n");
			}
			
			myWriter.flush();
			myWriter.close();
			return result.toArray(new String[0]);
		}
	    
	    URIBuilder uriBuilder = new URIBuilder("https://api.twitter.com/2/users");
	    ArrayList<NameValuePair> queryParameters;
	    queryParameters = new ArrayList<>();
	    queryParameters.add(new BasicNameValuePair("ids", String.join(",", String.join(",", usernames))));
	    queryParameters.add(new BasicNameValuePair("user.fields", "created_at,description,pinned_tweet_id"));
	    uriBuilder.addParameters(queryParameters);

	    HttpGet httpGet = new HttpGet(uriBuilder.build());
	    httpGet.setHeader("Authorization", String.format("Bearer %s", bearerToken));
	    httpGet.setHeader("Content-Type", "application/json");

	    HttpResponse response = httpClient.execute(httpGet);
	    HttpEntity entity = response.getEntity();
	    if (null != entity) {
	      userResponse = EntityUtils.toString(entity, "UTF-8");
	    }else return null;
	    
	    JSONArray res = null;
	    JSONObject obj = new JSONObject(userResponse);
	    System.out.println(obj);
		try {
			res = obj.getJSONArray("data");//json 배열이 data랑 error 항목으로 구성돼서 data만 참고하면 없는 사용자를 참고하는 일은 없음.
		}catch(Exception e) {
			e.printStackTrace();
			System.out.println("OBJ:");
			System.out.println(obj);
			Thread.sleep(15*60*1000+1000);
			return null;
		}
		
		ret = new String[res.length()];
		
		for(int i=0;i<res.length();i++) {
			String date = res.getJSONObject(i).getString("created_at").substring(0, 4);
			hm.put(res.getJSONObject(i).getString("id"), date);
			ret[i] = date;
		}

		return ret;
	  }

	public static String getTweets2(String userId) throws IOException, URISyntaxException {
	    //return created_dates of userId
		String tweetResponse = null;

	    HttpClient httpClient = HttpClients.custom()
	        .setDefaultRequestConfig(RequestConfig.custom()
	            .setCookieSpec(CookieSpecs.STANDARD).build())
	        .build();

	    URIBuilder uriBuilder = new URIBuilder(String.format("https://api.twitter.com/2/users/%s/tweets", userId));
	    ArrayList<NameValuePair> queryParameters;
	    queryParameters = new ArrayList<>();
	    queryParameters.add(new BasicNameValuePair("tweet.fields", "created_at"));
	    uriBuilder.addParameters(queryParameters);

	    HttpGet httpGet = new HttpGet(uriBuilder.build());
	    httpGet.setHeader("Authorization", String.format("Bearer %s", bearerToken));
	    httpGet.setHeader("Content-Type", "application/json");

	    HttpResponse response = httpClient.execute(httpGet);
	    HttpEntity entity = response.getEntity();
	    if (null != entity) {
	      tweetResponse = EntityUtils.toString(entity, "UTF-8");
	    }
	    return tweetResponse;
	  }
	
	public static String getTweets(String userId, String nextToken, CSVWriter csv) throws IOException, URISyntaxException, InterruptedException {
	    String tweetResponse = null;
	    boolean sw = false;
	    //FileWriter fw = new FileWriter("tweets_java.csv");
	    //CSVWriter csv = new CSVWriter(new FileWriter("C:/Users/PC/Desktop/tweets_java.csv"));
	    
	    HttpClient httpClient = HttpClients.custom()
	        .setDefaultRequestConfig(RequestConfig.custom()
	            .setCookieSpec(CookieSpecs.STANDARD).build())
	        .build();

	    URIBuilder uriBuilder = new URIBuilder(String.format("https://api.twitter.com/2/users/%s/tweets", userId));
	    ArrayList<NameValuePair> queryParameters;
	    queryParameters = new ArrayList<>();
	    queryParameters.add(new BasicNameValuePair("max_results", "100"));
	    /*
	    queryParameters.add(new BasicNameValuePair("start_time", "2021-08-09T00:00:00Z"));
	    queryParameters.add(new BasicNameValuePair("end_time", "2021-11-09T00:00:00Z"));*/
	    queryParameters.add(new BasicNameValuePair("start_time", "2021-09-04T00:00:00Z"));
	    queryParameters.add(new BasicNameValuePair("end_time", "2021-12-04T00:00:00Z"));
	    queryParameters.add(new BasicNameValuePair("tweet.fields", "created_at,public_metrics"));
	    queryParameters.add(new BasicNameValuePair("exclude", "replies"));
	    //queryParameters.add(new BasicNameValuePair("user.fields", "id,username"));
	    if(nextToken!=null) queryParameters.add(new BasicNameValuePair("pagination_token", nextToken));
	    
	    uriBuilder.addParameters(queryParameters);

	    HttpGet httpGet = new HttpGet(uriBuilder.build());
	    httpGet.setHeader("Authorization", String.format("Bearer %s", bearerToken));
	    httpGet.setHeader("Content-Type", "application/json");
	    
	    while(true) {
		    HttpResponse response = httpClient.execute(httpGet);
		    HttpEntity entity = response.getEntity();
		    if (null != entity) {
		      tweetResponse = EntityUtils.toString(entity, "UTF-8");
		    }
		    //System.out.println(new JSONObject(tweetResponse).getJSONArray("data").getJSONObject(0).getJSONObject("public_metrics").getInt("retweet_count"));
		    
		    JSONArray res = null;
		    JSONObject obj = new JSONObject(tweetResponse);

			try {
				if(obj.getJSONObject("meta").getInt("result_count")==0) return null; //no tweets
				res = obj.getJSONArray("data");//json 배열이 data랑 error 항목으로 구성돼서 data만 참고하면 없는 사용자를 참고하는 일은 없음.
			}catch(Exception e) {
				if(obj.has("errors")) {
					String tmp = (String)((JSONObject)obj.getJSONArray("errors").get(0)).get("detail");
					
					if(((tmp.equals("Sorry, you are not authorized to see the user with id: ["+userId+"].")
							|| tmp.equals("Could not find user with id: ["+userId+"].")
							|| tmp.equals("User has been suspended: ["+userId+"].")))) return null;
				}

				System.out.print("tweetResponse: ");
				System.out.println(obj);

				if(sw == false) {
					System.out.println("Thread sleeps until "+LocalDateTime.now().plusMinutes(15).plusSeconds(10));
					Thread.sleep(15*60*1000+1000);
				}
				else return null;
				
				sw = true;
			}
			
			System.out.println(res.length());

			for(int i=0;i<res.length();i++) {
				JSONObject object = res.getJSONObject(i);
				JSONObject metrics = object.getJSONObject("public_metrics");
				
				csv.writeNext(new String[]{userId,object.getString("created_at"),object.getString("id"),object.getString("text").replaceAll("[\\n\\t,]", "").replaceAll(",", " "),String.valueOf(metrics.getInt("retweet_count")),String.valueOf(metrics.getInt("like_count")),String.valueOf(metrics.getInt("reply_count")),String.valueOf(metrics.getInt("quote_count"))});
			}
			
			csv.flush();
			
			//fetch next token for pagination.
			try{nextToken = obj.getJSONObject("meta").getString("next_token");}
			catch(Exception e) {return null;}
			
			if(nextToken!=null) getTweets(userId, nextToken, csv);
		    return null;
	    }
	  }
}
