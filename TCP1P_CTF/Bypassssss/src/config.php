<?php
$host = "mysql-db";
$username = "ctf";
$password = "Password_K1nz";
$databasename = "Z0k3r_K1nz";
$conn = mysqli_connect($host, $username, $password, $databasename);

if (!$conn) {
    die("Connection failed");
}
?>