import java.sql.*;
import java.util.List;

// If you are looking for Java data structures, these are highly useful.
// Remember that an important part of your mark is for doing as much in SQL (not Java) as you can.
// Solutions that use only or mostly Java will not receive a high mark.
import java.util.ArrayList;
public class Assignment2 extends JDBCSubmission {

    public Assignment2() throws ClassNotFoundException {

        Class.forName("org.postgresql.Driver");
    }


    @Override
    //Connect to a database with the supplied credentials.
    public boolean connectDB(String url, String username, String password) {
        // Implement this method!
        try {
            //在JDBCsubmission里已经define了connection这个public的variable
            connection = DriverManager.getConnection(url, username, password);

            String queryString = "SET SEARCH_PATH to parlgov";
            PreparedStatement pStatement = connection.prepareStatement(queryString);
            pStatement.execute() ;

        } catch(SQLException e) {
            System.err.println("SQL Exception." + "<Message>:" + e.getMessage());
            return false;
        }
        return true;
    }

    @Override
    //Disconnect from the database.
    public boolean disconnectDB() {
        // Implement this method!
        try {
            connection.close();
        }catch (SQLException e) {
            System.err.println("SQL Exception." + "<Message>:" + e.getMessage());
            return false;
        }
        return true;
    }

    @Override
    //given a country, returns the list of elections in that country, 
    //in descending order of years, and the cabinets that have formed 
    //after that election and before the next election of the same type.
    //note: the return type is an user-defined object!
    public ElectionCabinetResult electionSequence(String countryName) {
        // Implement this method!
        List<Integer> elections = new ArrayList<Integer>();
        List<Integer> cabinets = new ArrayList<Integer>();
        ArrayList<Integer> tempIds = new ArrayList<Integer>();
        String query1, query2;
        PreparedStatement pstatement1, pstatement2;
        ResultSet rs1, rs2;

        try{
            //the list of elections in that country, in descending order of years
            query1 = "SELECT DISTINCT e.id AS electionID, e.e_date FROM country c, election e " + 
                     "WHERE name = ? AND c.id = e.country_id " +
                     "ORDER BY e.e_date DESC" ;
            pstatement1 = connection.prepareStatement(query1);
            pstatement1.setString(1, countryName);
            rs1 = pstatement1.executeQuery();

            //把我们现有的所有election的id都先存起来
            while (rs1.next()) {
                int tempId = rs1.getInt("electionID");
                tempIds.add(tempId);
            }

            for (int i=0; i<tempIds.size(); i++) {
                //得到当前election id，要对应这个election_id去找cabinets,所有election_i都找一遍
                int currElectionID = tempIds.get(i);

                query2 = "SELECT id FROM cabinet WHERE election_id = ? ORDER BY start_date";
                pstatement2 = connection.prepareStatement(query2);
                pstatement2.setInt(1, currElectionID);
                rs2 = pstatement2.executeQuery();

                //只要当前还有cabinet，就往return的list里加同样数量的当前的electionID和cabinetId
                while (rs2.next()) {
                    int cabinetID = rs2.getInt("id");
                    elections.add(currElectionID);
                    cabinets.add(cabinetID);
                }
            }

        }catch(SQLException e){
            System.err.println("SQL EXCEPTION: <MESSAGE:> " + e.getMessage());
        }

        return new ElectionCabinetResult(elections,cabinets);
    }

    @Override
    //given a president, returns other presidents that have
    //similar comments and descriptions in the database.
    //prof's note: They should be compared together not individually. 
    // you can combine comment and description into one string first.
    // >= (float)threshold
    public List<Integer> findSimilarPoliticians(Integer politicianName, Float threshold) {
        // Implement this method!
        List<Integer> returnList = new ArrayList<Integer>();
        PreparedStatement pStatement1, pStatement2;
        ResultSet rs1, rs2;
        String query1, query2;
        String targetDescription, presidentDescription;
        int politicianID;

        try{

            //first get the comment and description of the given president
            //note: the parameter "politicianName" is actually the politician's ID
            query1 = "SELECT id, description, comment FROM politician_president WHERE id = ?";
            pStatement1 = connection.prepareStatement(query1);
            pStatement1.setInt(1, politicianName);
            rs1 = pStatement1.executeQuery();
            rs1.next();

            //we have to compare the comment AND the description, and concatenate them by a space
            targetDescription = rs1.getString("comment") + " " + rs1.getString("description");

            //Then we have to get the all the other presidents' comment AND descriptions and concatenate them
            query2 = "SELECT id, description, comment FROM politician_president " + 
                     "WHERE id != " + Integer.toString(politicianName);
            pStatement2 = connection.prepareStatement(query2);
            rs2 = pStatement2.executeQuery();

            //Then we will loop through the results like in Example.java
            while(rs2.next()) {
                politicianID = rs2.getInt("id");
                presidentDescription = rs2.getString("comment") + " " + rs2.getString("description");
                float similarity = (float)similarity(targetDescription, presidentDescription);

                //when looping, compare each similarity value with the threshold
                if(similarity >= threshold) returnList.add(politicianID);
            }


        }catch (SQLException e){
            System.err.println("SQL Exception." + "<Message>: " + e.getMessage());
        }
        return returnList;
    }



    public static void main(String[] args) {
        // You can put testing code in here. It will not affect our autotester.
        
    }

}

