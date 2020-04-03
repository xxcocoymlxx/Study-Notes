package com.csc301.profilemicroservice;

import org.apache.tomcat.util.json.JSONParser;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.csc301.profilemicroservice.Utils;
import com.fasterxml.jackson.databind.ObjectMapper;

import okhttp3.Call;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("/")
public class ProfileController {
	public static final String KEY_USER_NAME = "userName";
	public static final String KEY_USER_FULLNAME = "fullName";
	public static final String KEY_USER_PASSWORD = "password";

	@Autowired
	private final ProfileDriverImpl profileDriver;

	@Autowired
	private final PlaylistDriverImpl playlistDriver;
	
	private String regex = "^[a-zA-Z0-9]+$";
	private Pattern pattern = Pattern.compile(regex);

	OkHttpClient client = new OkHttpClient();

	public ProfileController(ProfileDriverImpl profileDriver, PlaylistDriverImpl playlistDriver) {
		this.profileDriver = profileDriver;
		this.playlistDriver = playlistDriver;
	}

	@RequestMapping(value = "/profile", method = RequestMethod.POST)
	public @ResponseBody Map<String, Object> addProfile(@RequestParam Map<String, String> params,
			HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("POST %s", Utils.getUrl(request)));

		//if params has all required info, get info from params and call createUserProfile
		String userName = params.get("userName");
		String fullName = params.get("fullName");
		String password = params.get("password");
		System.out.println("password is: ".concat(password));
		if (userName != null && fullName != null && password != null){
			if (userName.equals("") || password.equals("")) {
				response.put("message", "BAD REQUEST: missing parameter");
				response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
				return response;
			}
			DbQueryStatus status = this.profileDriver.createUserProfile(userName, fullName, password);
			//set response body depending on status
			response.put("message", status.getMessage());
			response = Utils.setResponseStatus(response, status.getdbQueryExecResult(), status.getData());
		}
		else{
			response.put("message", "BAD REQUEST: missing parameter");
			response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
		}

		return response;
	}

	@RequestMapping(value = "/followFriend/{userName}/{friendUserName}", method = RequestMethod.PUT)
	public @ResponseBody Map<String, Object> followFriend(@PathVariable("userName") String userName,
			@PathVariable("friendUserName") String friendUserName, HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("PUT %s", Utils.getUrl(request)));
		DbQueryStatus status = this.profileDriver.followFriend(userName, friendUserName);
		response.put("message", status.getMessage());
		response = Utils.setResponseStatus(response, status.getdbQueryExecResult(), status.getData());
		return response;
	}


	@RequestMapping(value = "/getAllFriendFavouriteSongTitles/{userName}", method = RequestMethod.GET)
	public @ResponseBody Map<String, Object> getAllFriendFavouriteSongTitles(@PathVariable("userName") String userName,
			HttpServletRequest request) {
		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("PUT %s", Utils.getUrl(request)));

		//get the map of friend's usernames and their list of fav song ids from neo4j
		DbQueryStatus status = this.profileDriver.getAllSongFriendsLike(userName);

		if (status.getdbQueryExecResult()!=DbQueryExecResult.QUERY_OK) {

			response.put("message", status.getMessage());
			Utils.setResponseStatus(response, status.getdbQueryExecResult(), status.getData());
			return response;

		}else {
			Map<String,List<String>> frendsLikeSongIDs = (Map<String, List<String>>) status.getData();
			Iterator<Map.Entry<String, List<String>>>  frendsLikeSongIDsIterator = frendsLikeSongIDs.entrySet().iterator(); 

			//HashMap of friend's usernames and their fav song's TITLEs
			Map<String,List<String>> responseData = new HashMap<String,List<String>>(); 

			while(frendsLikeSongIDsIterator.hasNext())
			{ 
				Map.Entry<String, List<String>> entry = frendsLikeSongIDsIterator.next(); 
				String friendUsername = entry.getKey();  
				List<String> songIDs = entry.getValue();

				List<String> songTitles = new ArrayList<String>();

				for (int i = 0; i < songIDs.size(); i++) {
					String songID = songIDs.get(i);

					//compose the new url (song-microservice runs on PORT 3001)
					HttpUrl.Builder getSongTitleUrlBuilder = HttpUrl.parse("http://localhost:3001" + "/getSongTitleById/" + songID).newBuilder();
					String getSongTitleUrl = getSongTitleUrlBuilder.build().toString();

					Request getSongTitleRequest = new Request.Builder()
							.url(getSongTitleUrl)
							.method("GET",null)
							.build();

					//make the client call to song-Service
					Call getSongTitleCall = client.newCall(getSongTitleRequest);

					Response responseFromGetSongTitleCall = null;
					String getSongTitleBodyString = "{}";
					try {
						//send the request, the response body will be returned
						responseFromGetSongTitleCall = getSongTitleCall.execute();

						//get the response body
						getSongTitleBodyString = responseFromGetSongTitleCall.body().string();
						JSONObject getSongBodyJson = new JSONObject(getSongTitleBodyString);
						String getSongQueryMessage = (String) getSongBodyJson.get("message");

						if(getSongQueryMessage.equals("found song")) {
							String songTitle = (String) getSongBodyJson.get("data");
							if (songTitle != null) {
								songTitles.add(songTitle);
							}else {
								//found the song but somehow the song title is null
								songTitles.add("song exists in mongoDB but the title is null");
							}

						}else {
							songTitles.add("song DNE in mongoDB");
							//response.put("message", "song does not exist in mongoDB");
							//response.put("status", HttpStatus.NOT_FOUND);
							//return response;
						}
					} catch (IOException e) {
						e.printStackTrace();
					}
				}//for loop of songIDs ends
				responseData.put(friendUsername, songTitles);
			}//while ends
			response.put("data", responseData);
			response.put("status",HttpStatus.OK);
			response.put("message", status.getMessage());
		} //else: queryStatus == OK ends

		return response;
	}


	@RequestMapping(value = "/unfollowFriend/{userName}/{friendUserName}", method = RequestMethod.PUT)
	public @ResponseBody Map<String, Object> unfollowFriend(@PathVariable("userName") String userName,
			@PathVariable("friendUserName") String friendUserName, HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("PUT %s", Utils.getUrl(request)));
		DbQueryStatus status = this.profileDriver.unfollowFriend(userName, friendUserName);
		response.put("message", status.getMessage());
		response = Utils.setResponseStatus(response, status.getdbQueryExecResult(), status.getData());
		return response;
	}

	//need song-microservice
	@RequestMapping(value = "/likeSong/{userName}/{songId}", method = RequestMethod.PUT)
	public @ResponseBody Map<String, Object> likeSong(@PathVariable("userName") String userName,
			@PathVariable("songId") String songId, HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("PUT %s", Utils.getUrl(request)));
		
		//check if songId is alphanumerical
		Matcher matcher = pattern.matcher(songId);
		if (songId.equals("") || songId.length() != 24 || !matcher.matches()) {
			response.put("message", "invalid songID");
			response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
			return response;
		}

		//like the song in mongoDB first
		//Check if the song exists in mongodb. 
		//If no, return an error directly. If yes, proceed to like the song in mongo and neo4j. 

		//compose the new url (song-microservice runs on PORT 3001)
		HttpUrl.Builder getSongUrlBuilder = HttpUrl.parse("http://localhost:3001" + "/getSongById/" + songId).newBuilder();
		String getSongUrl = getSongUrlBuilder.build().toString();

		//the actual "request" object, which contains url and request body
		Request getSongRequest = new Request.Builder()
				.url(getSongUrl)
				.method("GET",null)
				.build();

		//make the client call to song-Service
		Call getSongCall = client.newCall(getSongRequest);

		Response responseFromGetSongCall = null;
		String getSongBodyString = "{}";
		try {
			//send the request，the response body will be returned
			responseFromGetSongCall = getSongCall.execute();

			//get the response body
			getSongBodyString = responseFromGetSongCall.body().string();
			JSONObject getSongBodyJson = new JSONObject(getSongBodyString);
			String getSongQueryMessage = (String) getSongBodyJson.get("message");

			if (getSongQueryMessage.equals("no song found")){

				response.put("message", "song does not exist in mongoDB");
				response.put("status", HttpStatus.NOT_FOUND);

			}else { //song exists in mongoDB, proceed to like the song in neo4j
				DbQueryStatus status = this.playlistDriver.likeSong(userName, songId);

				//song in neo4j has already been liked
				if (status.getdbQueryExecResult()!=DbQueryExecResult.QUERY_OK) {

					response = Utils.setResponseStatus(response, status.getdbQueryExecResult(), status.getData());

				}else {//status.getdbQueryExecResult() == OK

					if (status.getMessage().equals("song already liked")) {
						//song already liked in neo4j
						response.put("message", "song already liked");
						response.put("status", HttpStatus.OK);	
						return response;
					}else {
						//song liked in neo4j, proceed to increment favCount in mongoDB
						HttpUrl.Builder updateFavCountUrlBuilder = HttpUrl.parse("http://localhost:3001" + "/updateSongFavouritesCount/" + songId).newBuilder();
						updateFavCountUrlBuilder.addQueryParameter("shouldDecrement", "false");
						String updateFavCountUrl = updateFavCountUrlBuilder.build().toString();

						RequestBody updateFavCountRequestBody = RequestBody.create(null, new byte[0]);

						//the actual "request" object, which contains url and request body
						Request updateFavCountRequest = new Request.Builder()
								.url(updateFavCountUrl)
								.method("PUT",updateFavCountRequestBody)
								.build();

						//make the client call to song-Service
						Call updateFavCountCall = client.newCall(updateFavCountRequest);

						Response responseFromUpdateFavCount = null;
						String updateFavCountBody = "{}";
						try {
							//send the request，the responde body will be returned
							responseFromUpdateFavCount = updateFavCountCall.execute();

							//get the response body
							updateFavCountBody = responseFromUpdateFavCount.body().string();
							JSONObject updateFavCountBodyJson = new JSONObject(updateFavCountBody);
							String updateFavCountQueryMessage = (String) updateFavCountBodyJson.get("message");

							if (updateFavCountQueryMessage.equals("songAmountFavourites updated")){

								response.put("message", "song liked in both neo4j and mongoDB");
								response.put("status", HttpStatus.OK);	

							}else if (updateFavCountQueryMessage.equals("invalid songID")){
								response.put("message", "invalid songID");
								response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
							}else {
								response.put("message", "unkown error");
								response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
							}

						} catch (IOException e) {
							e.printStackTrace();
						}
					}
				}
			}
		}catch  (IOException e) {
			e.printStackTrace();
		}

		return response;
	}

	//need song-microservice, decrement the favorites counter in song
	@RequestMapping(value = "/unlikeSong/{userName}/{songId}", method = RequestMethod.PUT)
	public @ResponseBody Map<String, Object> unlikeSong(@PathVariable("userName") String userName,
			@PathVariable("songId") String songId, HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("PUT %s", Utils.getUrl(request)));
		
		//check if songId is alphanumerical
		Matcher matcher = pattern.matcher(songId);
		if (songId.equals("") || songId.length() != 24 || !matcher.matches()) {
			response.put("message", "invalid songID");
			response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
			return response;
		}

		//like the song in mongoDB first
		//Check if the song exists in mongodb. 
		//If no, return an error directly. If yes, proceed to unlike the song in mongo and neo4j. 

		//compose the new url (song-microservice runs on PORT 3001)
		HttpUrl.Builder getSongUrlBuilder = HttpUrl.parse("http://localhost:3001" + "/getSongById/" + songId).newBuilder();
		String getSongUrl = getSongUrlBuilder.build().toString();

		//the actual "request" object, which contains url and request body
		Request getSongRequest = new Request.Builder()
				.url(getSongUrl)
				.method("GET",null)
				.build();

		//make the client call to song-Service
		Call getSongCall = client.newCall(getSongRequest);

		Response responseFromGetSongCall = null;
		String getSongBodyString = "{}";
		try {
			//send the request，the response body will be returned
			responseFromGetSongCall = getSongCall.execute();

			//get the response body
			getSongBodyString = responseFromGetSongCall.body().string();
			JSONObject getSongBodyJson = new JSONObject(getSongBodyString);
			String getSongQueryMessage = (String) getSongBodyJson.get("message");

			if (getSongQueryMessage.equals("no song found")){

				response.put("message", "song does not exist in mongoDB");
				response.put("status", HttpStatus.NOT_FOUND);

			}else { //song exists in mongoDB, proceed to unlike the song in neo4j
				DbQueryStatus status = this.playlistDriver.unlikeSong(userName, songId);


				if (status.getdbQueryExecResult()!=DbQueryExecResult.QUERY_OK) {

					response = Utils.setResponseStatus(response, status.getdbQueryExecResult(), status.getData());

				}else {

					//song in neo4j has already been unliked
					if (status.getMessage().equals("song was not liked to begin with")) {
						//song already unliked in neo4j, shuold not decrement fav count
						response.put("message", "song was not liked to begin with");
						response.put("status", HttpStatus.OK);	
						return response;
					}else {

						//song unliked in neo4j, proceed to decrement favCount in mongoDB
						HttpUrl.Builder updateFavCountUrlBuilder = HttpUrl.parse("http://localhost:3001" + "/updateSongFavouritesCount/" + songId).newBuilder();
						updateFavCountUrlBuilder.addQueryParameter("shouldDecrement", "true");
						String updateFavCountUrl = updateFavCountUrlBuilder.build().toString();

						RequestBody updateFavCountRequestBody = RequestBody.create(null, new byte[0]);

						//the actual "request" object, which contains url and request body
						Request updateFavCountRequest = new Request.Builder()
								.url(updateFavCountUrl)
								.method("PUT",updateFavCountRequestBody)
								.build();

						//make the client call to song-Service
						Call updateFavCountCall = client.newCall(updateFavCountRequest);

						Response responseFromUpdateFavCount = null;
						String updateFavCountBody = "{}";
						try {
							//send the request，the responde body will be returned
							responseFromUpdateFavCount = updateFavCountCall.execute();

							//get the response body
							updateFavCountBody = responseFromUpdateFavCount.body().string();
							JSONObject updateFavCountBodyJson = new JSONObject(updateFavCountBody);
							String updateFavCountQueryMessage = (String) updateFavCountBodyJson.get("message");

							if (updateFavCountQueryMessage.equals("songAmountFavourites updated")){

								response.put("message", "song unliked in both neo4j and mongoDB");
								response.put("status", HttpStatus.OK);	

							}else if (updateFavCountQueryMessage.equals("songAmountFavourites <= 0, cannot be decremented")) {
								response.put("message", "songAmountFavourites <= 0, cannot be decremented");
								response.put("status", HttpStatus.OK);	

							}else if (updateFavCountQueryMessage.equals("invalid songID")){
								response.put("message", "invalid songID");
								response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
							}else {
								response.put("message", "unkown error");
								response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
							}

						} catch (IOException e) {
							e.printStackTrace();
						}
					}
				}
			}
		}catch  (IOException e) {
			e.printStackTrace();
		}

		return response;
	}

	//delete from neo4j only
	//do not decrease the favourite's count in song
	@RequestMapping(value = "/deleteAllSongsFromDb/{songId}", method = RequestMethod.PUT)
	public @ResponseBody Map<String, Object> deleteAllSongsFromDb(@PathVariable("songId") String songId,
			HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("PUT %s", Utils.getUrl(request)));

		DbQueryStatus status = this.playlistDriver.deleteSongFromDb(songId);
		response.put("message", status.getMessage());
		response = Utils.setResponseStatus(response, status.getdbQueryExecResult(), status.getData());
		return response;
	}
}
