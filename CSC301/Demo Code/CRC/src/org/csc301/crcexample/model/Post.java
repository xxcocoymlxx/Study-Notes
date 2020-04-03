package org.csc301.crcexample.model;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Post {

	
	private String id;
	private String title;
	private String imageUrl;
	private User postedBy;
	private Date postedAt;
	
	private DateFormat dateFormat;  // used in toString
	
	
	// NOTE: This constructor is considered bad style - When using it, it's
	// hard to remember the order of the arguments.
	// The solution: Builder pattern, which we will mention later in the course.
	public Post(String id, String title, String imageUrl, User postedBy, Date postedAt) {
		super();
		this.id = id;
		this.title = title;
		this.imageUrl = imageUrl;
		this.postedBy = postedBy;
		this.postedAt = postedAt;
		this.dateFormat = new SimpleDateFormat();
	}
	
	public Post(String id, String title, String imageUrl, User postedBy) {
		this(id, title, imageUrl, postedBy, new Date());
	}

	
	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getImageUrl() {
		return imageUrl;
	}

	public void setImageUrl(String imageUrl) {
		this.imageUrl = imageUrl;
	}

	public User getPostedBy() {
		return postedBy;
	}

	public void setPostedBy(User postedBy) {
		this.postedBy = postedBy;
	}

	public String getId() {
		return id;
	}
	
	public Date getPostedAt() {
		return postedAt;
	}
	
	@Override
	public String toString() {
		return String.format("%s\nID: %s\nPosted at %s by %s\n%s", getTitle(), getId(), 
				dateFormat.format(getPostedAt()), getPostedBy().getUsername(),
				getImageUrl());
	}
}