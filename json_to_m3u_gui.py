# 北京联通IPTV抓包数据的处理的程序
# 主要按表格生成m3u和txt两种播放列表，可用于IPTV、Tivimate等m3u或tvbox等txt播放

import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import csv

class JSONtoM3UGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON到M3U转换器")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # 设置窗口居中
        self.center_window()
        
        # 默认值
        self.default_udpxy_ip = "192.168.1.13"
        self.default_udpxy_port = "23234"
        self.default_protocol = "rtp"
        
        # 变量
        self.udpxy_ip_var = tk.StringVar(value=self.default_udpxy_ip)
        self.udpxy_port_var = tk.StringVar(value=self.default_udpxy_port)
        self.protocol_var = tk.StringVar(value=self.default_protocol)
        self.input_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()
        
        # 创建界面
        self.create_widgets()
    
    def center_window(self):
        # 获取屏幕宽高
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算窗口位置
        x = (screen_width - 500) // 2
        y = (screen_height - 500) // 2
        
        # 设置窗口位置
        self.root.geometry(f"500x500+{x}+{y}")
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="JSON到M3U转换器", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # udpxy配置
        udpxy_frame = ttk.LabelFrame(main_frame, text="udpxy配置", padding="10")
        udpxy_frame.pack(fill=tk.X, pady=10)
        
        # IP地址
        ip_label = ttk.Label(udpxy_frame, text="IP地址:")
        ip_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        ip_entry = ttk.Entry(udpxy_frame, textvariable=self.udpxy_ip_var, width=20)
        ip_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # 端口
        port_label = ttk.Label(udpxy_frame, text="端口:")
        port_label.grid(row=0, column=2, sticky=tk.W, pady=5)
        port_entry = ttk.Entry(udpxy_frame, textvariable=self.udpxy_port_var, width=10)
        port_entry.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)
        
        # 协议选择
        protocol_frame = ttk.LabelFrame(main_frame, text="协议选择", padding="10")
        protocol_frame.pack(fill=tk.X, pady=10)
        
        rtp_radio = ttk.Radiobutton(protocol_frame, text="RTP", variable=self.protocol_var, value="rtp")
        rtp_radio.pack(side=tk.LEFT, padx=10)
        
        udp_radio = ttk.Radiobutton(protocol_frame, text="UDP", variable=self.protocol_var, value="udp")
        udp_radio.pack(side=tk.LEFT, padx=10)
        
        # 文件选择
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        # 输入文件
        input_label = ttk.Label(file_frame, text="输入JSON文件:")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        input_entry = ttk.Entry(file_frame, textvariable=self.input_file_var, width=30)
        input_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        input_button = ttk.Button(file_frame, text="浏览", command=self.browse_input_file)
        input_button.grid(row=0, column=2, pady=5, padx=5)
        
        # 输出文件
        output_label = ttk.Label(file_frame, text="输出M3U文件:")
        output_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(file_frame, textvariable=self.output_file_var, width=30)
        output_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        output_button = ttk.Button(file_frame, text="浏览", command=self.browse_output_file)
        output_button.grid(row=1, column=2, pady=5, padx=5)
        
        # 进度标签
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.pack(pady=10)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # 确认按钮
        confirm_button = ttk.Button(button_frame, text="确认", command=self.convert, width=10)
        confirm_button.pack(side=tk.LEFT, padx=20)
        
        # 取消按钮
        cancel_button = ttk.Button(button_frame, text="取消", command=self.root.quit, width=10)
        cancel_button.pack(side=tk.LEFT, padx=20)
    
    def browse_input_file(self):
        file_path = filedialog.askopenfilename(
            title="选择输入JSON文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if file_path:
            self.input_file_var.set(file_path)
    
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title="选择输出M3U文件",
            filetypes=[("M3U文件", "*.m3u"), ("所有文件", "*.*")],
            defaultextension=".m3u"
        )
        if file_path:
            self.output_file_var.set(file_path)
    
    def convert(self):
        # 获取配置参数
        udpxy_ip = self.udpxy_ip_var.get()
        udpxy_port = self.udpxy_port_var.get()
        protocol = self.protocol_var.get()
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()
        
        # 验证参数
        if not input_file:
            messagebox.showerror("错误", "请选择输入JSON文件")
            return
        
        if not output_file:
            messagebox.showerror("错误", "请选择输出M3U文件")
            return
        
        try:
            self.status_var.set("正在转换...")
            self.root.update()
            
            # 读取频道映射CSV文件，只读取一次
            mapping_file = r"d:/Users/chien/PycharmProjects/testcode/program/get_iptv_data/channel_mapping_utf8.csv"
            channel_mapping_list = []
            channel_mapping_set = set()
            
            with open(mapping_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    bjtv_channel = row['bjtv_channel'].strip()
                    epg_display_name = row['epg_display_name'].strip()
                    if bjtv_channel:
                        channel_mapping_list.append((bjtv_channel, epg_display_name))
                        channel_mapping_set.add(bjtv_channel)
            
            # 读取JSON文件
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取频道信息
            channels = data.get('channleInfoStruct', [])
            
            # 构建频道字典，用于快速查找
            channel_dict = {}
            
            # 记录被抛弃的频道
            discarded_channels = []
            
            for channel in channels:
                channel_name = channel.get('channelName', '')
                channel_url = channel.get('channelURL', '')
                channel_id = channel.get('channelID', '')
                user_channel_id = channel.get('userChannelID', '')
                
                # 记录被抛弃的原因
                if not channel_name or not channel_url:
                    discarded_channels.append([channel_id, user_channel_id, channel_name, channel_url, "缺少频道名称或URL"])
                    continue
                
                # 只处理CSV文件中存在的频道，减少不必要的处理
                if channel_name not in channel_mapping_set:
                    discarded_channels.append([channel_id, user_channel_id, channel_name, channel_url, "不在映射表中"])
                    continue
                
                # 提取组播地址和端口
                # channel_url格式: igmp://239.3.1.161:8001
                if channel_url.startswith('igmp://'):
                    multicast_part = channel_url[7:]
                    multicast_ip, multicast_port = multicast_part.split(':')
                    
                    # 生成udpxy地址
                    udpxy_url = f"http://{udpxy_ip}:{udpxy_port}/{protocol}/{multicast_ip}:{multicast_port}"
                    
                    channel_dict[channel_name] = udpxy_url
                else:
                    discarded_channels.append([channel_id, user_channel_id, channel_name, channel_url, "URL格式不正确"])
            
            # 生成M3U内容，按照CSV文件的顺序排序
            m3u_content = ["#EXTM3U x-tvg-url=\"http://epg.51zmt.top:8000/e.xml.gz\""]
            
            # 按照CSV文件的顺序处理频道
            for bjtv_channel, epg_display_name in channel_mapping_list:
                # 检查频道是否在JSON文件中存在
                if bjtv_channel in channel_dict:
                    # 获取udpxy地址
                    udpxy_url = channel_dict[bjtv_channel]
                    
                    # 确定tvg-name
                    tvg_name = epg_display_name if epg_display_name else bjtv_channel
                    
                    # 添加到M3U内容
                    m3u_content.append(f"#EXTINF:-1, tvg-name=\"{tvg_name}\", {bjtv_channel}")
                    m3u_content.append(udpxy_url)
            
            # 写入M3U文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(m3u_content))
            
            # 生成并写入TXT播放文件
            txt_output_file = output_file.rsplit('.', 1)[0] + '.txt'
            txt_content = []
            
            # 添加默认分类
            txt_content.append("北京,#genre#")
            
            # 从M3U内容中提取频道信息，跳过第一行
            for i in range(1, len(m3u_content), 2):
                # 解析EXTINF行，提取频道名称
                extinf_line = m3u_content[i]
                # 格式：#EXTINF:-1, tvg-name="频道名称", 频道名称
                channel_name = extinf_line.split(',')[-1].strip()
                
                # 获取播放地址
                url_line = m3u_content[i+1]
                
                # 添加到TXT内容
                txt_content.append(f"{channel_name},{url_line}")
            
            # 写入TXT文件
            with open(txt_output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(txt_content))
            
            # 写入被抛弃的频道CSV文件
            discarded_csv_file = r"d:/Users/chien/PycharmProjects/testcode/program/get_iptv_data/iptv_discarded.csv"
            if discarded_channels:
                with open(discarded_csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # 写入表头
                    writer.writerow(['channelID', 'userChannelID', 'channelName', 'channelURL', 'discardReason'])
                    # 写入数据
                    writer.writerows(discarded_channels)
                
                # 生成被抛弃频道的M3U文件
                discarded_m3u_file = discarded_csv_file.rsplit('.', 1)[0] + '.m3u'
                discarded_m3u_content = ["#EXTM3U x-tvg-url=\"http://epg.51zmt.top:8000/e.xml.gz\""]
                
                for channel_info in discarded_channels:
                    channel_id, user_channel_id, channel_name, channel_url, discard_reason = channel_info
                    
                    # 只处理URL格式正确的频道
                    if channel_url.startswith('igmp://'):
                        multicast_part = channel_url[7:]
                        multicast_ip, multicast_port = multicast_part.split(':')
                        
                        # 生成udpxy地址
                        udpxy_url = f"http://{udpxy_ip}:{udpxy_port}/{protocol}/{multicast_ip}:{multicast_port}"
                        
                        # 添加到M3U内容
                        discarded_m3u_content.append(f"#EXTINF:-1, tvg-name=\"{channel_name}\", {channel_name} ({discard_reason})")
                        discarded_m3u_content.append(udpxy_url)
                
                # 写入被抛弃频道的M3U文件
                with open(discarded_m3u_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(discarded_m3u_content))
                
                discarded_info = f"，被抛弃的频道已记录到 {discarded_csv_file} 和 {discarded_m3u_file}"
            else:
                discarded_info = "，没有被抛弃的频道"
            
            self.status_var.set(f"转换完成！生成了 {len(m3u_content) // 2} 个频道")
            messagebox.showinfo("成功", f"转换完成！输出文件：{output_file} 和 {txt_output_file}{discarded_info}")
            
            # 询问用户是否关闭窗口
            result = messagebox.askyesno("询问", "转换已完成，是否关闭窗口？")
            if result:
                # 用户选择“是”，关闭窗口
                self.root.quit()
            else:
                # 用户选择“否”，重置状态，等待再次转换
                self.status_var.set("就绪")
            
        except Exception as e:
            self.status_var.set("转换失败")
            messagebox.showerror("错误", f"转换失败：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONtoM3UGUI(root)
    root.mainloop()