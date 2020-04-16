<!DOCTYPE html>
<html>
<head>
	<title>User Profile</title>
    <link rel="stylesheet" type="text/css" href="style.css" />
</head>

<body>

<header><h1>Game Center</h1></header>
		<nav>
			<ul>
			<li> Games
			<li> <a href="?operation=guessgame">Guess Game</a>
			<li> <a href="?operation=15puzzles">15 Puzzles</a>
			<li> <a href="?operation=pegsolitare">Peg Solitare</a>
			<li> <a href="?operation=mastermind">Master Mind</a>
			<li> <hr>
			<li> <a href="?operation=mainpage">Main Page</a>
			<li> <a href="?operation=userprofile">User Profile</a>
			<li> <a href="?operation=gamestats">Game Stats</a>
			<li> <a href="?operation=logout">Log Out</a>
            </ul>
		</nav>

<main>
<!-- submit the form to index.php to check user inputs -->
<form method="post" action="index.php">
  <div class="container">
    <h1>User Profile</h1>
    <p>You can modify and update your profile.</p>
    <hr>


    <label for="email"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="username" required minlength="4" value="<?php echo($_SESSION['user']->username); ?>" readonly = "readonly">

	<br><br>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required minlength="6" value="<?php echo($_SESSION['user']->password); ?>">

	<br><br>

    <label for="psw-repeat"><b>Repeat Password</b></label>
	<input type="password" placeholder="Repeat Password" name="psw-repeat" required minlength="6" value="<?php echo($_SESSION['user']->password); ?>">
	
	<br><br>

	<label><b>Gender</b></label>
	<select name="gender" >
					<option value="male"  <?php if($_SESSION['user']->genderflag == 0) {echo "selected";}?>> Male </option>
					<option value="female" <?php if($_SESSION['user']->genderflag == 1) {echo "selected";}?>> Female </option>
					<option value="Unknown" <?php if($_SESSION['user']->genderflag == 3) {echo "selected";}?>> Unknown </option>
	</select>

	<br><br>

	<label><b>Birthday</b></label>
	<input type="date" name="birthday" value="<?php echo($_SESSION['user']->birthday); ?>">

	<br><br>

	<label><b>Please choose one free gift for new users.</b></label>
    <br>
    Note: Since this gift can only be offered once for new registered users. You are unable to change it at this time.
	<ul> 
        <!--------------------------------->
        <li>
        <label>
            <input type="radio" name="category" value="giftcard" 
            <?php if($_SESSION['user']->giftflag == 2) {echo "checked";}?> disabled='disabled'/> 
            Tim Hortons $5 gift card
        </label>
        </li>

         <!--------------------------------->

        <li>
            <label>
                <input type="radio" name="category" value="3sub" 
                <?php if($_SESSION['user']->giftflag == 3) {echo "checked";}?> disabled='disabled'/> 
				Free Subsribtion for 3 Months
            </label>
        </li>

                                <!--------------------------------->

                                <li>
                                    <label>
                                        <input type="radio" name="category" value="secret" 
                                        <?php if($_SESSION['user']->giftflag == 4) {echo "checked";}?> disabled='disabled'/> 
										Secret Algorithm for Solving Master Mind Fast
                                    </label>
                                </li> 
                                <!--------------------------------->
								<li>
                                    <label>
                                        <input type="radio" name="category" value="nogift" 
                                        <?php if($_SESSION['user']->giftflag == 1) {echo "checked";}?> disabled='disabled'/> 
										I don't want free gifts
                                    </label>
                                </li> 

                            </ul>



	<label><b>Subscribe to our newsletter?</b></label>
	<label>
		<input type="checkbox" name="subscribe" value= "yes"
        <?php if($_SESSION['user']->subflag == 1) {echo "checked";} ?> />
        
	</label>

	<br/>

	<hr>
	
    <input type="submit" name="update" value="Update Profile" />
  </div>
	
  <br/>
  <tr><th>&nbsp;</th><td><?php echo(view_errors($errors)); ?></td></tr>
  <tr><th>&nbsp;</th><td><?php 
					if(isset($_SESSION['message'])) {
						echo($_SESSION['message']);
					} ?></td></tr>
</form>

</main>

<footer>
</footer>

</body>
</html>