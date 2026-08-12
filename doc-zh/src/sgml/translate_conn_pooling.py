#!/usr/bin/env python3
"""Translate connection-pooling.sgml from English to Simplified Chinese."""

import re
import sys

INPUT_FILE = r"C:/Users/荷塘月色/AppData/Local/Temp/pgpool2-full/doc-zh/src/sgml/connection-pooling.sgml"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Define replacements as (old, new) tuples.
# We process text nodes (everything outside SGML tags) and apply these sequentially.
replacements = [
    # Section titles
    ("Connection Pooling", "连接池"),
    ("Connection Pooling Settings", "连接池设置"),
    ("Error Reporting and Logging", "错误报告与日志"),
    ("Where To Log", "日志位置"),
    ("When To Log", "日志记录时机"),
    ("What To Log", "日志记录内容"),

    # Connection Pooling section
    ("maintains established\n  connections to the PostgreSQL servers, and reuses them whenever a\n  new connection with the same properties (i.e. user name, database,\n  protocol version) comes in. It reduces the connection overhead,\n  and improves system's overall throughput.",
     "会保持与 PostgreSQL 服务器的已建立连接，并在有相同属性（即用户名、数据库、协议版本）的新连接到来时复用这些连接。这可以减少连接开销，并提高系统的整体吞吐量。"),

    ("Caches connections to backends when set to on. Default is on.",
     "设置为 on 时缓存到后端的连接。默认为 on。"),

    ("However, connections to ",
     "但是，即使 <varname>connection_cache</> 为 on，连接到 "),

    (" and ", "、"),

    (" databases are not cached even if",
     " 数据库的连接也不会被缓存。"),

    ("You need to restart ",
     "如果修改此值，需要重启 "),

    (" if you change this value.",
     "。"),

    ("The maximum number of cached connections\n       in each ",
     "每个 "),

    (" child\n       process. ",
     " 子进程中缓存连接的最大数量。"),

    (" reuses the\n       cached connection if an incoming connection is connecting\n       to the same database with the same user name and the same\n       run-time parameters.  If not,\n       ",
     " 在传入连接与同一数据库、同一用户名以及相同运行期参数连接时使用缓存连接。如果不是，"),

    (" creates a new\n       connection to the backend.  If the number of cached\n       connections exceeds max_pool, the oldest connection will\n       be discarded, and uses that slot for the new connection.",
     " 将创建一条新的后端连接。如果缓存连接数超过 max_pool，最旧的连接将被丢弃，并使用该位置来建立新连接。"),

    ("Default value is 4. Please be aware that the number of\n       connections from ",
     "默认值为 4。请注意，"),

    (" processes to the backends may reach\n       num_init_children * max_pool in total.",
     " 进程到后端的连接数总计可能达到 num_init_children * max_pool。"),

    ("This parameter can only be set at server start.",
     "此参数只能在服务器启动时设置。"),

    ("Specifies the length of connection queue from frontend to\n       ",
     "指定前端到"),

    (". The queue length (actually\n       ",
     " 的连接队列长度。队列长度（实际上是"),

    ("\"backlog\"", "\"backlog\""),

    (" parameter of ",
     " 系统调用的 "),

    (" system call) is defined as\n       ",
     "）定义为 "),

    (" * ",
     " * "),

    ("Some systems have the upper limit of the backlog parameter of\n       ",
     "某些系统对 "),

    (" system call.\n       See ",
     " 系统调用的 backlog 参数有上限限制。请参阅 "),

    (" for more details.",
     " 以了解更多详细信息。"),

    ("Default is 2.",
     "默认为 2。"),

    ("When set to on, ",
     "设置为 on 时，"),

    (" enables the serialization\n       on incoming client connections.",
     " 会对传入客户端连接启用序列化。"),

    ("Without serialization the OS kernel wakes up all of the ",
     "未启用序列化时，OS 内核会唤醒所有"),

    (" children processes to execute ",
     " 子进程来执行 "),

    (" and one of them\n       actually gets the incoming connection. The problem here is, because so my child\n       process wake up at a same time, heavy context switching occurs and the\n       performance is affected.",
     "，其中一个会实际获得传入连接。这里的问题是，因为如此多的子进程在同一时间被唤醒，会导致严重的上下文切换，从而影响性能。"),

    ("This phenomena is a well known classic problem called\n       \"the thundering herd problem\". This can be solved by the\n       serialization of the ",
     "这种现象是一个众所周知的经典问题，称为"惊群效应"（the thundering herd problem）。可以通过序列化 "),

    (" calls, so that only one\n       ",
     " 调用来解决，使得只有一个 "),

    (" process gets woken up\n       for incoming connection to execute the ",
     " 进程被唤醒来处理传入连接的 "),

    ("But serialization has its own overheads, and it is recommended\n       to be used only with the larger values of ",
     "但序列化本身也有开销，建议仅在 "),

    (".\n       For the small number of ",
     " 值较大时使用。对于 "),

    (",\n\tthe serialize accept can degrade the performance because of\n\tserializing overhead.",
     " 较小的情况，由于序列化开销，serialize_accept 反而可能降低性能。"),

    ("It is recommended to do a benchmark before deciding whether to use\n       ",
     "建议在决定是否使用 "),

    (" or not, because the correlation\n       of ",
     " 之前进行基准测试，因为 "),

    (" and ",
     " 与 "),

    ("\n\tcan be different on different environments.",
     " 之间的关系在不同环境下可能有所不同。"),

    ("When ",
     "当 "),

    (" is enabled, ",
     " 启用时，"),

    ("\thas no effect. Make sure that you set ",
     " 无效。请确保将 "),

    (" to 0 if you intend\n\t to turn on the ",
     " 设为 0，如果你打算开启 "),

    (".\n\t And if you are worried about ",
     "。另外，如果你担心 "),

    (" process memory leaks\n\t or whatever potential issue, you could use ",
     " 进程内存泄漏或其他潜在问题，可以使用 "),

    (" instead.\n\t  This is purely an implementation limitation and may be removed in the future.",
     " 代替。这纯粹是实现的限制，未来可能会移除。"),

    ("Default is off.",
     "默认为 off。"),

    ("Specifies the time in seconds to terminate\n       a ",
     "指定一个 "),

    ("\n       child process if it remains idle because no client is connecting to it.\n       The new child process\n       is immediately spawned by ",
     " 子进程在被终止前的空闲时间（秒），即没有客户端连接到它时。当子进程因为 "),

    (" when it\n       is terminated because of ",
     " 被终止时，"),

    (".\n       ",
     " 会立即生成一个新的子进程。"),

    (" is a measure to prevent the\n       memory leaks and other unexpected errors in ",
     " 是用于防止 "),

    ("\n\n       children.",
     " 子进程中内存泄漏和其他意外错误的措施。"),

    (" does not apply to\n       processes that have not accepted any connection yet.",
     " 不适用于尚未接受任何连接的进程。"),

    (" becomes ineffective when\n\t",
     " 在 "),

    (" is enabled.",
     " 启用时无效。"),

    ("Default is 300 (5 minutes) and setting it to 0 disables the feature.",
     "默认为 300（5 分钟），设为 0 则禁用该功能。"),

    ("Specifies the time in seconds to disconnect a client if it remains idle\n       since the last query.\n       This is useful for preventing the ",
     "指定最后一次查询后保持客户端空闲的超时时间（秒），超过该时间则断开客户端连接。这对于防止 "),

    ("\n       children from being occupied by a lazy clients or broken TCP/IP\n       connection between client and ",
     " 子进程被懒惰的客户端或客户端与 "),

    ("\n       between client and ",
     " 之间损坏的 TCP/IP 连接占用很有用。"),

    (" is ignored in\n       the second stage of online recovery.",
     " 在在线恢复的第二阶段会被忽略。"),

    ("The default is 0, which turns off the feature.",
     "默认为 0，表示关闭该功能。"),

    ("This parameter can be changed by reloading the ",
     "此参数可通过重新加载 "),

    (" configurations.",
     " 配置来更改。"),

    ("You can also use ",
     "也可以使用 "),

    (" command to alter the value of\n       this parameter for a current session.",
     " 命令来修改当前会话中此参数的值。"),

    ("Specifies the lifetime of a ",
     "指定 "),

    ("\n       child process in terms of the number of client connections it can receive.\n       ",
     " 子进程以客户端连接数为度量的生命周期。"),

    (" will terminate the child process\n       after it has served ",
     " 在服务的客户端连接数达到 "),

    (" client connections and will immediately spawn a new child process to take its place.",
     " 后将终止该子进程，并立即生成一个新的子进程接替其位置。"),

    (" is useful on a very busy server,\n       where ",
     " 在非常繁忙的服务器上很有用，此时 "),

    (" and ",
     " 和 "),

    ("\n\tnever gets triggered. It is also useful to prevent the ",
     " 都不会触发。它也用于防止 "),

    (" servers from getting\n\ttoo big.",
     " 服务器的连接数过大。"),

    ("The default is 0, which turns off the feature.",
     "默认为 0，表示关闭该功能。"),

    ("Specifies the time in seconds to terminate the cached connections\n       to the ",
     "指定终止到 "),

    (" backend. This serves as the cached connection expiration time.",
     " 后端缓存连接的超时时间（秒）。这用作缓存连接的过期时间。"),

    ("If a client connects to the process which holds the cached\n       connections, a calculation on\n       the ",
     "如果客户端连接到持有缓存连接的进程，则客户端断开连接之前不会计算 "),

    (" is not performed\n       until the client disconnects. Thus it is possible that the cached\n       connections are kept for longer time than this value. To avoid\n       this, it is recommended to set shorter value\n       to ",
     "。因此，缓存连接可能保持的时间长于该值。为避免这种情况，建议对 "),

    ("设置较短的值。"),

    ("The default is 0, which means the cached connections will not be\n       disconnected.",
     "默认为 0，表示缓存连接不会断开。"),

    ("Specifies the ",
     "指定退出用户会话时发送到后端以重置连接的 "),

    (" commands to be sent to reset the backend connection\n       when exiting the user session. Multiple commands can be specified by delimiting each\n       by ",
     " 命令。多个命令可通过 "),

    ("."),
     ("。"),

    ("\n       The available commands differ among ",
     "\n      可用的命令因 "),

    (" versions.",
     " 版本而异。"),

    ("\n       Below are some recommended settings for ",
     "\n      以下是针对不同 "),

    ("\n       on different ",
     " 版本的 "),

    ("\n       Note, however, that ",
     "\n      注意，"),

    (" command should be always included.",
     " 命令应始终包含在内。"),

    ("PostgreSQL version", "PostgreSQL 版本"),
    ("7.1 or earlier", "7.1 及更早版本"),
    ("7.2 to 8.2", "7.2 至 8.2"),
    ("8.3 or later", "8.3 及更新版本"),

    (" is not issued when not in a transaction block for 7.4 or later\n       ",
     " 对于 7.4 及更新版本的 PostgreSQL，若非事务块状态则不发出 "),

    ("Default is ",
     "默认为 "),

    # Logging section
    (" supports two destinations\n       for logging the ",
     " 支持两种记录 "),

    (" messages.\n       The supported log destinations are ",
     " 消息的日志目标。支持的日志目标为 "),

    (" and ",
     " 和 "),

    (". You can also set this parameter to a list\n       of desired log destinations separated by commas if you want the log messages\n       on the multiple destinations.",
     "。如果你希望在多个目标上记录日志，也可以用逗号分隔的设置列表来指定该参数。"),

    ("#for example to log on both syslog and stderr",
     "# 例如同时记录到 syslog 和 stderr"),

    ("The default is to log to ",
     "默认为仅记录到 "),

    (" only.",
     "。"),

    ("On some systems you will need to alter the configuration of your\n       system's ",
     "在某些系统上，你需要修改系统 "),

    (" daemon in order to make use of the\n       ",
     " 守护进程的配置才能使用 "),

    (" option\n       for ",
     " 选项。"),

    (" can log to ",
     " 可以记录到 "),

    (" facilities LOCAL0 through LOCAL7\n       (see ",
     " 设施 LOCAL0 到 LOCAL7（参见 "),

    ("), but the default\n\t",
     "），但大多数平台上的默认 "),

    ("\tconfiguration on most platforms will discard all such messages.\n\tYou will need to add something like:\n\t",
     " 配置会丢弃所有此类消息。你需要在 syslog 守护进程的配置文件中添加类似：\n\t"),

    ("\tto the syslog daemon's configuration file to make it work.",
     " 使其生效。"),

    ("This parameter enables the logging collector, which is a background process that captures\n\t log messages sent to stderr and redirects them into log files.",
     "此参数启用日志收集器，这是一个后台进程，用于捕获发送到 stderr 的日志消息并将其重定向到日志文件。"),

    ("It is possible to log to stderr without using the logging collector; the log messages will\n\t just go to wherever the server's stderr is directed. However, that method is only suitable\n\t for low log volumes, since it provides no convenient way to rotate log files.",
     "不使用日志收集器也可以记录到 stderr；日志消息将发送到服务器 stderr 所指向的位置。但是，这种方法仅适用于日志量较低的情况，因为它无法提供方便的日志文件轮换方式。"),

    ("This parameter can only be set at the Pgpool-II start.",
     "此参数只能在 Pgpool-II 启动时设置。"),

    (" is not available prior to\n       ",
     " 在 "),

    ("V4.2",
     "V4.2"),

    (".",
     "。"),

    ("When ",
     "当 "),

    (" is enabled, this parameter determines\n\t the directory in which log files will be created.",
     " 启用时，此参数决定日志文件的创建目录。"),

    ("The default is ",
     "默认为 "),

    ("When ",
     "当 "),

    (" is enabled, this parameter sets the\n\t file names of the created log files. The value is treated as a\n\t ",
     " 启用时，此参数设置创建日志文件的文件名。该值被视为 "),

    (" pattern, so %-escapes can be used to specify time-varying\n\t file names.\n\t The supported %-escapes are similar to those listed in the Open Group's\n\t ",
     " 模式，因此可使用 %-转义来指定随时间变化的文件名。支持的 %-转义与 Open Group 的 "),

    (" specification.",
     " 规范中列出的类似。"),

    ("If you specify a file name without escapes, you should plan to use a log rotation\n\t utility to avoid eventually filling the entire disk.",
     "如果你指定了不含转义的文件名，应计划使用日志轮换工具，以避免最终填满整个磁盘。"),

    ("The default is ",
     "默认为 "),

    ("This parameter sets the permissions for log files when ",
     "当 "),

    (" is enabled. The parameter value is expected to be a numeric mode specified in the format\n\t accepted by the ",
     " 启用时，此参数设置日志文件的权限。参数值应为 "),

    (" and ",
     " 和 "),

    (" system calls.",
     " 系统调用接受的格式的数值模式。"),

    ("To use the customary octal format the number must start with a 0 (zero).",
     "要使用常见的八进制格式，数字必须以 0（零）开头。"),

    (" is enabled, this parameter determines\n\t the maximum amount of time to use an individual log file, after which a new log\n\t file will be created. If this value is specified without units,\n\t it is taken as minutes. The default is 24 hours.",
     " 启用时，此参数决定单个日志文件的使用最长时长，超过该时长后将会创建新日志文件。如果未指定单位，则视为分钟。默认为 24 小时。"),

    ("Set to zero to disable time-based creation of new log files.",
     "设为 0 可禁用基于时间的日志文件创建。"),

    (" is enabled, this parameter determines\n\t the maximum size of an individual log file. After this many kilobytes have been\n\t emitted into a log file, a new log file will be created.",
     " 启用时，此参数决定单个日志文件的最大大小。向日志文件写入超过指定千字节数后，将创建新的日志文件。"),

    ("Set to zero to disable size-based creation of new log files.",
     "设为 0 可禁用基于大小的日志文件创建。"),

    (" is enabled,\n\t this parameter will cause ",
     " 启用时，此参数将使 "),

    (" to truncate (overwrite),\n\t rather than append to, any existing log file of the same name.\n\t However, truncation will occur only when a new file is being opened due to\n\t time-based rotation, not during the startup or size-based rotation.\n\t When off, pre-existing files will be appended to in all cases.\n\t For example, using this setting in combination with a ",
     " 截断（覆盖）任何同名现有日志文件，而不是追加到现有日志文件。但是，仅在因基于时间的轮换而打开新文件时才进行截断，而非在启动或基于大小的轮换时。关闭时，所有情况下都会追加到预存在的文件。例如，将此设置与 "),

    (" like pgpool-%H.log would result in generating twenty-four hourly log\n\t files and then cyclically overwriting them.",
     " 设置为 pgpool-%H.log 组合使用，将生成二十四个逐时日志文件，然后循环覆盖它们。"),

    ("See also the documentation of your system's syslog daemon.\n       When logging to ",
     "另请参阅你系统的 syslog 守护进程文档。启用向 "),

    (" is enabled,\n       this parameter determines the ",
     " 记录日志时，此参数决定要使用的 "),

    ("\n       \"facility\" to be used.\n       You can choose from ",
     " "facility"。可从 "),

    (", ",
     "、"),

    (";\n       the default is ",
     "；默认为 "),

    (".\n       See also the documentation of your system's ",
     "。另请参阅你系统的 "),

    (" daemon.",
     " 守护进程文档。"),

    ("When logging to ",
     "启用向 "),

    (" is enabled, this parameter determines\n       the program name used to identify ",
     " 记录日志时，此参数决定用于在 "),

    (" messages in ",
     " 日志中标识 "),

    (" logs. The default is ",
     " 消息的程序名。默认为 "),

    ("Controls which minimum message levels are sent to the client.\n       Valid values are ",
     "控制发送客户端的消息的最小级别。有效值为 "),

    (". Each level includes\n       all the levels that follow it. The default is ",
     "。每个级别包含其后的所有级别。默认为 "),

    ("Controls which minimum message levels are emitted to log.\n       Valid values are ",
     "控制输出到日志的消息的最小级别。有效值为 "),

    (".\n       Each level includes all the levels that follow it.\n       The default is ",
     "。每个级别包含其后的所有级别。默认为 "),

    ("Setting to on, prints all SQL statements to the log.",
     "设置为 on 时，将所有 SQL 语句打印到日志中。"),

    ("Similar to ",
     "类似于 "),

    (", except that it print the\n       logs for each DB node separately. It can be useful to make sure that\n       replication or load-balancing is working.",
     "，但会为每个数据库节点分别打印日志。这对于确保复制或负载均衡是否正常工作很有用。"),

    ("Similar to ",
     "类似于 "),

    (", except\n       that it prints the statement logs for each DB node separately as\n       a NOTICE message. With the\n       default ",
     "，但以 NOTICE 消息的形式为每个数据库节点分别打印语句日志。使用默认的 "),

    (" setting (that\n       is NOTICE), the log message will be printed on client's terminal\n       as well. This is convenient for clients because it does not need\n       to access ",
     " 设置（即 NOTICE）时，日志消息也会打印到客户端终端上。这对客户端很方便，因为它无需访问 "),

    (" log file.  Note\n       that\n       unlike ",
     " 日志文件。注意，与 "),

    (", ",
     " 不同，"),

    ("\n       does not print internal queries, (e.g., system catalog inquiry).\n       This is because this feature is designed to be used for testing\n       as well. As internal queries tend to be non-deterministic,\n       printing them in testing is not helpful. For the same reason,\n       backend process id is not printed.",
     " 不会打印内部查询（例如，系统目录查询）。这是因为此功能也用于测试。由于内部查询往往是非确定性的，在测试中打印它们并无帮助。出于同样的原因，后端进程 ID 也不会被打印。"),

    ("Setting to on, prints client messages to the log.",
     "设置为 on 时，将客户端消息打印到日志中。"),

    ("Setting to ",
     "设置为 "),

    ("\n       or ",
     " 或 "),

    (", prints backend messages to the\n       log.  With ",
     " 时，将后端消息打印到日志中。使用 "),

    (" the number of same kind of\n       messages are recorded and is printed when different kind of\n       messages is sent. Below is an example.",
     " 时，相同类型的消息数量会被记录，并在发送不同类型消息时打印。以下是一个示例。"),

    ("Thus the log will not be printed if the process corresponding to\n       the session is killed. If you want to print the log even in this\n       case, use ",
     "因此，如果对应会话的进程被杀死，日志将不会打印。如果你希望在此种情况下也打印日志，请使用 "),

    (" option. Note that with the\n       option each repeated message is printed and lots of log lines\n       are printed. The default is ",
     " 选项。注意，使用该选项时每条重复消息都会被打印，产生大量日志行。默认为 "),

    (", which\n       disables printing log messages from backend.",
     "，这会禁用来自后端的日志消息打印。"),

    ("Setting to on, prints the hostname instead of IP address\n       in the ",
     "设置为 on 时，在 "),

    (" command result, and connection logs\n       (when ",
     " 命令结果和连接日志（当 "),

    (" is on).",
     " 开启时）中以主机名代替 IP 地址。"),

    ("Setting to on, prints all client connections from to the log.",
     "设置为 on 时，将所有客户端连接打印到日志中。"),

    ("Setting to on, prints all client connection terminations to the log.",
     "设置为 on 时，将所有客户端连接终止打印到日志中。"),

    ("Setting to on, enable logging about normal PCP Process\n       fork and exit status. Default is off.",
     "设置为 on 时，启用关于正常 PCP 进程 fork 和退出状态的日志记录。默认为 off。"),

    ("Controls the amount of detail emitted for each message that is logged.\n       Valid values are ",
     "控制每条日志消息输出的详细程度。有效值为 "),

    (", ",
     "、"),

    ", and ",
     " 和 "),

    (",\n       each adding more fields\n       to displayed messages. ",
     "，每个级别在显示的消息中增加更多字段。"),

    " excludes the logging of ",
     " 不包含 "),

    (",\n       ",
     "、"),

    " and ",
     " 和 "),

    (" error information.",
     " 错误信息。"),

    ("This is a ",
     "这是一个 "),

    "-style string that is output at the beginning of\n       each log line.",
     " 风格的字符串，在每行日志的开头输出。"),

    ("\n       characters begin ",
     " 字符开始"),

    (" that are replaced\n       with information outlined below.\n       All unrecognized escapes are ignored. Other characters are copied straight to\n       the log line. Default is '%m: %a pid %p: ', which prints timestamp, application name and process id.",
     "，这些序列会被替换为下方概述的信息。所有未识别的转义将被忽略。其他字符直接复制到日志行。默认为 '%m: %a pid %p: '，它打印时间戳、应用程序名称和进程 ID。"),

    ("log_line_prefix escape options",
     "log_line_prefix 转义选项"),

    ("Escape", "转义"),
    ("Effect", "效果"),

    ("Application name. The initial value for child (session\n\t  process) is \"child\". If Clients set application name\n\t  (either in the startup message or by using SET command),\n\t  application name will be changed accordingly. In other types\n\t  of process, application name is a hard coded string. see\n\t  ",
     "应用程序名称。子进程（会话进程）的初始值为 \"child\"。如果客户端（在启动消息中或通过 SET 命令）设置了应用程序名称，应用程序名称将相应更改。在其他类型的进程中，应用程序名称是硬编码字符串。参见 "),

    ("Process ID (PID)",
     "进程 ID（PID）"),

    ("Process name",
     "进程名称"),

    ("Time stamp without milliseconds",
     "不含毫秒的时间戳"),

    ("Time stamp with milliseconds",
     "含毫秒的时间戳"),

    ("Database name",
     "数据库名称"),

    ("User name",
     "用户名"),

    ("Log line number for each process",
     "每个进程的日志行号"),

    ("'%' character",
     "'%' 字符"),

    ("application names in various process",
     "各进程中的应用名称"),

    ("Process type",
     "进程类型"),

    ("application name",
     "应用程序名称"),

    ("main", "main"),
    ("child", "child"),

    ("streaming replication delay check worker",
     "流复制延迟检查工作进程"),

    ("sr_check_worker",
     "sr_check_worker"),

    ("watchdog heart beat sender",
     "watchdog 心跳发送方"),

    ("heart_beat_sender",
     "heart_beat_sender"),

    ("watchdog heart beat receiver",
     "watchdog 心跳接收方"),

    ("heart_beat_receiver",
     "heart_beat_receiver"),

    ("watchdog", "watchdog"),

    ("watchdog life check",
     "watchdog 健康检查"),

    ("life_check",
     "life_check"),

    ("follow primary child",
     "跟随主节点子进程"),

    ("follow_child",
     "follow_child"),

    ("watchdog utility",
     "watchdog 工具进程"),

    ("watchdog_utility",
     "watchdog_utility"),

    ("pcp main", "pcp main"),
    ("pcp_main", "pcp_main"),
    ("pcp child", "pcp child"),
    ("pcp_child", "pcp_child"),

    ("health check process",
     "健康检查进程"),

    ("health_check%d (%d is replaced with backend node id)",
     "health_check%d (%d 由后端节点 ID 替换)"),

    ("logger process",
     "日志记录进程"),

    ("logger (Note that the application name \"logger\" will not be output to the log file managed by logger process)",
     "logger（注意：应用程序名称 \"logger\" 不会输出到 logger 进程管理的日志文件中）"),

    ("logger", "logger"),

    ("To run the ",
     "运行 "),

    (" use the following\n       command.",
     " 的命令如下。"),

    ("\n       Here, ",
     "。这里，"),

    (" tells ",
     " 告诉 "),

    (" to connect\n       to database each time a transaction gets executed. ",
     " 每次事务执行时都连接到数据库。"),

    ("\n       specifies the number of the concurrent sessions to ",
     " 指定了并发连接到 "),

    (".\n       You should change this according to your system's requirement.\n       After ",
     " 的会话数。你应该根据系统需求调整此值。"),

    (" finishes, check the number from\n       \"including connections establishing\".",
     " 完成后，从 \"including connections establishing\" 中检查数值。"),

    ("using pgbench to decide if serialize_accept should be used",
     "使用 pgbench 判断是否应使用 serialize_accept"),

    # Table headings
    ("Recommended setting for ",
     "的推荐设置"),

    # Various remaining
    ("\n       on different PostgreSQL versions",
     "不同 PostgreSQL 版本下"),

    ("\n       Note, however, that ",
     "注意，"),

    (" command should be always included.",
     " 命令应始终包含在内。"),

    ("\n        is not issued when not in a transaction block for 7.4 or later\n       ",
     " 对于 7.4 及更新版本的 PostgreSQL，若非事务块状态则不发出 "),

    # Remove any remaining raw English phrases inside text nodes
    ("\n        #for example to log on both syslog and stderr",
     "\n        # 例如同时记录到 syslog 和 stderr"),
]

def translate_text(text):
    """Apply all replacements to a text node."""
    for old, new in replacements:
        text = text.replace(old, new)
    return text

# Split content into text nodes and tag nodes, translate text nodes
result = []
i = 0
while i < len(content):
    if content[i] == '<':
        j = content.find('>', i)
        if j != -1:
            result.append(content[i:j+1])
            i = j + 1
        else:
            result.append(content[i])
            i += 1
    else:
        j = content.find('<', i)
        if j == -1:
            result.append(translate_text(content[i:]))
            i = len(content)
        else:
            result.append(translate_text(content[i:j]))
            i = j

translated = ''.join(result)

with open(INPUT_FILE, "w", encoding="utf-8") as f:
    f.write(translated)

print("Translation complete. File saved.")