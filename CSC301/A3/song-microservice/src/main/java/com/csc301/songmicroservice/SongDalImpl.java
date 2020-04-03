package com.csc301.songmicroservice;

import java.util.List;

import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

/*
 * Data Access Layer interface (DAL)
 * 
 * We will make use of MongoTemplate bean which is initialized 
 * by Spring Boot using the properties we defined in the 
 * src/main/resources/application.properties. 
 * 
 * MongoTemplate provides us some abstracted methods with
 * which we can save an object into the database and get 
 * all data from Database as well.
 */

@Repository
public class SongDalImpl implements SongDal {

	private final MongoTemplate db;

	@Autowired
	public SongDalImpl(MongoTemplate mongoTemplate) {
		this.db = mongoTemplate;
	}

	@Override
	public DbQueryStatus addSong(Song songToAdd) {

		//check if given song (name,artist) already exists in db
		Query query = new Query();
		query.addCriteria(Criteria.where("songName").is(songToAdd.getSongName()));
		query.addCriteria(Criteria.where("songArtistFullName").is(songToAdd.getSongArtistFullName()));
		Song foundSong = this.db.findOne(query, Song.class);

		if (foundSong == null) {
			this.db.insert(songToAdd, "songs");
			DbQueryStatus result = new DbQueryStatus("inserted song",DbQueryExecResult.QUERY_OK);
			result.setData(songToAdd.getJsonRepresentation());
			return result;
		}else {

			return new DbQueryStatus("song already exists",DbQueryExecResult.QUERY_ERROR_GENERIC);
		}
	}


	@Override
	public DbQueryStatus findSongById(String songId) {
		Query query = new Query();
		query.addCriteria(Criteria.where("_id").is(songId));
		Song foundSong = this.db.findOne(query, Song.class);

		if (foundSong != null) {
			DbQueryStatus result = new DbQueryStatus("found song",DbQueryExecResult.QUERY_OK);
			result.setData(foundSong.getJsonRepresentation());
			return result;
		}else {
			return new DbQueryStatus("no song found",DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
		}
	}

	@Override
	public DbQueryStatus getSongTitleById(String songId) {
		Query query = new Query();
		query.addCriteria(Criteria.where("_id").is(songId));
		Song foundSong = this.db.findOne(query, Song.class);

		if (foundSong != null) {
			DbQueryStatus result = new DbQueryStatus("found song",DbQueryExecResult.QUERY_OK);
			result.setData(foundSong.getSongName());
			return result;
		}else {
			return new DbQueryStatus("no song found",DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
		}
	}

	//Deletes the song from the MongoDB database and from all Profiles
	//that have the songId added in their “favourites” list
	@Override
	public DbQueryStatus deleteSongById(String songId) {
		Query query = new Query();
		query.addCriteria(Criteria.where("_id").is(songId));
		Song foundSong = this.db.findOne(query, Song.class);
		if(foundSong!= null) {
			this.db.remove(foundSong);
			return new DbQueryStatus("deletion successful",DbQueryExecResult.QUERY_OK);
		}else {
			return new DbQueryStatus("no song found",DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
		}
	}

	@Override
	public DbQueryStatus updateSongFavouritesCount(String songId, boolean shouldDecrement) {
		Query query = new Query();
		query.addCriteria(Criteria.where("_id").is(songId));
		Song foundSong = this.db.findOne(query, Song.class);

		if (foundSong != null) {

			if (shouldDecrement) {
				if (foundSong.getSongAmountFavourites()>0) {
					long songAmountFavourites = foundSong.getSongAmountFavourites();
					foundSong.setSongAmountFavourites(songAmountFavourites-1);
					this.db.save(foundSong, "songs");
					return new DbQueryStatus("songAmountFavourites updated",DbQueryExecResult.QUERY_OK);
				}else {
					///should NOT error if it is asked to decrement below 0,  explain it in the string, but no error.
					return new DbQueryStatus("songAmountFavourites <= 0, cannot be decremented",DbQueryExecResult.QUERY_OK);
				}

			}else {
				long songAmountFavourites = foundSong.getSongAmountFavourites();
				foundSong.setSongAmountFavourites(songAmountFavourites+1);
				this.db.save(foundSong, "songs");	
				return new DbQueryStatus("songAmountFavourites updated",DbQueryExecResult.QUERY_OK);
			}

		}else {
			return new DbQueryStatus("no song found",DbQueryExecResult.QUERY_ERROR_NOT_FOUND);
		}	
	}

}