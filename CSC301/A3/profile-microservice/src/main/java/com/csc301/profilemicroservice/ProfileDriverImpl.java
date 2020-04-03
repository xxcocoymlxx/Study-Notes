package com.csc301.profilemicroservice;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.Record;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.StatementResult;

import org.springframework.stereotype.Repository;
import org.neo4j.driver.v1.Transaction;

@Repository
public class ProfileDriverImpl implements ProfileDriver {

	Driver driver = ProfileMicroserviceApplication.driver;

	public static void InitProfileDb() {
		String queryStr;

		try (Session session = ProfileMicroserviceApplication.driver.session()) {
			try (Transaction trans = session.beginTransaction()) {
				queryStr = "CREATE CONSTRAINT ON (nProfile:profile) ASSERT exists(nProfile.userName)";
				trans.run(queryStr);

				queryStr = "CREATE CONSTRAINT ON (nProfile:profile) ASSERT exists(nProfile.password)";
				trans.run(queryStr);

				queryStr = "CREATE CONSTRAINT ON (nProfile:profile) ASSERT nProfile.userName IS UNIQUE";
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
				//if profile with matching userName found, return true
				if (exists.hasNext()) {
					session.close();
					return true;
				}
			}
			session.close();
		}
		return false;
	}
	
	public boolean isFollowing(String user, String friend) {
		String queryStr;
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("userName", user);
        parameters.put("frndUserName", friend);
        try(Session session = ProfileMicroserviceApplication.driver.session()){
    		try(Transaction trans = session.beginTransaction()){
    			queryStr = "MATCH (p1 {userName: $userName})-[f:follows]->(p2 {userName: $frndUserName}) RETURN f";
				trans.success();
				StatementResult match = trans.run(queryStr, parameters);
				//if match found, return true
				if (match.hasNext()) {
					session.close();
					return true;
				}
    		}
        }
        return false;	
	}
	
	@Override
	public DbQueryStatus createUserProfile(String userName, String fullName, String password) {
		DbQueryStatus status;
		String queryStr;
		
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("userName", userName);
        parameters.put("fullName", fullName);
        parameters.put("password", password);
        parameters.put("plName", userName.concat("-favourites"));
        
        if (userName == null || userName.equals("")){
        	status = new DbQueryStatus("no userName provided", DbQueryExecResult.QUERY_ERROR_GENERIC);
        }
        else if (password == null || password.equals("")) {
        	status = new DbQueryStatus("no password provided", DbQueryExecResult.QUERY_ERROR_GENERIC);
        }
        else if (userExists(userName)) {
        	status = new DbQueryStatus("userName already in use", DbQueryExecResult.QUERY_ERROR_GENERIC);
        }
        else {
        	try(Session session = ProfileMicroserviceApplication.driver.session()){
        		try (Transaction trans = session.beginTransaction()) {
        			queryStr = "CREATE (p:profile {userName: $userName, fullName: $fullName, password: $password})"
        				+ "CREATE (pl:playlist {plName: $plName}) CREATE (p)-[r:created]->(pl)";
        			trans.run(queryStr, parameters);
        			trans.success();
        			status = new DbQueryStatus("profile created", DbQueryExecResult.QUERY_OK);	
        			
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
	public DbQueryStatus followFriend(String userName, String frndUserName) {
		DbQueryStatus status;
		String queryStr;
		
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("userName", userName);
        parameters.put("frndUserName", frndUserName);
        
        if(! userExists(userName)) {
        	status = new DbQueryStatus("user does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        
        else if (userName.equals(frndUserName)) {
        	status = new DbQueryStatus("user cannot follow self", DbQueryExecResult.QUERY_OK);
        	return status;
        }
        
        else if (! userExists(frndUserName)){
        	status = new DbQueryStatus("frndUserName does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        
        else if (isFollowing(userName, frndUserName)) {
        	status = new DbQueryStatus("user already follows friend", DbQueryExecResult.QUERY_OK);
        }
        
        else {
        	try(Session session = ProfileMicroserviceApplication.driver.session()){
        		try(Transaction trans = session.beginTransaction()){
        			queryStr = "MATCH (p1:profile),(p2:profile) WHERE p1.userName = $userName AND p2.userName = $frndUserName "
            					+ "CREATE (p1)-[r:follows]->(p2)";
        			trans.run(queryStr, parameters);
        			trans.success();
        			status = new DbQueryStatus("friend followed", DbQueryExecResult.QUERY_OK);
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
	public DbQueryStatus unfollowFriend(String userName, String frndUserName) {
		DbQueryStatus status;
		String queryStr;
		
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("userName", userName);
        parameters.put("frndUserName", frndUserName);
        
        if(! userExists(userName)) {
        	status = new DbQueryStatus("user does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        
        if (userName.equals(frndUserName)) {
        	status = new DbQueryStatus("user cannot unfollow self", DbQueryExecResult.QUERY_OK);
        	return status;
        }
       
        else if (! userExists(frndUserName)){
        	status = new DbQueryStatus("frndUserName does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        
        else if (! isFollowing(userName, frndUserName)) {
        	status = new DbQueryStatus("user already does not follow friend", DbQueryExecResult.QUERY_OK);
        }
        
        else {
        	try(Session session = ProfileMicroserviceApplication.driver.session()){
        		try(Transaction trans = session.beginTransaction()){
        			queryStr = "MATCH (p1 {userName: $userName})-[r:follows]->(p2 {userName: $frndUserName}) DELETE r";
        			trans.run(queryStr, parameters);
        			trans.success();
        			status = new DbQueryStatus("friend unfollowed", DbQueryExecResult.QUERY_OK);	
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
	public DbQueryStatus getAllSongFriendsLike(String userName) {
		Map<String, ArrayList<String>> faveSongs = new HashMap<String, ArrayList<String>>();
		DbQueryStatus status;
		String queryStr;
		
		Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("userName", userName);
        
        if (! userExists(userName)) {
        	System.out.println("user does not exist");
        	status = new DbQueryStatus("user does not exist", DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
        }
        
        else {
        	try(Session session = ProfileMicroserviceApplication.driver.session()){
        		try(Transaction trans = session.beginTransaction()){
        			//get all of user's followers using helper
        			queryStr = "MATCH (p1 {userName: $userName})-[r:follows]->(p2: profile) RETURN { userName : p2.userName } as node;";
        			StatementResult followers = trans.run(queryStr, parameters);
        			System.out.println("searched for followees");
        			while (followers.hasNext()) {
        				Record currFollower = followers.next();
        				System.out.println("attempt to get followee username");
        				String follower = currFollower.get("node").get("userName").asString();
        				System.out.println("got followee username");
        				parameters.put("plName", follower.concat("-favourites"));
        				System.out.println("plName is: ".concat(parameters.get("plName").toString()));
        				faveSongs.put(follower, new ArrayList<String>());
        				//get follower's favourite songs using name of playlist
        				queryStr = "MATCH (pl:playlist)-[i:includes]->(s:song) "
        						+ "WHERE pl.plName = $plName RETURN { songId : s.songId } as node;";
        				StatementResult songIds = trans.run(queryStr, parameters);
        				System.out.println("searched for songs of a followee");
        				trans.success();
        				while(songIds.hasNext()) {
        					Record id = songIds.next();
        					String songId = id.get("node").get("songId").asString();
        					faveSongs.get(follower).add(songId);
        				}
        			}
        			status = new DbQueryStatus("favourite songIds collected", DbQueryExecResult.QUERY_OK);
        			status.setData(faveSongs);
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
}
