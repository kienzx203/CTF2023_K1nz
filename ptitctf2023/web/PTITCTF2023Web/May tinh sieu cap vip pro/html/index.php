<?php
// error_reporting(0);
// ini_set('display_errors', 0);
?>
<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<title>Trigonometric Formula v1.0 | PTITCTF 2023</title>
</head>

<body>
	<h1>Trigonometric Formula v1.0</h1>
	<h3>Example</h3>
	<ul>
		<li>sin(1)+cos(1)</li>
		<li>1+1000</li>
		<li>800*2</li>
	</ul>
	Function support: <b>sin(),cos(),tan(),asin(),acos(),atan(),atan2()</b>
	<!-- check phpinfo.php for more information -->
	<form method="POST" action="index.php">
		<textarea class="textarea" name="code" rows="5" cols="50" required=""></textarea>
		</div>
		</div>
		<button type="submit">Calc</button>
	</form>
	<h3>Result</h3>



	<?php
	if (isset($_POST['code']) || !empty($code)) {

		if (preg_match("/^[sincoeta01234567\[\]\{\}()$8=9*+-;]+$/", $_POST['code']) && is_string($_POST['code'])) {
			$string = "echo " . $_POST['code'] . ";";
			if (strlen($_POST['code']) < 1) {
				echo '<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSV_5L1GYajJWZ2di-NhG3bEzd27C6CUr6AoffoAqk0pOrozgb7G_aFP7iT4eINkU00aiw&usqp=CAU">';
			} else {
				echo ($string);
				eval($string);
			}
		} else {
			echo '<img src="https://i.imgflip.com/f7s0m.jpg?a450768" width="250" height="250">';
		}
	}

	?>
	</pre>
</body>

</html>