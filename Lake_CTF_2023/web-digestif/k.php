<?php
$data = [];
$needed_parts = ['nonce' => 1, 'nc' => 1, 'cnonce' => 1, 'qop' => 1, 'username' => 1, 'uri' => 1, 'response' => 1];
$matches = [];

preg_match_all('@(\w+)=(?:(["\'])([^\2]+?)\2|([^\s,]+))@', $_SERVER['PHP_AUTH_DIGEST'], $matches, PREG_SET_ORDER);

foreach ($matches as $m) {
    $data[$m[1]] = $m[3] ? $m[3] : $m[4];
    unset($needed_parts[$m[1]]);
}

echo $data;
