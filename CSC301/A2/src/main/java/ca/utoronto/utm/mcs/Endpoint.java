package ca.utoronto.utm.mcs;
import static com.mongodb.client.model.Filters.eq;

import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import org.bson.Document;
import org.bson.types.ObjectId;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.mongodb.BasicDBObjectBuilder;
import com.mongodb.DBObject;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.result.DeleteResult;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;


public class Endpoint implements HttpHandler{
	private static MongoClient db;
	private static MongoCollection<Document> collection;

	public Endpoint(MongoClient d) {
		this.db = d;
		this.collection = db.getDatabase("csc301a2").getCollection("posts");
	}

	public void handle(HttpExchange r) {
		try {

			if (r.getRequestMethod().equals("PUT")) {
				handlePut(r);
			}else if (r.getRequestMethod().equals("DELETE")) {
				handleDelete(r);
			}else if (r.getRequestMethod().equals("GET")) {
				handleGet(r);           	
			}else {
				r.sendResponseHeaders(405, -1);// METHOD NOT ALLOWED
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void handlePut(HttpExchange r) throws IOException, JSONException{
		try {

			String body = Utils.convert(r.getRequestBody());//converts InputStream to String

			try {
				JSONObject deserialized = new JSONObject(body);

				String title = null;
				String author = null;
				String content = null;
				JSONArray tags_array = null;
				List<String> tags = new ArrayList<>();

				//get actor id from JSON
				if (deserialized.has("author") && deserialized.has("title") 
						&& deserialized.has("content") && deserialized.has("tags")) {

					//convert a JSON object to a database object

					title = deserialized.getString("title");
					author = deserialized.getString("author");
					content = deserialized.getString("content");
					tags_array = deserialized.getJSONArray("tags");


					if ((!(title instanceof String)) || (!(author instanceof String)) || (!(content instanceof String))
							|| title.equals("") || author.equals("") || content.equals("") || tags_array.length() == 0) {
						r.sendResponseHeaders(400, -1);//BAD REQUEST
						return;
					}else {
						JSONObject response_body = new JSONObject();

						for (int i = 0, l = tags_array.length(); i < l; i++) {

							if (tags_array.get(i) instanceof String) {
								tags.add(tags_array.getString(i));
							}else {
								r.sendResponseHeaders(400, -1);//BAD REQUEST
								return;
							}
						}

						BasicDBObjectBuilder builder = BasicDBObjectBuilder.start()
								.append("title", title).append("author", author)
								.append("content", content).append("tags", tags);

						DBObject doc = builder.get();
						//convert the DB object to a document to be inserted
						Document result = new Document(doc.toMap());

						this.collection.insertOne(result);

						//we now have the id of the newly inserted document
						ObjectId id = result.getObjectId("_id");
						//convert the ID to a string
						String returnID = id.toString();

						//success response
						response_body.put("_id", returnID);
						r.sendResponseHeaders(200, response_body.toString().length());

						OutputStream os = r.getResponseBody();
						os.write(response_body.toString().getBytes());//write whatever bytes the response has
						os.close();
					}

				} else {
					r.sendResponseHeaders(400, -1);//BAD REQUEST
				}

			}catch(JSONException j) {
				r.sendResponseHeaders(400, -1);// BAD REQUEST
			}
		}catch(Exception e) {
			r.sendResponseHeaders(500, -1);// INTERNAL SERVER ERROR
		}


	}//function ends


	public void handleDelete(HttpExchange r) throws IOException, JSONException{
		try {

			String body = Utils.convert(r.getRequestBody());//converts InputStream to String

			try {
				JSONObject deserialized = new JSONObject(body);

				String deleteID = null;

				//get actor id from JSON
				if (deserialized.has("_id")) {

					//convert a JSON object to a database object

					deleteID = deserialized.getString("_id");
					if (deleteID.equals("") || (!(deleteID instanceof String))) {
						r.sendResponseHeaders(400, -1);//BAD REQUEST
						return;
					}

				} else {
					r.sendResponseHeaders(400, -1);//BAD REQUEST
				}


				try {

					Document idDoc = new Document("_id", new ObjectId(deleteID));   
					DeleteResult count = this.collection.deleteOne(idDoc);
					Integer res = (int) count.getDeletedCount();

					if (res == 1) {
						//success response (no response body)
						r.sendResponseHeaders(200, -1);
					}else{
						//if the id is not found, it will not crash, it just returns 0
						r.sendResponseHeaders(404, -1);//NOT FOUND
					}

				}catch (Exception e){

					r.sendResponseHeaders(400, -1);//BAD REQUEST
				}

			}catch(JSONException j) {
				r.sendResponseHeaders(400, -1);//BAD REQUEST
			}
		}catch(Exception e) {
			r.sendResponseHeaders(500, -1);// INTERNAL SERVER ERROR
		}

	}//function ends


	public void handleGet(HttpExchange r) throws IOException, JSONException{
		String postTitle = null;
		String postId = null;
		try {
			String body = Utils.convert(r.getRequestBody());
			try {
				JSONObject deserialized = new JSONObject(body);

				//if searching using a provided id
				if (deserialized.has("_id")) {
					postId = deserialized.getString("_id");
					if ((!(postId instanceof String)) || postId.equals("")) {
						r.sendResponseHeaders(400, -1);
					}
					else {
						Document result = this.collection.find(eq("_id", new ObjectId(postId))).first();

						//if no result matching provided id
						if (result == null) {
							if (deserialized.has("title")) {
								r.sendResponseHeaders(400, -1);
							}
							else {
								r.sendResponseHeaders(404, -1);
							}
						}

						else {
							JSONObject response_body = new JSONObject();
							JSONObject oid = new JSONObject();
							oid.put("$oid", postId);
							response_body.put("_id", oid);
							response_body.put("title", result.get("title"));
							response_body.put("author", result.get("author"));
							response_body.put("content", result.get("content"));
							response_body.put("tags", result.get("tags"));


							r.sendResponseHeaders(200, response_body.toString().length());
							OutputStream os = r.getResponseBody();
							os.write(response_body.toString().getBytes());
							os.close();
						}
					}
				}

				//if searching using a provided title
				else if (deserialized.has("title")) {
					List<JSONObject> results = new ArrayList<>(); 
					postTitle = deserialized.getString("title");
					if ((!(postTitle instanceof String)) || postTitle.equals("")) {
						r.sendResponseHeaders(400, -1);
					}
					else {
						//add each result with the word resultspostTitle
						FindIterable<Document> docs = (this.collection).find(
								Filters.regex("title", "\\b".concat(postTitle).concat("\\b")));
						for (Document doc : docs) {
							JSONObject currRes = new JSONObject();
							JSONObject oid = new JSONObject();
							oid.put("$oid", doc.get("_id"));
							currRes.put("_id", oid);
							currRes.put("title", doc.get("title"));
							currRes.put("author", doc.get("author"));
							currRes.put("content", doc.get("content"));
							currRes.put("tags", doc.get("tags"));
							results.add(currRes);
						}
						//if no results found with word postTitle in the title field
						if (results.size() == 0) {
							r.sendResponseHeaders(404, -1);
						}
						//if at least 1 response found with word postTitle in title field
						else {
							r.sendResponseHeaders(200, results.toString().length());
							OutputStream os = r.getResponseBody();
							os.write(results.toString().getBytes());
							os.close();
						}
					}
				}
				//if no title or id provided
				else {
					r.sendResponseHeaders(400, -1);
				}
			}catch(Exception e) {
				r.sendResponseHeaders(400, -1); //cannot make JSON object from request body
			}
		}catch(Exception e) {
			r.sendResponseHeaders(500, -1);//INTERNAL SERVER ERROR
		}
	}

}//class ends













