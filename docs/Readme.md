<article>

<header>

# mod_xsendfile for Apache2

</header>

<section>

## Overview

mod_xsendfile is a small Apache2 module that processes X-SENDFILE headers output handlers might have registered.

If it encounters the presence of such header it will discard all output and send the file specified by that header instead using Apache internals including all optimizations like caching-headers and sendfile or mmap if configured.

It is useful for processing script-output of e.g. php, perl, python or any *cgi.

## Useful?

Yep, it is useful.

*   Some applications require checking for special privileges.
*   Other have to lookup values first (e.g.. from a DB) in order to correctly process a download request.
*   Or store values (download-counters come into mind).
*   etc.

### Benefits

*   Uses apache internals
*   Optimal delivery through sendfile and mmap (if available).
*   Sets correct cache headers such as Etag and If-Modified-Since as if the file was statically served.
*   Processes cache headers such as If-None-Match or If-Modified-Since.
*   Support for ranges.

</section>

<section>

## Installation

1.  Grab the source.
2.  Compile and install
    *   In general:  
        `apxs -cia mod_xsendfile.c`
    *   Debian/Ubuntu uses apxs2:  
        `apxs2 -cia mod_xsendfile.c`
    *   Mac users might want to build fat binaries:  
        `apxs -cia -Wc,"-arch i386 -arch x86_64" -Wl,"-arch i386 -arch x86_64" mod_xsendfile.c`
3.  Restart apache
4.  That's all.

</section>

<section>

## Configuration

### Headers

*   `X-SENDFILE` - Send the file referenced by this headers instead of the current response body
*   `X-SENDFILE-TEMPORARY` - Like `X-SENDFILE`, but the file will be deleted afterwards. The file must originate from a path that has the `AllowFileDelete` flag set.

### XSendFile

<table class="code directive">

<tbody>

<tr>

<th>Description</th>

<td>Enables or disables header processing</td>

</tr>

<tr>

<th>Syntax</th>

<td>XSendFile on|off</td>

</tr>

<tr>

<th>Default</th>

<td>XSendFile off</td>

</tr>

<tr>

<th>Context</th>

<td>server config, virtual host, directory, .htaccess</td>

</tr>

</tbody>

</table>

Setting `XSendFile on` will enable processing.

The file specified in `X-SENDFILE` header will be sent instead of the handler output.

The value (file name) given by the header is assmumed to be url-encoded, i.e. unescaping/url-decoding will be performed. See [XSendFileUnescape](#XSendFileUnescape).  
If you happen to store files using already url-encoded file names, you must "double" encode the names... `%20 -> %2520`

If the response lacks the `X-SENDFILE` header the module will not perform any processing.

### XSendFileIgnoreEtag

<table class="code directive">

<tbody>

<tr>

<th>Description</th>

<td>Ignore script provided Etag headers</td>

</tr>

<tr>

<th>Syntax</th>

<td>XSendFileIgnoreEtag on|off</td>

</tr>

<tr>

<th>Default</th>

<td>XSendFileIgnoreEtag off</td>

</tr>

<tr>

<th>Context</th>

<td>server config, virtual host, directory, .htaccess</td>

</tr>

</tbody>

</table>

Setting `XSendFileIgnoreEtag on` will ignore all ETag headers the original output handler may have set.  
This is helpful for applications that will generate such headers even for empty content.

### XSendFileIgnoreLastModified

<table class="code directive">

<tbody>

<tr>

<th>Description</th>

<td>Ignore script provided LastModified headers</td>

</tr>

<tr>

<th>Syntax</th>

<td>XSendFileIgnoreLastModified on|off</td>

</tr>

<tr>

<th>Default</th>

<td>XSendFileIgnoreLastModified off</td>

</tr>

<tr>

<th>Context</th>

<td>server config, virtual host, directory, .htaccess</td>

</tr>

</tbody>

</table>

Setting `XSendFileIgnoreLastModified on` will ignore all Last-Modified headers the original output handler may have set.  
This is helpful for applications that will generate such headers even for empty content.

### XSendFileUnescape

<table class="code directive">

<tbody>

<tr>

<th>Description</th>

<td>Unescape/url-decode the value of the header</td>

</tr>

<tr>

<th>Syntax</th>

<td>XSendFileUnescape on|off</td>

</tr>

<tr>

<th>Default</th>

<td>XSendFileUnescape on</td>

</tr>

<tr>

<th>Context</th>

<td>server config, virtual host, directory, .htaccess</td>

</tr>

</tbody>

</table>

Setting `XSendFileUnescape off` will restore the pre-1.0 behavior of using the raw header value, instead of trying to unescape/url-decode first.  
Headers may only contain a certain ASCII subset, as dictated by the corresponding RFCs/protocol. Hence you should escape/url-encode (and have XSendFile unescape/url-decode) the header value. Failing to keep within the bounds of that ASCII subset might cause errors, depending on your application framework.

Hence this setting is meant only for backwards-compatibility with legacy applications expecting the old behavior; new applications should url-encode the value correctly and leave `XSendFileUnescape on`. Of course, if your paths are always ASCII, then (usually) no special encoding is required.

### XSendFilePath

<table class="code directive">

<tbody>

<tr>

<th>Description</th>

<td>White-list more paths</td>

</tr>

<tr>

<th>Syntax</th>

<td>XSendFilePath `<absolute path>` [`AllowFileDelete`]</td>

</tr>

<tr>

<th>Default</th>

<td>None</td>

</tr>

<tr>

<th>Context</th>

<td>server config, virtual host, directory</td>

</tr>

</tbody>

</table>

XSendFilePath allow you to add additional paths to some kind of white list. All files within these paths are allowed to get served through mod_xsendfile.

Provide an absolute path as Parameter to this directive.

If the optional `AllowFileDelete` flag is specified, then files under this path can be served using the `X-SENDFILE-TEMPORARY` header, and will then be deleted once the file is delievered. Hence you should only set the `AllowFileDelete` flag for paths that do not hold any files that shouldn't be deleted!

You may provide more than one path.

#### Remarks - Relative paths

The current working directory (if it can be determined) will be always checked first.

If you provide relative paths via the X-SendFile header, then all whitelist items will be checked until a seamingly valid combination is found, i.e. the result is within the bounds of the whitelist item; it isn't checked at this point if the path in question actually exists.  
Considering you whitelisted `/tmp/pool` and `/tmp/pool2` and your script working directory is `/var/www`.

`X-SendFile: file`

1.  `/var/www/file` - Within bounds of `/var/www`, OK

`X-SendFile: ../pool2/file`

1.  `/var/www/../pool2/file = /var/pool2/file` - Not within bounds of `/var/www`
2.  `/tmp/pool/../pool2/file = /tmp/pool2/file` - Not within bounds of `/tmp/pool`
3.  `/tmp/pool2/../pool2/file = /tmp/pool2/file` - Within bounds of `/tmp/pool2`, OK

You still can only access paths that are whitelisted. However you have might expect a different behavior here, hence the documentation.

**Please note:** It is recommended to always use absolute paths.

#### Remarks - Inheritance

The white list "inherits" entries from higher level configuration.  

<pre class="code">XSendFilePath /tmp
<VirtualHost *>
  ServerName someserver
  XSendFilePath /home/userxyz
</VirtualHost>
<VirtualHost *>
  ServerName anotherserver
  XSendFilePath /var/www/somesite/
  <Directory /var/www/somesite/fastcgis>
    XSendFilePath /var/www/shared
  </Directory>
</VirtualHost></pre>

Above example will give:

*   *
    *   `/tmp`
*   someserver
    *   `/tmp`
    *   `/home/userxyz`
*   another
    *   `/tmp`
    *   `/var/www/somesite`
    *   `/var/www/shared` (for scripts* located in /var/www/somesite/fastcgis)

*) Scripts, in this context, mean the actual script-starters. E.g. PHP as a handler will use the .php itself, while in CGI mode refers to the starter.

_Windows_ users must include the drive letter to those paths as well. Tests show that it has to be in upper-case.

### Example

`.htaccess`

<pre><Files out.php>
XSendFile on
</Files></pre>

`out.php`

`<span style="color: rgb(0, 0, 0);"><span style="color: rgb(0, 0, 187);"><?php  
</span><span style="color: rgb(0, 119, 0);">...  
if (</span><span style="color: rgb(0, 0, 187);">$user</span><span style="color: rgb(0, 119, 0);">-></span><span style="color: rgb(0, 0, 187);">isLoggedIn</span><span style="color: rgb(0, 119, 0);">())  
{  
    </span><span style="color: rgb(0, 0, 187);">header</span><span style="color: rgb(0, 119, 0);">(</span><span style="color: rgb(221, 0, 0);">"X-Sendfile: $path_to_somefile"</span><span style="color: rgb(0, 119, 0);">);  
    </span><span style="color: rgb(0, 0, 187);">header</span><span style="color: rgb(0, 119, 0);">(</span><span style="color: rgb(221, 0, 0);">"Content-Type: application/octet-stream"</span><span style="color: rgb(0, 119, 0);">);  
    </span><span style="color: rgb(0, 0, 187);">header</span><span style="color: rgb(0, 119, 0);">(</span><span style="color: rgb(221, 0, 0);">"Content-Disposition: attachment; filename=\"$somefile\""</span><span style="color: rgb(0, 119, 0);">);  
    exit;  
}  
</span><span style="color: rgb(0, 0, 187);">?>  
</span><h1>Permission denied</h1>  
<p>Login first!</p></span>`

## Limitations / Issues / Security considerations

*   The `Content-Encoding` header - if present - will be dropped, as the module cannot know if it was set by intention of the programmer or the handler. E.g. php with output compression enabled will set this header, but the replacement file send via mod_xsendfile is most likely not compressed.
*   The header (X-SENDFILE) is not case-sensitive.
*   **X-Sendfile will also happily send files that are otherwise protected (e.g. Deny from all).**  

</section>

<section>

## Credits

The idea comes from [lighttpd](http://www.lighttpd.net/) - <span style="font-style: italic;">A fast web server with minimal memory footprint</span>.

The module itself was inspired by many other Apache2 modules such as mod_rewrite, mod_headers and obviously core.c.

## License

**Copyright 2006-2012 by Nils Maier**

Licensed under the _Apache License, Version 2.0_ (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at  
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and limitations under the License.

## Changes

### Version 1.0

*   Unescape/url-decode header value to support non-ascii file names
*   `XSendFileUnescape` setting, to support legacy applications
*   `X-SENDFILE-TEMPORARY` header and corresponding `AllowFileDelete` flag
*   Fix: Actually look into the backend-provided headers for Last-Modified

### Version 0.12

*   Now incorrect headers will be dropped early

### Version 0.11.1

*   Fixed some documentation bugs
*   Built win32 binaries against latest httpd using MSVC9
*   Updated MSVC Project files

### Version 0.11

*   Fixed large file support

### Version 0.10

*   Won't override Etag/Last-Modified if already set.
*   New Configuration directive: XSendFileIgnoreEtag
*   New Configuration directive: XSendFileIgnoreLastModified
*   New Configuration directive: XSendFilePath
*   Removed Configuration directive: XSendFileAllowAbove  
    Use XSendFilePath instead.
*   Improved header handling for FastCGI/CGI output (removing duplicate headers).

### Version 0.9

*   New configuration directive: XSendFileAllowAbove
*   Initial FastCGI/CGI support
*   Filter only added when needed

### Version 0.8

*   This is the initial public release.

</section>

</article>
