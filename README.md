提取北京联通IPTV抓包频道数据

#概述
本项目是本人，一个代码小白用TraeCN写出来的数据处理项目。仅用于在北京联通宽带IPTV机顶盒所在网络抓取的频道数据json文件中提取出适合IPTV、TiViMate等安卓手机、平板和TV软件播放的m3u文件，以及适合tvbox、OK影视等安卓手机、平板和TV软件播放的txt文件。

#本项目包含以下文件
##1. 主要文件
get_iptv_data.py：Python脚本，用于从json文件中提取IPTV频道数据。
channeldata.json：北京联通IPTV抓包频道数据json文件，包含所有IPTV频道的信息。
channel_mapping_utf8.csv：IPTV频道名称映射为EPG节目表的csv文件，用于将原始频道名称映射为EPG节目表名称，同时也作为iptv.m3u文件的频道排序表。

##2. 工作过程文件
iptv_discarded.csv：包含所有被丢弃的IPTV频道，主要测试、购物、标清、无信号等非正常频道。
iptv_discarded.m3u：则是将抛弃的频道也写入m3u文件，主要是为了方便查看是否有新增或被误抛的频道，以便加入到channel_mapping_utf8.csv文件中。

##3. 成果文件
iptv.m3u：适合IPTV、TiViMate等安卓手机、平板和TV软件播放的m3u文件，包含所有IPTV频道的播放地址。
iptv.txt：适合tvbox、OK影视等安卓手机、平板和TV软件播放的txt文件，包含所有IPTV频道的播放地址。

#使用方法
##1. 确保已安装Python 3.x版本。
##2. 下载或克隆本项目到本地。
##3. 在项目目录下，运行以下命令安装依赖：
pip install requests
##4. 运行get_iptv_data.py脚本，提取IPTV频道数据：
python get_iptv_data.py
##5. 脚本运行完成后，在项目目录下会生成iptv.m3u和iptv.txt文件，以及iptv_discarded.csv和iptv_discarded.m3u文件。
插入图片
![image.png](images/ScreenShot_2025-11-30_162231_611.png)

#IPTV频道数据抓包方法
##1. 确保已安装Wireshark等抓包工具。
##2. 启动抓包工具，设置过滤规则，仅捕获机顶盒IP相关的数据包。
##3. 打开北京联通IPTV机顶盒，连接到网络，看几个频道3-5分钟。关键是从开机开始，这样收的数据包才是完整的。
##4. 在抓包工具中，http contains "ChannelName" or http contains "ChannelURL" or http contains "igmp://" 查看并过滤出IPTV相关的数据包。就在“Info”列中包含有”JSON（application/json）“的数据包。选中这条数据，右键选择“追踪流”->“HTTP Stream”，即可查看该数据包的详细内容，其中有IPTV频道的信息的就是。
##5. 选中有频道数据的json记录，菜单“文件”中“导出对象”--“HTTP...“，弹窗”文本过滤器“输入”channel“，选中”ChannelAquire“字节数为xxKB的就是可提取的频道数据，保存为json文件。
