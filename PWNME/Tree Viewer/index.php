<?php
$parsed = isset($_POST['input']) ? $_POST['input'] : "/home/";

preg_match_all('/[;|]/m', $parsed, $illegals, PREG_SET_ORDER, 0);
if ($illegals) {
    echo "Illegals chars found";
    $parsed = "/home/";
}

if (isset($_GET['source'])) {
    highlight_file(__FILE__);
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tree Viewer</title>
</head>

<body>
    <a href="/?source">Source code</a>
    <hr />
    <form action="/" method="post">
        <label for="input">Directory to check</label>
        <input type="text" placeholder="Directory to see" id="input" name="input" value="<?= $parsed ?>">
    </form>

    <h3>Content of
        <?= $parsed ?>:
        <?= shell_exec('ls ' . $parsed); ?>
    </h3>

</body>

</html>
?>