package com.csc301.profilemicroservice;

import java.util.HashMap;
import java.util.Map;

import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.StatementResult;
import org.springframework.stereotype.Repository;
import org.neo4j.driver.v1.Transaction;

@Repository
public class PlaylistDriverImpl implements PlaylistDriver {

	Driver driver = ProfileMicroserviceApplication.driver;

	public static void InitPlaylistDb() {
		String queryStr;

		try (Session session = ProfileMicroserviceApplication.driver.session()) {
			try (Transaction trans = session.beginTransaction()) {
				queryStr = "CREATE CONSTRAINT ON (nPlaylist:playlist) ASSERT exists(nPlaylist.plName)";
				trans.run(queryStr);
				trans.success();
			}
			session.close();
		}
	}
	
	public boolean userExists(String userName) {
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("userName", userName);
		try(Session session = ProfileMicroserviceApplication.driver.session()){
			try(Transaction trans = session.beginTransaction()){
				String queryStr = "MATCH (p1:profile) WHERE p1.userName = $userName RETURN p1" ;
				StatementResult exists = trans.run(queryStr, parameters);
				trans.success();
				if (exists.hasNext()) {
					session.close();
					return true;
				}
			}
			session.close();
		}
		return false;
	}
	
	public boolean songExists(String songId) {
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("songId", songId);
		try(Session session = ProfileMicroserviceApplication.driver.session()){
			try(Transaction trans = session.beginTransaction()){
				String queryStr = "MATCH (s:song) WHERE s.songId = $songId RETURN s" ;
				StatementResult exists = trans.run(queryStr, parameters);
				trans.success();
				if (exists.hasNext()) {
					session.close();
					return true;
				}
			}
			session.close();
		}
		return false;
	}
	
	public boolean putSongInNeo4j(String songId) {
		System.out.println("inside putSongInNeo4j");
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("songId", songId);
		try(Session session = ProfileMicroserviceApplication.driver.session()){
			try(Transaction trans = session.beginTransaction()){
				String queryStr = "Create (s:song{songId: $songId})" ;
				trans.run(queryStr, parameters);
				trans.success();
				session.close();
				return true;
			}
			catch(Exception e) {
				session.close();
				return false;
			}
			
		}catch(Exception e) {
			return false;
		}
	}
	
	public boolean plContainsSong(String userName, String songId) {
		String queryStr;
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("songId", songId);
        parameters.put("plName", userName.concat("-favourites"));
        try(Session session = ProfileMicroserviceApplication.driver.session()){
			try(Transaction trans = session.beginTransaction()){
				queryStr = "MATCH (pl {plName: $plName})-[r:includes]->(s {songId: $songId}) RETURN r";
				trans.success();
				StatementResult match = trans.run(queryStr, parameters);
				if (match.hasNext()) {
					session.close();
					System.out.println("match for song in pl found");
					return true;
				}
			}
			session.close();
        }
        return false;
	}

	@Override
	public DbQueryStatus likeSong(String userName, String songId) {
		DbQueryStatus status;
		String queryStr;
		
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("songId", songId);
        parameters.put("plName", userName.concat("-favourites"));
        
        //check if user exists
        if (! userExists(userName)) {
        	status = new DbQueryStatus("user does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        	return status;
        }
        
        //if user already likes the song
        else if (plContainsSong(userName, songId)) {
        	status = new DbQueryStatus("song already liked", DbQueryExecResult.QUERY_OK);
        }
        
        //like the song
        else {
        	try(Session session = ProfileMicroserviceApplication.driver.session()){
        		try(Transaction trans = session.beginTransaction()){
        			//if song not in neo4j DB yet, add it
        			if(! songExists(songId)) {
        				putSongInNeo4j(songId);
        			}
        			queryStr = "MATCH (pl:playlist),(s:song) WHERE pl.plName = $plName AND s.songId = $songId "
    							+ "CREATE (pl)-[i:includes]->(s)";
        			trans.run(queryStr, parameters);
        			trans.success();
        			status = new DbQueryStatus("song added to playlist", DbQueryExecResult.QUERY_OK);
        		}catch(Exception e) {
        			System.out.println("e1");
        			status = new DbQueryStatus("error", DbQueryExecResult.QUERY_ERROR_GENERIC);
        		}
        		session.close();
        	}catch(Exception e) {
        		System.out.println("e2");
        		status = new DbQueryStatus("error", DbQueryExecResult.QUERY_ERROR_GENERIC);
        	}
        }
        return status;
	}

	@Override
	public DbQueryStatus unlikeSong(String userName, String songId) {
		DbQueryStatus status;
		String queryStr;
		
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("songId", songId);
        parameters.put("plName", userName.concat("-favourites"));
        
        //check if user exists
        if (! userExists(userName)) {
        	status = new DbQueryStatus("user does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        //check if song exists
        else if (! songExists(songId)) {
        	status = new DbQueryStatus("song does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        //if song not already liked, like it
        else {
        	try(Session session = ProfileMicroserviceApplication.driver.session()){
        		try(Transaction trans = session.beginTransaction()){
        			//if song in user's playlist
        			if (plContainsSong(userName, songId)) {
        				queryStr = "MATCH (pl {plName: $plName})-[r:includes]->(s {songId: $songId}) DELETE r";
        				trans.run(queryStr, parameters);
        				trans.success();
        				status = new DbQueryStatus("song unliked", DbQueryExecResult.QUERY_OK);	
        			}
        			//if song not user's playlist to being with
        			else {
        				status = new DbQueryStatus("song was not liked to begin with", DbQueryExecResult.QUERY_OK);
        			}
        		}catch(Exception e) {
        			status = new DbQueryStatus("error", DbQueryExecResult.QUERY_ERROR_GENERIC);
        		}
        		session.close();
        	}catch(Exception e) {
        		status = new DbQueryStatus("error", DbQueryExecResult.QUERY_ERROR_GENERIC);
        	}
        }
        return status;
	}

	@Override
	public DbQueryStatus deleteSongFromDb(String songId) {
		DbQueryStatus status;
		String queryStr;
		
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("songId", songId);
        
        //check if songExists
        if (! songExists(songId)) {
        	status = new DbQueryStatus("song does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        
        //detach delete that song
        else {
        	try(Session session = ProfileMicroserviceApplication.driver.session()){
        		try(Transaction trans = session.beginTransaction()){
        			queryStr = "MATCH (s { songId: $songId }) DETACH DELETE s";
        			trans.run(queryStr, parameters);
        			trans.success();
        			status = new DbQueryStatus("song deleted from database", DbQueryExecResult.QUERY_OK);	
        		}catch(Exception e) {
        			System.out.println("e1");
        			status = new DbQueryStatus("error", DbQueryExecResult.QUERY_ERROR_GENERIC);
        		}
        	session.close();
        	}catch(Exception e) {
        		status = new DbQueryStatus("error", DbQueryExecResult.QUERY_ERROR_GENERIC);
    		}
        }
        
        return status;
        }
}
