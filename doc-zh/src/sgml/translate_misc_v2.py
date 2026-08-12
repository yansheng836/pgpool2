#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate misc-config.sgml text content to Simplified Chinese."""
import sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src = r'C:/Users/荷塘月色/AppData/Local/Temp/pgpool2-full/doc-zh/src/sgml/misc-config.sgml'

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# Use line-by-line approach: for each <para>, translate its text content
lines = content.split('\n')
result = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Handle <title> tags
    if '<title>' in line and '</title>' in line:
        result.append(re.sub(r'<title>(.*?)</title>', r'<title>杂项配置参数</title>', line))
        i += 1
        continue

    # Check if this line starts a <para> block that needs translation
    # We process each <para> element fully
    if stripped == '<para>':
        para_lines = ['<para>']
        i += 1
        indent_level = None
        while i < len(lines):
            cur = lines[i]
            cur_stripped = cur.strip()
            if cur_stripped == '</para>':
                para_lines.append('</para>')
                break
            # Determine indentation from first non-empty line
            if indent_level is None and cur_stripped:
                indent_level = len(cur) - len(cur.lstrip())
            para_lines.append(cur)
            i += 1
        # Translate the para content
        result.extend(_translate_para(para_lines))
        i += 1
        continue

    result.append(line)
    i += 1


def _translate_para(para_lines):
    """Translate a list of lines forming a <para> element."""
    # Join content, translate key phrases, then reformat with proper indentation
    raw_text = '\n'.join(para_lines[1:-1])  # exclude <para> and </para>
    translated = _translate_text(raw_text)
    # Rebuild with original indentation pattern (use first line's indent)
    if para_lines:
        first_line = para_lines[0]  # <para>
        last_line = para_lines[-1]  # </para>
        indent = len(first_line) - len(first_line.lstrip()) if first_line.strip() else 5
    else:
        indent = 5

    result = [first_line]
    for tline in translated.split('\n'):
        if tline.strip() == '':
            result.append(' ' * indent)
        else:
            result.append(' ' * indent + tline)
    result.append(last_line)
    return result


def _translate_text(text):
    """Apply all translation substitutions to text content."""
    # relcache_expire para (multi-line)
    old = """Specifies the relation cache expiration time in seconds.
     The relation cache is used for caching the query result of
     <productname>PostgreSQL</> system catalogs that is used by <productname>Pgpool-II
     </productname> to get various information including the table
     structures and to check table types(e.g. To check if the referred
     table is a temporary table or not). The cache is maintained in
     the local memory space of <productname>Pgpool-II</productname>
     child process and its lifetime is same as of the child process.
     The cache is also maintained in shared memory to share among child
     processes,if enable  <xref linkend="guc-enable-shared-relcache">
      So If the table is modified using <command>ALTER TABLE</command>
      or some other means, the relcache becomes inconsistent.
      For this purpose, <varname>relcache_expire</varname> controls
      the life time of the cache.
      Default is 0, which means the cache never expires."""
    new = "指定关系缓存的过期时间（秒）。关系缓存用于缓存 <productname>PostgreSQL</productname> 系统目录的查询结果，<productname>Pgpool-II</productname> 通过该缓存获取包括表结构在内的各种信息，并检查表类型（例如，检查被引用的表是否为临时表）。缓存存储在 <productname>Pgpool-II</productname> 子进程的本地内存空间中，其生命周期与子进程相同。如果启用了 <xref linkend="guc-enable-shared-relcache">，缓存还会保存在共享内存中以在子进程间共享。因此，如果使用 <command>ALTER TABLE</command> 或其他方式修改了表，关系缓存将变得不一致。为此，<varname>relcache_expire</varname> 控制缓存的生命周期。默认值为 0，表示缓存永不过期。"
    text = text.replace(old, new)

    text = text.replace(
        "This parameter can only be set at server start.",
        "此参数只能在服务器启动时设置。")

    text = text.replace(
        """Specifies the number of relcache entries. Default is 256.
     The cache is created  about 10 entries per table. So you can estimate
     the required number of relation cache at "number of using table * 10".""",
        "指定 relcache 条目的数量。默认为 256。每个表大约创建 10 个缓存条目。因此可以按「使用表数量 × 10」来估算所需的关系缓存大小。")

    text = text.replace(
        """If the below message frequently appears in the
      <productname>Pgpool-II</productname> log, you may need to
      increase the <varname>relcache_size</varname> for better performance.""",
        "如果以下消息在 <productname>Pgpool-II</productname> 日志中频繁出现，则可能需要增大 <varname>relcache_size</varname> 以改善性能。")

    text = text.replace(
        """By setting to on, relation cache is shared among
     <productname>Pgpool-II</productname> child processes using the in
     memory query cache (see <xref
     linkend="runtime-in-memory-query-cache-enabling"> for more
     details). Default is on. Each child process needs to access to
     the system catalog from <productname>PostgreSQL</productname>.
     By enabling this feature, other process can extract the catalog
     lookup result from the query cache and it should reduce the
     frequency of the query. Cache invalidation is not happen even if
     the system catalog is modified. So it is strongly recommend to
     set time out base cache invalidation by using <xref
     linkend="guc-relcache-expire"> parameter.""",
        "设置为 on 后，关系缓存将在 <productname>Pgpool-II</productname> 子进程间通过内存查询缓存共享（详见 <xref linkend="runtime-in-memory-query-cache-enabling">）。默认为 on。每个子进程都需要访问 <productname>PostgreSQL</productname> 的系统目录。启用此功能后，其他进程可以从查询缓存中提取目录查找结果，从而降低查询频率。即使修改了系统目录，缓存也不会自动失效，因此强烈建议配合使用 <xref linkend="guc-relcache-expire"> 参数设置基于超时的缓存失效机制。")

    text = text.replace(
        """This parameter can be used even if <xref
     linkend="guc-memory-cache-enabled"> is off.  In this case some
     query cache parameters(<xref linkend="guc-memqcache-method">,
     <xref linkend="guc-memqcache-maxcache"> and each cache storage
     parameter) is used together.""",
        "即使 <xref linkend="guc-memory-cache-enabled"> 为 off，此参数仍可使用。此时会一并使用某些查询缓存参数（<xref linkend="guc-memqcache-method">、<xref linkend="guc-memqcache-maxcache"> 及各缓存存储参数）。")

    text = text.replace(
        """<productname>Pgpool-II</productname> search the local relation
     cache first. If it is not found on the cache, the shared relation
     query cache is searched if this feature is enabled. If it is
     found on query cache, it is copied into the local relation
     cache. If a cache entry is not found on anywhere,
     <productname>Pgpool-II</productname> executes the query against
     <productname>PostgreSQL</productname>, and the result is stored
     into the shared relation cache and the local cache.""",
        "<productname>Pgpool-II</productname> 首先搜索本地关系缓存。如果在本地缓存中未找到，且此功能已启用，则会搜索共享关系查询缓存。如果在查询缓存中找到，则将其复制到本地关系缓存中。如果在任何地方都未找到缓存条目，<productname>Pgpool-II</productname> 将向 <productname>PostgreSQL</productname> 执行查询，并将结果存储到共享关系缓存和本地缓存中。")

    text = text.replace(
        """The target node to send queries to create relation cache
     entries. If set to <literal>primary</literal>, queries will
     be sent to primary node. This is the default and
     recommended to most users because the query could get the
     latest information.  If you want to lower the load of
     primary node, you can set the parameter to
     <literal>load_balance_node</literal>, which will send
     queries to the load balance node. This is especially useful
     for such a system
     where <productname>Pgpool-II</productname>/primary server is
     on a continent A while
     other <productname>Pgpool-II</productname>/standby server is
     on other continent B. Clients on B want read data from the
     standby because it's much geographically closer. In this
     case you can set backend_weight0 (this represents primary)
     to 0, backend_weight1 to 1 (this represents standby) and set
     relcache_query_target
     to <literal>load_balance_node</literal>.""",
        "创建关系缓存条目时发送查询的目标节点。如果设置为 <literal>primary</literal>，查询将发送到主节点。这是默认值，也是大多数用户推荐的选择，因为查询可以获取最新信息。如果要降低主节点的负载，可以将参数设置为 <literal>load_balance_node</literal>，将查询发送到负载均衡节点。对于 <productname>Pgpool-II</productname>/主服务器位于 A 大陆而其他 <productname>Pgpool-II</productname>/备服务器位于 B 大陆的系统，这一选项尤其有用。B 大陆的客户端希望从备库读取数据，因为它地理位置更近。此时可将 backend_weight0（代表主节点）设为 0，backend_weight1（代表备节点）设为 1，并将 relcache_query_target 设置为 <literal>load_balance_node</literal>。")

    text = text.replace(
        """Note, however, if you send query to the standby node,
     recently created tables and rows might not be available on
     the standby server yet because of replication delay. Thus
     such a configuration is not recommended for systems where
     data modification activity is high.""",
        "需要注意的是，如果向备节点发送查询，由于复制延迟，刚创建的表和行在备服务器上可能还不可用。因此，对于数据修改活动频繁的系统，不建议采用这种配置。")

    text = text.replace(
        "This parameter can be changed by reloading\n     the <productname>Pgpool-II</> configurations.",
        "通过重新加载 <productname>Pgpool-II</productname> 配置可以更改此参数。")

    text = text.replace(
        """Setting to <literal>catalog</literal>
     or <literal>trace</literal>, enables the temporary table
     check in the <acronym>SELECT</acronym> statements. To check
     the temporary table <productname>Pgpool-II</productname>
     queries the system catalog of
     primary/main <productname>PostgreSQL</productname> backend
     if <literal>catalog</literal> is specified, which
     increases the load on the primary/main server.""",
        "设置为 <literal>catalog</literal> 或 <literal>trace</literal>，可启用 <acronym>SELECT</acronym> 语句中的临时表检查。如果指定 <literal>catalog</literal>，<productname>Pgpool-II</productname> 会查询主 <productname>PostgreSQL</productname> 后端的系统目录来检查临时表，这会增加主服务器的负载。")

    text = text.replace(
        """If <literal>trace</literal> is
     set, <productname>Pgpool-II</productname> traces temporary
     table creation and dropping to obtain temporary table
     info. So no need to access system catalogs. However, if
     temporary table creation is invisible
     to <productname>Pgpool-II</productname> (done in functions
     or triggers, for
     example), <productname>Pgpool-II</productname> cannot
     recognize the creation of temporary tables.""",
        "如果设置为 <literal>trace</literal>，<productname>Pgpool-II</productname> 会跟踪临时表的创建和删除操作以获取临时表信息，因此无需访问系统目录。但是，如果临时表的创建对 <productname>Pgpool-II</productname> 不可见（例如在函数或触发器中完成），则 <productname>Pgpool-II</productname> 无法识别临时表的创建。")

    text = text.replace(
        "If you are absolutely sure that your system never uses\n     temporary tables, then you can safely set to none.",
        "如果您确定系统中永远不会使用临时表，则可以安全地设置为 none。")

    text = text.replace(
        """For a backward compatibility sake for 4.0 or
      before, <productname>Pgpool-II</productname>
      accepts <literal>on</literal>, which is same
      as <literal>catalog</literal> and <literal>off</literal>,
      which is same as <literal>none</literal>, they may be
      deleted in the future version.""",
        "为兼容 4.0 及更早版本，<productname>Pgpool-II</productname> 接受 <literal>on</literal>（与 <literal>catalog</literal> 相同）和 <literal>off</literal>（与 <literal>none</literal> 相同），它们可能会在未来的版本中被删除。")

    text = text.replace(
        "Default is <literal>catalog</literal>.",
        "默认为 <literal>catalog</literal>。")

    text = text.replace(
        """This parameter can be changed by reloading
     the <productname>Pgpool-II</productname> configurations.
     You can also use <xref linkend="SQL-PGPOOL-SET"> command to
      alter the value of this parameter for a current session.""",
        "通过重新加载 <productname>Pgpool-II</productname> 配置可以更改此参数。您也可以使用 <xref linkend="SQL-PGPOOL-SET"> 命令在当前会话中更改此参数的值。")

    text = text.replace(
        """Setting to on, enables the unlogged table check in the <acronym>SELECT</acronym>
     statements. To check the unlogged table <productname>Pgpool-II</productname>
     queries the system catalog of primary/main <productname>PostgreSQL</> backend which increases
     the load on the primary/main server.
     If you are absolutely sure that your system never uses the unlogged tables
     (for example, you are using 9.0 or earlier version of <productname>PostgreSQL</>) then you
     can safely turn off the <varname>check_unlogged_table</varname>.
     Default is on.""",
        "设置为 on，可启用 <acronym>SELECT</acronym> 语句中的未记录表检查。如需检查未记录表，<productname>Pgpool-II</productname> 会查询主 <productname>PostgreSQL</productname> 后端的系统目录，这会增加主服务器的负载。如果您确定系统中永远不会使用未记录表（例如，您使用的是 9.0 或更早版本的 <productname>PostgreSQL</productname>），则可以安全地关闭 <varname>check_unlogged_table</varname>。默认为 on。")

    text = text.replace(
        """This parameter can be changed by reloading the <productname>Pgpool-II</> configurations.
     You can also use <xref linkend="SQL-PGPOOL-SET"> command to alter the value of
      this parameter for a current session.""",
        "通过重新加载 <productname>Pgpool-II</productname> 配置可以更改此参数。您也可以使用 <xref linkend="SQL-PGPOOL-SET"> 命令在当前会话中更改此参数的值。")

    text = text.replace(
        """Specifies the full path to a file to store the <productname>Pgpool-II
     </productname> process id.
     The pid_file_name path can be specified as relative to the
     location of pgpool.conf file or as an absolute path
     Default is <literal>"/var/run/pgpool/pgpool.pid"</literal>.""",
        "指定用于存储 <productname>Pgpool-II</productname> 进程 ID 的文件完整路径。pid_file_name 路径可以相对于 pgpool.conf 文件位置指定，也可以使用绝对路径。默认为 <literal>"/var/run/pgpool/pgpool.pid"</literal>。")

    text = text.replace(
        """Specifies the full path to a directory to store the <literal>pgpool_status</literal>.
     Default is <literal>'/tmp'</literal>.""",
        "指定用于存储 <literal>pgpool_status</literal> 的目录完整路径。默认为 <literal>'/tmp'</literal>。")

    # health_check_test caution - uses TAB characters
    text = text.replace(
        "\tDo not set this parameter to on in a production\n\tenvironment. This feature is purely for testing purpose.\n",
        "请勿在生产环境中将此参数设置为 on。此功能仅用于测试目的。\n")

    text = text.replace(
        """Setting to on,
     enables the testing facility of health checking. In this case the
     health check process looks
     into <filename>backend_down_request</filename>
     under <xref linkend="guc-work-dir">.  The file may contain multiple
     lines, and each line corresponds to each backend. A line in the
     file starts with backend id (must be a decimal number starting
     with zero), then a TAB, and ends with "down". The backend is
     assumed in down status and <productname>Pgpool-II</productname>
     will start a failover. Once the failover completes, the "down" is
     rewritten to "already_down" by health check process to prevent
     repeating failovers.""",
        "设置为 on，可启用健康检查的测试功能。在这种情况下，健康检查进程会查看 <xref linkend="guc-work-dir"> 下的 <filename>backend_down_request</filename> 文件。该文件可能包含多行，每行对应一个后端。文件中的行以后端 ID 开头（必须是从小数 0 开始的十进制数），接着是一个 TAB，最后以 \"down\" 结尾。后端被假定为宕机状态，<productname>Pgpool-II</productname> 将启动故障转移。故障转移完成后，健康检查进程会将 \"down\" 改写为 \"already_down\" 以防止重复故障转移。")

    text = text.replace(
        """This feature is particularly useful for
     testing <xref linkend="guc-failover-require-consensus">. Suppose
     we have 3 watchdog node. Each watchdog checks healthiness of
     backend 0. By setting "0\tdown" in the file only under watchdog 0,
     other watchdogs disagree with the unhealthiness of backend 0, so
     failover will not occur. This kind of partial network failure can
     be simulated using this feature.""",
        "此功能对测试 <xref linkend="guc-failover-require-consensus"> 非常有用。假设我们有 3 个 watchdog 节点，每个 watchdog 检查后端 0 的健康状况。只在 watchdog 0 下的文件中设置 \"0\tdown\"，其他 watchdog 将不认同后端 0 不健康，因此不会发生故障转移。使用此功能可以模拟此类部分网络故障。")

    text = text.replace(
        "Default is <literal>off</literal>.",
        "默认为 <literal>off</literal>。")

    return text


# Process para elements
lines = content.split('\n')
result = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if stripped == '<para>':
        para_lines = ['<para>']
        i += 1
        indent = None
        while i < len(lines):
            cur = lines[i]
            cur_stripped = cur.strip()
            if cur_stripped == '</para>':
                para_lines.append('</para>')
                break
            if indent is None and cur_stripped:
                indent = len(cur) - len(cur.lstrip())
            para_lines.append(cur)
            i += 1
        translated_lines = _translate_para(para_lines)
        result.extend(translated_lines)
        i += 1
    else:
        result.append(line)
        i += 1

output = '\n'.join(result)

# Fix stray </> that slipped in from source
output = output.replace("</>", "</productname>")

with open(src, 'w', encoding='utf-8', newline='') as f:
    f.write(output)

print("Translation complete.")
print(f"Output length: {len(output)} chars")
