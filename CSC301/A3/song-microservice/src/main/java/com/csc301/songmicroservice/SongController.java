package com.csc301.songmicroservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import okhttp3.Call;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import javax.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("/")
public class SongController {

	@Autowired
	private final SongDal songDal;
	private String regex = "^[a-zA-Z0-9]+$";
	private Pattern pattern = Pattern.compile(regex);

	private OkHttpClient client = new OkHttpClient();

	
	public SongController(SongDal songDal) {
		this.songDal = songDal;
	}

	
	@RequestMapping(value = "/getSongById/{songId}", method = RequestMethod.GET)
	public @ResponseBody Map<String, Object> getSongById(@PathVariable("songId") String songId,
			HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("GET %s", Utils.getUrl(request)));
		
		Matcher matcher = pattern.matcher(songId);
		if (songId.equals("") || songId.length() != 24 || !matcher.matches()) {
			response.put("message", "invalid songID");
			response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
			return response;
		}

		DbQueryStatus dbQueryStatus = songDal.findSongById(songId);

		response.put("message", dbQueryStatus.getMessage());
		response = Utils.setResponseStatus(response, dbQueryStatus.getdbQueryExecResult(), dbQueryStatus.getData());

		return response;
	}

	
	@RequestMapping(value = "/getSongTitleById/{songId}", method = RequestMethod.GET)
	public @ResponseBody Map<String, Object> getSongTitleById(@PathVariable("songId") String songId,
			HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("GET %s", Utils.getUrl(request)));
		
		Matcher matcher = pattern.matcher(songId);
		if (songId.equals("") || songId.length() != 24 || !matcher.matches()) {
			response.put("message", "invalid songID");
			response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
			return response;
		}
		
		DbQueryStatus dbQueryStatus = songDal.getSongTitleById(songId);
		
		response.put("message", dbQueryStatus.getMessage());
		response = Utils.setResponseStatus(response, dbQueryStatus.getdbQueryExecResult(), dbQueryStatus.getData());

		return response;
	}

	
	@RequestMapping(value = "/deleteSongById/{songId}", method = RequestMethod.DELETE)
	public @ResponseBody Map<String, Object> deleteSongById(@PathVariable("songId") String songId,
			HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("DELETE %s", Utils.getUrl(request)));
		
		Matcher matcher = pattern.matcher(songId);
		if (songId.equals("") || songId.length() != 24 || !matcher.matches()) {
			response.put("message", "invalid songID");
			response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
			return response;
		}

		DbQueryStatus dbQueryStatus = songDal.deleteSongById(songId);
		
		response.put("message", dbQueryStatus.getMessage());
		response = Utils.setResponseStatus(response, dbQueryStatus.getdbQueryExecResult(), dbQueryStatus.getData());

		return response;
	}

	
	@RequestMapping(value = "/addSong", method = RequestMethod.POST)
	public @ResponseBody Map<String, Object> addSong(@RequestParam Map<String, String> params,
			HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("path", String.format("POST %s", Utils.getUrl(request)));
		
		
		String songName = params.get("songName");
		String songArtistFullName = params.get("songArtistFullName");
		String songAlbum = params.get("songAlbum");
		
		if(songName==null || songArtistFullName == null || songAlbum==null ||
				songName.equals("") || songArtistFullName.equals("") || songAlbum.equals("")) {
			response.put("message", "BAD REQUEST");
			response = Utils.setResponseStatus(response, DbQueryExecResult.QUERY_ERROR_GENERIC, null);
			return response;
			
		}else {
			Song newSong = new Song(songName, songArtistFullName, songAlbum);

			DbQueryStatus dbQueryStatus = songDal.addSong(newSong);
		
			response.put("message", dbQueryStatus.getMessage());
			response = Utils.setResponseStatus(response, dbQueryStatus.getdbQueryExecResult(), dbQueryStatus.getData());

			return response;
		}
	}

	
	@RequestMapping(value = "/updateSongFavouritesCount/{songId}", method = RequestMethod.PUT)
	public @ResponseBody Map<String, Object> updateFavouritesCount(@PathVariable("songId") String songId,
			@RequestParam("shouldDecrement") String shouldDecrement, HttpServletRequest request) {

		Map<String, Object> response = new HashMap<String, Object>();
		response.put("data", String.format("PUT %s", Utils.getUrl(request)));
		
		Matcher matcher = pattern.matcher(songId);
		if (songId.equals("") || songId.length() != 24 || !matcher.matches()) {
			response.put("message", "invalid songID");
			response.put("status", HttpStatus.INTERNAL_SERVER_ERROR);
			return response;
		}

		boolean should_decrement = shouldDecrement.equals("true");
		DbQueryStatus dbQueryStatus = songDal.updateSongFavouritesCount(songId,should_decrement);
		
		response.put("message", dbQueryStatus.getMessage());
		response = Utils.setResponseStatus(response, dbQueryStatus.getdbQueryExecResult(), dbQueryStatus.getData());

		return response;
	}
	
}