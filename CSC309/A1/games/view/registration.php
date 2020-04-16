<?php
//TODO: still have the problem where it can't remember my choice for checklist and radio buttons

// So I don't have to deal with unset $_REQUEST['user'] when refilling the form
// You can also take a look at the new ?? operator in PHP7
$_REQUEST['username']=!empty($_REQUEST['username']) ? $_REQUEST['username'] : '';
$_REQUEST['psw']=!empty($_REQUEST['psw']) ? $_REQUEST['psw'] : '';
$_REQUEST['psw-repeat']=!empty($_REQUEST['psw-repeat']) ? $_REQUEST['psw-repeat'] : '';
$_REQUEST['birthday']=!empty($_REQUEST['birthday']) ? $_REQUEST['birthday'] : '';
$_REQUEST['gender']=!empty($_REQUEST['gender']) ? $_REQUEST['gender'] : '';
?>

<!DOCTYPE html>
<html>
<head>
	<title>User Registration</title>
</head>

<body>
<header><h1>User Registration</h1></header>

<main>

<!-- submit the form to index.php to check user inputs -->
<form method="post" action="index.php">
  <div class="container">
    <h1>Create New Account</h1>
    <p>Please fill in this form to create an account.</p>
    <hr>

    <label for="email"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="username" required minlength="4" value="<?php echo($_REQUEST['username']); ?>">

	<br><br>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required minlength="6" value="<?php echo($_REQUEST['psw']); ?>">

	<br><br>

    <label for="psw-repeat"><b>Repeat Password</b></label>
	<input type="password" placeholder="Repeat Password" name="psw-repeat" required minlength="6" value="<?php echo($_REQUEST['psw-repeat']); ?>">
	
	<br><br>

	<label><b>Gender</b></label>
	<select name="gender" value="<?php echo($_REQUEST['gender']); ?>">
					<option value="male"> Male </option>
					<option value="female"> Female </option>
					<option value="Unknown "> Unknown </option>
	</select>

	<br><br>

	<label><b>Birthday</b></label>
	<input type="date" name="birthday" value="<?php echo($_REQUEST['birthday']); ?>">

	<br><br>


	<label><b>Please choose one free gift for new users.</b></label>
	<ul> 
        <!--------------------------------->
        <li>
        <label>
            <input type="radio" name="category" value="giftcard" checked="<?php echo($_REQUEST['category']); ?>"/> 
            Tim Hortons $5 gift card
        </label>
        </li>

                                <!--------------------------------->

                                <li>
                                    <label>
                                        <input type="radio" name="category" value="3sub" checked="<?php echo($_REQUEST['category']); ?>"/> 
										Free Subsribtion for 3 Months
                                    </label>
                                </li>

                                <!--------------------------------->

                                <li>
                                    <label>
                                        <input type="radio" name="category" value="secret" checked="<?php echo($_REQUEST['category']); ?>"/> 
										Secret Algorithm for Solving Master Mind Fast
                                    </label>
                                </li> 
                                <!--------------------------------->
								<li>
                                    <label>
                                        <input type="radio" name="category" value="nogift" checked="<?php echo($_REQUEST['category']); ?>"/> 
										I don't want free gifts
                                    </label>
                                </li> 

                            </ul>


	<label><b>Subscribe to our newsletter?</b></label>
	<label>
		<input type="checkbox" name="subscribe" value="yes" <?php if(!empty($_POST['yes_sub']['yes'])) echo 'checked="checked"'; ?>/>
	</label>

	<br/><br/>

	<hr>


	
    <input type="submit" name="register" value="Register" />
  </div>
	
  <tr><th>&nbsp;</th><td><?php echo(view_errors($errors)); ?></td></tr>
</form>

</main>

<a href="?operation=login">Back to Login</a>

<footer>
</footer>

</body>
</html>