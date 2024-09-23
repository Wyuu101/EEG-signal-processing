import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from scipy.signal import welch

import sys
import os
import threading

class MainWindow(QWidget):
    def __init__(self):
        self.is_running = 0
        self.thread=None
        self.naodian_filename = None
        self.jiashi_filename = None
        super().__init__()
        icon = QIcon('icon.png')
        self.setWindowIcon(icon)
        self.setWindowTitle('数据分析')
        self.resize(500,450)
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        layout=QVBoxLayout()
        self.setLayout(layout)#设置垂直布局
        layout.addLayout(self.init_naodian())
        layout.addLayout(self.init_naodian_tips())
        layout.addLayout(self.init_naodian_options1())
        layout.addLayout(self.init_naodian_options2())
        layout.addLayout(self.init_space())
        layout.addLayout(self.init_fre_option())
        layout.addLayout(self.init_space())

        layout.addLayout(self.init_jiashi())
        layout.addLayout(self.init_jiashi_tips())
        layout.addLayout(self.init_jiashi_options())
        layout.addLayout(self.init_space())
        layout.addLayout(self.init_savename())
        layout.addLayout(self.init_space())
        layout.addLayout(self.init_log_label())
        layout.addLayout(self.init_logs())
        layout.addLayout(self.init_start())
        layout.addStretch()
        self.show()
        self.logs.append(f'初始化完成，欢迎使用！')
    def init_naodian(self):
        naodian_layout = QHBoxLayout()
        self.naodian_checkbox = QCheckBox('脑电数据提取', self)
        self.naodian_checkbox.stateChanged.connect(self.naodian_options_toggle)
        naodian_layout.addWidget(self.naodian_checkbox)
        self.naodian_select_file=QPushButton('选择文件')
        self.naodian_select_file.setEnabled(False)
        self.naodian_select_file.clicked.connect(self.naodian_showFileDialog)
        naodian_layout.addWidget(self.naodian_select_file)
        self.naodian_file_label = QLabel('未选择文件', self)
        self.naodian_file_label.setEnabled(False)
        naodian_layout.addWidget(self.naodian_file_label)
        naodian_layout.addStretch()
        return naodian_layout
    def init_naodian_tips(self):
        naodian_tips_layout = QHBoxLayout()
        self.naodian_tips_label = QLabel('请选择要绘制的波形', self)
        self.naodian_tips_label.setEnabled(False)
        naodian_tips_layout.addWidget(self.naodian_tips_label)
        return naodian_tips_layout
    def init_naodian_options1(self):
        naodian_options_layout = QHBoxLayout()
        self.naodian_option1 = QCheckBox('Raw Wave', self)
        self.naodian_option2 = QCheckBox('Delta', self)
        self.naodian_option3 = QCheckBox('Theta', self)
        self.naodian_option4 = QCheckBox('Low Alpha', self)
        self.naodian_option5 = QCheckBox('High Alpha', self)
        self.naodian_option6 = QCheckBox('Low Beta', self)
        self.naodian_option1.setEnabled(False)
        self.naodian_option2.setEnabled(False)
        self.naodian_option3.setEnabled(False)
        self.naodian_option4.setEnabled(False)
        self.naodian_option5.setEnabled(False)
        self.naodian_option6.setEnabled(False)
        naodian_options_layout.addWidget(self.naodian_option1)
        naodian_options_layout.addWidget(self.naodian_option2)
        naodian_options_layout.addWidget(self.naodian_option3)
        naodian_options_layout.addWidget(self.naodian_option4)
        naodian_options_layout.addWidget(self.naodian_option5)
        naodian_options_layout.addWidget(self.naodian_option6)
        naodian_options_layout.addStretch()
        return naodian_options_layout
    def init_naodian_options2(self):
        naodian_options_layout = QHBoxLayout()
        self.naodian_option7 = QCheckBox('High Beta', self)
        self.naodian_option8 = QCheckBox('Low Gamma', self)
        self.naodian_option9 = QCheckBox('High Gamma', self)
        self.naodian_option10 = QCheckBox('Attention', self)
        self.naodian_option11 = QCheckBox('Meditation', self)
        self.naodian_option7.setEnabled(False)
        self.naodian_option8.setEnabled(False)
        self.naodian_option9.setEnabled(False)
        self.naodian_option10.setEnabled(False)
        self.naodian_option11.setEnabled(False)
        naodian_options_layout.addWidget(self.naodian_option7)
        naodian_options_layout.addWidget(self.naodian_option8)
        naodian_options_layout.addWidget(self.naodian_option9)
        naodian_options_layout.addWidget(self.naodian_option10)
        naodian_options_layout.addWidget(self.naodian_option11)
        naodian_options_layout.addStretch()
        return naodian_options_layout

    def init_space(self):
        space_layout = QHBoxLayout()
        space_layout.addItem(QSpacerItem(0,20))
        return space_layout

    def init_fre_option(self):
        fre_option_layout = QHBoxLayout()
        self.naodian_fre_option = QCheckBox("是否绘制频域图")
        self.naodian_fre_option.setEnabled(False)
        fre_option_layout.addStretch()
        fre_option_layout.addWidget(self.naodian_fre_option)
        fre_option_layout.addStretch()
        return fre_option_layout

    def naodian_options_toggle(self, state):
        if state == 2:
            self.naodian_option1.setEnabled(True)
            self.naodian_option2.setEnabled(True)
            self.naodian_option3.setEnabled(True)
            self.naodian_option4.setEnabled(True)
            self.naodian_option5.setEnabled(True)
            self.naodian_option6.setEnabled(True)
            self.naodian_option7.setEnabled(True)
            self.naodian_option8.setEnabled(True)
            self.naodian_option9.setEnabled(True)
            self.naodian_option10.setEnabled(True)
            self.naodian_option11.setEnabled(True)
            self.naodian_select_file.setEnabled(True)
            self.naodian_file_label.setEnabled(True)
            self.naodian_tips_label.setEnabled(True)
            self.naodian_fre_option.setEnabled(True)
            self.start_button.setEnabled(True)
        else:
            self.naodian_option1.setEnabled(False)
            self.naodian_option2.setEnabled(False)
            self.naodian_option3.setEnabled(False)
            self.naodian_option4.setEnabled(False)
            self.naodian_option5.setEnabled(False)
            self.naodian_option6.setEnabled(False)
            self.naodian_option7.setEnabled(False)
            self.naodian_option8.setEnabled(False)
            self.naodian_option9.setEnabled(False)
            self.naodian_option10.setEnabled(False)
            self.naodian_option11.setEnabled(False)
            self.naodian_select_file.setEnabled(False)
            self.naodian_file_label.setEnabled(False)
            self.naodian_tips_label.setEnabled(False)
            self.naodian_fre_option.setEnabled(False)
            if(not self.jiashi_checkbox.isChecked()):
                self.start_button.setEnabled(False)
    def naodian_showFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'All Files (*)')
        if file_path:
            self.naodian_file_label.setText(os.path.basename(file_path))
            self.naodian_filename = os.path.basename(file_path)
        else:
            self.naodian_file_label.setText('未选择文件')
            self.naodian_filename = None
    def init_jiashi(self):
        jiashi_layout = QHBoxLayout()
        self.jiashi_checkbox = QCheckBox('驾驶数据提取', self)
        self.jiashi_checkbox.stateChanged.connect(self.jiashi_options_toggle)
        jiashi_layout.addWidget(self.jiashi_checkbox)
        self.jiashi_select_file = QPushButton('选择文件')
        self.jiashi_select_file.setEnabled(False)
        self.jiashi_select_file.clicked.connect(self.jiashi_showFileDialog)
        jiashi_layout.addWidget(self.jiashi_select_file)
        self.jiashi_file_label = QLabel('未选择文件', self)
        self.jiashi_file_label.setEnabled(False)
        jiashi_layout.addWidget(self.jiashi_file_label)
        jiashi_layout.addStretch()
        return jiashi_layout
    def init_jiashi_tips(self):
        jiashi_tips_layout = QHBoxLayout()
        self.jiashi_tips_label = QLabel('请选择要绘制的波形', self)
        self.jiashi_tips_label.setEnabled(False)
        jiashi_tips_layout.addWidget(self.jiashi_tips_label)
        return jiashi_tips_layout
    def init_jiashi_options(self):
        jiashi_options_layout = QHBoxLayout()
        self.jiashi_option1 = QCheckBox('速度', self)
        self.jiashi_option2 = QCheckBox('方向盘', self)
        self.jiashi_option3 = QCheckBox('油门', self)
        self.jiashi_option4 = QCheckBox('刹车', self)
        self.jiashi_option1.setEnabled(False)
        self.jiashi_option2.setEnabled(False)
        self.jiashi_option3.setEnabled(False)
        self.jiashi_option4.setEnabled(False)

        jiashi_options_layout.addWidget(self.jiashi_option1)
        jiashi_options_layout.addWidget(self.jiashi_option2)
        jiashi_options_layout.addWidget(self.jiashi_option3)
        jiashi_options_layout.addWidget(self.jiashi_option4)
        jiashi_options_layout.addStretch()
        return jiashi_options_layout
    def jiashi_options_toggle(self, state):
        if state == 2:
            self.jiashi_option1.setEnabled(True)
            self.jiashi_option2.setEnabled(True)
            self.jiashi_option3.setEnabled(True)
            self.jiashi_option4.setEnabled(True)
            self.jiashi_select_file.setEnabled(True)
            self.jiashi_file_label.setEnabled(True)
            self.jiashi_tips_label.setEnabled(True)
            self.start_button.setEnabled(True)
        else:
            self.jiashi_option1.setEnabled(False)
            self.jiashi_option2.setEnabled(False)
            self.jiashi_option3.setEnabled(False)
            self.jiashi_option4.setEnabled(False)
            self.jiashi_select_file.setEnabled(False)
            self.jiashi_file_label.setEnabled(False)
            self.jiashi_tips_label.setEnabled(False)
            if(not self.naodian_checkbox.isChecked()):
                self.start_button.setEnabled(False)
    def jiashi_showFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'All Files (*)')
        if file_path:
            self.jiashi_file_label.setText(os.path.basename(file_path))
            self.jiashi_filename = os.path.basename(file_path)
        else:
            self.jiashi_file_label.setText('未选择文件')
            self.jiashi_filename =None
    def init_savename(self):
        save_layout = QHBoxLayout()
        self.savename_bar = QLineEdit()
        self.savename_bar.setPlaceholderText('默认为figure.png')
        self.savename = "figure.png"
        label = QLabel('将图片保存为:', self)
        save_layout.addWidget(label)
        save_layout.addWidget(self.savename_bar)
        return save_layout
    def init_log_label(self):
        log_label_layout = QHBoxLayout()
        self.log_label = QLabel('日志', self)
        self.log_label.setEnabled(False)
        log_label_layout.addWidget(self.log_label)
        return log_label_layout
    def init_logs(self):
        logs_layout = QHBoxLayout()
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        logs_layout.addWidget(self.logs)
        # self.text_edit.setGeometry(10, 10, 780, 500)
        return logs_layout
    def init_start(self):
        start_layout = QHBoxLayout()
        self.start_button = QPushButton('开始绘图')
        self.start_button.setEnabled(False)
        self.start_button.setFixedSize(100,55)
        self.start_button.clicked.connect(self.start_thread)
        start_layout.addStretch()
        start_layout.addWidget(self.start_button)
        start_layout.addStretch()
        return start_layout
    def start_thread(self):
        if(self.naodian_checkbox.isChecked() and self.naodian_filename==None):
            self.logs.append("请选择数据文件!")
            return
        if(self.jiashi_checkbox.isChecked() and self.jiashi_filename == None):
            self.logs.append("请选择数据文件！")
            return
        if(self.savename_bar.text()!=""):
            self.savename = self.savename_bar.text()
        self.pics = 0
        self.pics_name = []
        if(self.naodian_checkbox.isChecked()):
            if(self.naodian_option1.isChecked()):
                self.pics_name.append("raw_wave")
            if (self.naodian_option2.isChecked()):
                self.pics_name.append("delta")
            if (self.naodian_option3.isChecked()):
                self.pics_name.append("theta")
            if (self.naodian_option4.isChecked()):
                self.pics_name.append("low_alpha")
            if (self.naodian_option5.isChecked()):
                self.pics_name.append("high_alpha")
            if (self.naodian_option6.isChecked()):
                self.pics_name.append("low_beta")
            if (self.naodian_option7.isChecked()):
                self.pics_name.append("high_beta")
            if (self.naodian_option8.isChecked()):
                self.pics_name.append("low_gamma")
            if (self.naodian_option9.isChecked()):
                self.pics_name.append("middle_gamma")
            if (self.naodian_option10.isChecked()):
                self.pics_name.append("attention")
            if (self.naodian_option11.isChecked()):
                self.pics_name.append("meditation")
            if (self.naodian_fre_option.isChecked()):
                self.fre_chosed = 1
        if(self.jiashi_checkbox.isChecked()):
            if(self.jiashi_option1.isChecked()):
                self.pics_name.append("speed")
            if (self.jiashi_option2.isChecked()):
                self.pics_name.append("steering")
            if (self.jiashi_option3.isChecked()):
                self.pics_name.append("throttle")
            if (self.jiashi_option4.isChecked()):
                self.pics_name.append("brake")
        if(len(self.pics_name)<=1):
            self.logs.append("请至少选择两个项目进行绘制")
            return
        thread = threading.Thread(target=self.func)
        self.thread=thread
        self.logs.append("正在开始绘图，请耐心等待...")
        thread.start()
    def stop_thread(self):
        self.thread.stop()
    def func(self):
        if(self.naodian_checkbox.isChecked() and (not self.jiashi_checkbox.isChecked())):
            finaldata = {}
            finaldata.update(self.get_rawdata_from_txt())
            if(self.fre_chosed ==1):
                special_keys = ["delta","theta","low_alpha","high_alpha","low_beta","high_beta","low_gamma","middle_gamma"]
                rawdata_from_large_packets_list = [finaldata[key] for key in special_keys]
                self.plot_signals_and_features(rawdata_from_large_packets_list)
            self.logs.append("频域分析图已绘制完毕，保存为eeg_features.png")
            self.logs.append("开始绘制时域分析图...")
            self.draw_pic(finaldata, 0)
        elif(self.jiashi_checkbox.isChecked() and (not self.naodian_checkbox.isChecked())):
            finaldata = {}
            finaldata.update(self.get_rawdata_from_csv())
            self.draw_pic(finaldata,1)
        elif (self.jiashi_checkbox.isChecked() and  self.naodian_checkbox.isChecked()):
            finaldata = {}
            finaldata.update(self.get_rawdata_from_txt())
            finaldata.update(self.get_rawdata_from_csv())
            self.draw_pic(finaldata, 2)
    def get_rawdata_from_smallpacket(self,small_packets):
        packets_size = len(small_packets)
        correct_packets = 0
        rawdatas = []
        for packet in small_packets:
            match = re.match(r'AAAA048002(.{6})', packet)
            if match:
                data = match.group(1)
                if len(data) == 6:
                    data1 = data[0:2]
                    data2 = data[2:4]
                    data3 = data[4:6]
                    # 将数据转换为十进制整数
                    high = int(data1, 16)
                    low = int(data2, 16)
                    checksum = int(data3, 16)
                    total = 0x80 + 0x02 + high + low
                    inverted = total ^ 0xFFFFFFFF
                    result = inverted & 0xFF
                    if(result == checksum):
                        correct_packets= correct_packets+1
                        rawdata = (high << 8) | low
                        # 调整 rawdata 到有符号整数范围
                        if rawdata > 32768:
                            rawdata -= 65536
                        rawdatas.append(rawdata)
        return rawdatas
        self.logs.append(f"脑电数据丢包率为:{((packets_size-correct_packets)/packets_size*100)}%")
    def get_rawdata_from_large_packets(self,large_packets):
        packets_size = len(large_packets)
        correct_packets = 0
        delta_rawdata = []
        theta_rawdata = []
        low_alpha_rawdata = []
        high_alpha_rawdata = []
        low_beta_rawdata = []
        high_beta_rawdata = []
        low_gamma_rawdata = []
        middle_gamma_rawdata = []
        attention_rawdata = []
        meditation_rawdata = []
        for packet in large_packets:
            match = re.match(r'AAAA2002(.{64})', packet)
            if match:
                data = match.group(1)
                if len(data) == 64:
                    split_data = [data[i:i+2] for i in range(0, len(data), 2)]
                    delta_rawdata.append((int(split_data[3],16)<<16) | (int(split_data[4],16)<<8) | (int(split_data[5],16)))
                    theta_rawdata.append((int(split_data[6],16)<<16) | (int(split_data[7],16)<<8) | (int(split_data[8],16)))
                    low_alpha_rawdata.append((int(split_data[9],16)<<16) | (int(split_data[10],16)<<8) | (int(split_data[11],16)))
                    high_alpha_rawdata.append((int(split_data[12],16)<<16) | (int(split_data[13],16)<<8) | (int(split_data[14],16)))
                    low_beta_rawdata.append((int(split_data[15],16)<<16) | (int(split_data[16],16)<<8) | (int(split_data[17],16)))
                    high_beta_rawdata.append((int(split_data[18],16)<<16) | (int(split_data[19],16)<<8) | (int(split_data[20],16)))
                    low_gamma_rawdata.append((int(split_data[21],16)<<16) | (int(split_data[22],16)<<8) | (int(split_data[23],16)))
                    middle_gamma_rawdata.append((int(split_data[24],16)<<16) | (int(split_data[25],16)<<8) | (int(split_data[26],16)))
                    attention_rawdata.append(int(split_data[28], 16))
                    meditation_rawdata.append(int(split_data[30], 16))
        rawdatas  = {
            "delta":delta_rawdata,
            "theta":theta_rawdata,
            "low_alpha":low_alpha_rawdata,
            "high_alpha":high_alpha_rawdata,
            "low_beta":low_beta_rawdata,
            "high_beta":high_beta_rawdata,
            "low_gamma":low_gamma_rawdata,
            "middle_gamma":middle_gamma_rawdata,
            "attention":attention_rawdata,
            "meditation":meditation_rawdata
        }
        return  rawdatas
    def get_rawdata_from_csv(self):
        df = pd.read_csv(self.jiashi_filename)
        # start = int(input("请输入采样起始点:"))
        # step = int(input("请输入采样步长(建议为5):"))
        sampled_df = df.iloc[::5]
        # 提取速度和加速度列并放入列表
        time_stamp_list = sampled_df['timeStamp'].tolist()#时间
        speed_list = sampled_df['speedInKmPerHour'].tolist()#速度
        steering_list = sampled_df['rawSteering'].tolist()#方向盘
        throttle_list = sampled_df['throttle'].tolist()#油门
        brake_list = sampled_df['brake'].tolist()#刹车
        length = len(time_stamp_list)
        self.logs.append(f"已提取{length}条数据，范围从 {time_stamp_list[0]} 至 {time_stamp_list[-1]}")
        data_dict = {
            "len":length,
            "time":time_stamp_list,
            "speed":speed_list,
            "steering":steering_list,
            "throttle":throttle_list,
            "brake":brake_list
        }
        return data_dict
    def get_rawdata_from_txt(self):
        with open(self.naodian_filename, "r", encoding="utf-8") as file:
            data_with_time = file.read();
        data_list = re.findall(r'RX：(.*)', data_with_time)
        filtered_data_list = [element.strip() for element in data_list if element.strip()]
        data = "".join(filtered_data_list).replace(" ", "")
        with open("formatted_data.txt", "w", encoding="utf-8") as file:
            file.write(data)
        self.logs.append(f"脑电数据流已格式化并保存为formatted_data.txt")
        small_packet_pattern = r'(AAAA048002.{6})'
        large_packet_pattern = r'(AAAA2002.{64})'
        small_packets = re.findall(small_packet_pattern, data)
        large_packets = re.findall(large_packet_pattern, data)
        rawdata_from_large_packets =  self.get_rawdata_from_large_packets(large_packets)
        reslut = rawdata_from_large_packets
        rawdata_from_smallpackets=  self.get_rawdata_from_smallpacket(small_packets)
        reslut.update({"raw_wave":rawdata_from_smallpackets})
        return reslut
    def draw_pic(self,finaldata,model):
        size = len(self.pics_name)
        fig, axs = plt.subplots(size, 1, figsize=(200, 150))
        if(model==0 or model==1):
            for index, pic in enumerate(self.pics_name):
                axs[index].set_title(pic, fontsize=40)
                if(pic == "raw_wave"):
                    axs[index].plot(finaldata[pic], label=pic, color = "red",linewidth=5, marker='')
                    continue
                if (pic == "attention" or pic == "meditation"):
                    axs[index].plot(finaldata[pic], label=pic, color="green", linewidth=5, marker='')
                    continue
                axs[index].plot(finaldata[pic], label=pic, linewidth=5, marker='')
        else:
            spilt = 0
            if("speed" in self.pics_name):
                spilt = len(finaldata["speed"])
            elif("steering" in self.pics_name):
                spilt = len(finaldata["steering"])
            elif ("throttle" in self.pics_name):
                spilt = len(finaldata["throttle"])
            elif ("brake" in self.pics_name):
                spilt = len(finaldata["brake"])
            for index, pic in enumerate(self.pics_name):
                axs[index].set_title(pic, fontsize=40)
                if(pic == "raw_wave"):
                    axs[index].plot(finaldata[pic][:spilt], label=pic, color = "red",linewidth=5, marker='')
                    continue
                if (pic == "attention" or pic == "meditation"):
                    axs[index].plot(finaldata[pic][:spilt], label=pic, color="green", linewidth=5, marker='')
                    continue
                axs[index].plot(finaldata[pic][:spilt], label=pic, linewidth=5, marker='')
        plt.gca().axes.get_xaxis().set_visible(False)
        fig.suptitle('Figure', fontsize=80)
        self.logs.append(f"图像已生成并保存为{self.savename}")
        plt.savefig(self.savename)
        #plt.show()

    def extract_time_domain_features(self,signal):
        features = {
            "Mean": np.mean(signal),  # 均值
            "Variance": np.var(signal),  # 方差
            "Peak-to-Peak": np.ptp(signal),  # 峰值
            "Standard Deviation": np.std(signal)  # 标准差
        }
        return features


    def extract_frequency_domain_features(self,signal, fs=512):
        freqs, psd = welch(signal, fs=fs)
        return freqs, psd

    def plot_signals_and_features(self,rawdata_from_large_packets):
        titles = ["Delta", "Theta", "Low Alpha", "High Alpha", "Low Beta", "High Beta", "Low Gamma", "High Gamma"]
        fs = 512  # 采样率为512Hz

        fig, axs = plt.subplots(8, 2, figsize=(20, 40))  # 8个波形，每个波形2个子图（时域和频域）

        # 创建一个空的DataFrame，用于存储特征
        df = pd.DataFrame(columns=["Signal", "Feature", "Value"])

        for i in range(8):
            signal = rawdata_from_large_packets[i]
            # 时域特征提取
            time_features = self.extract_time_domain_features(signal)
            #print(f"{titles[i]} - Time Domain Features: {time_features}")

            # 将时域特征添加到DataFrame
            time_features_df = pd.DataFrame([{"Signal": titles[i], "Feature": feature_name, "Value": feature_value}
                                             for feature_name, feature_value in time_features.items()])
            df = pd.concat([df, time_features_df], ignore_index=True)

            # 时域图
            axs[i, 0].plot(signal, label=f'{titles[i]} Time Domain')
            axs[i, 0].set_title(f'{titles[i]} Time Domain')
            axs[i, 0].legend()

            # 频域特征提取
            freqs, psd = self.extract_frequency_domain_features(signal, fs)

            # 将频域特征（功率谱密度）添加到DataFrame
            psd_df = pd.DataFrame([{"Signal": titles[i], "Feature": f'PSD_{freq:.2f}Hz', "Value": psd_value}
                                   for freq, psd_value in zip(freqs, psd)])
            df = pd.concat([df, psd_df], ignore_index=True)

            # 频域图
            axs[i, 1].semilogy(freqs, psd, label=f'{titles[i]} Frequency Domain')
            axs[i, 1].set_title(f'{titles[i]} Frequency Domain')
            axs[i, 1].legend()

        # 保存特征到Excel文件
        df.to_excel("eeg_features.xlsx", index=False)

        fig.suptitle('EEG Signal Time and Frequency Domain Features', fontsize=20)
        plt.tight_layout()
        plt.savefig('eeg_features.png')  # 保存图片
        #plt.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

