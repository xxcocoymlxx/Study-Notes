package org.csc301.crcexample.service;

import java.util.Iterator;

import org.csc301.crcexample.model.Post;
import org.csc301.crcexample.model.User;

public interface DAO {

	public User registerUser(String username, String password);
	public User login(String username, String password);
	public Post createPost(String title, String imageUrl, User user);
	public Iterator<Post> getPostsByUsername(String username);
	public Post getPostById(String postId);
	
}