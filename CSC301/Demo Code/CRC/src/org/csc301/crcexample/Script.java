package org.csc301.crcexample;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.csc301.crcexample.model.Post;
import org.csc301.crcexample.model.User;
import org.csc301.crcexample.service.DAO;
import org.csc301.crcexample.service.DAOImplInMemory;

public class Script {

	static String username1 = "funkMstr";
	static String username2 = "CatMan";
	static String password = "123456";
	static String url1 = "http://loose.upt.ro/~oose/uploads/SEF/sef.jpg";
	static String url2 = "http://www.dons.net.au/gallery2/d/2328-2/SoftwareEngineering.jpg";
	
	public static void run(DAO dao){
		User u1 = dao.registerUser(username1, password);
		System.out.println("Registered user " + u1.getUsername());
		
		User u2 = dao.registerUser(username2, password);
		System.out.println("Registered user " + u2.getUsername());
		
		System.out.println("Let's try to login with a wrong username ...");
		try{
			dao.login("invalid-username", password);
		} catch (Exception e){
			System.out.println("Error message: " + e.getMessage());
		}
		
		System.out.println("Let's try to login with a wrong password ...");
		try{
			dao.login(username1, "invalid-password");
		} catch (Exception e){
			System.out.println("Error message: " + e.getMessage());
		}
		
		
		System.out.println("Let's try to login as " + username1);
		u1 = dao.login(username1, password);
		System.out.println("Got back User " + u1.getUsername());
		
		System.out.println("Let's try to create a few posts ...");
		List<Post> posts = new ArrayList<Post>();
		for (int i = 1; i < 4; i++) {
			posts.add(dao.createPost(u1.getUsername() + "'s post # " + i, url1, u1));
			posts.add(dao.createPost(u2.getUsername() + "'s post # " + i, url2, u2));
		}
		
		for(Post p : posts){
			System.out.println("\n");
			System.out.println(p);
		}
		
		
		System.out.println("======================================================");
		System.out.println("Let's try to get " + u1.getUsername() + "'s posts ...");
		Iterator<Post> itr = dao.getPostsByUsername(u1.getUsername());
		while (itr.hasNext()) {
			System.out.println("\n");
			System.out.println(itr.next());
		}
	}
	
	
	
	
	
	public static void main(String[] args) {
		/*
		 * Notice that this is the only place where we depend on a specific DAO implementation.
		 */
		run(new DAOImplInMemory());
	}

}
