#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from dna_tools import DNATools

# 获取程序运行路径,兼容打包后的exe
if getattr(sys, 'frozen', False):
    # 如果是打包后的exe
    root_path = os.path.dirname(sys.executable)
else:
    # 如果是python脚本
    root_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(root_path, "..")



class GibsonPrimerDesignApp:
    """Gibson Assembly引物设计工具的图形用户界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gibson Assembly引物设计工具")
        self.root.geometry("900x700")
        
        # 设置窗口图标
        try:
            icon_path = f"{root_path}/assets/LetsGibson_subsize.ico"
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"设置图标时出错: {str(e)}")
        
        # 创建DNA工具实例
        self.dna_tools = DNATools()
        
        # 存储插入片段和载体信息
        self.fragments = []
        self.fragment_files = []
        self.fragment_order = []
        self.vector = None
        self.vector_file = ""
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        """创建图形界面组件"""
        # 创建标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建输入页面
        self.input_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text="输入")
        
        # 创建结果页面
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="结果")
        
        # 设置输入页面
        self.setup_input_frame()
        
        # 设置结果页面
        self.setup_result_frame()
        
        # 添加关于按钮
        about_btn = ttk.Button(self.root, text="关于 / About", command=self.show_about_dialog)
        about_btn.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def setup_input_frame(self):
        """设置输入页面的组件"""
        # 创建左右分栏
        left_frame = ttk.Frame(self.input_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.input_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧：插入片段部分
        fragment_frame = ttk.LabelFrame(left_frame, text="插入片段")
        fragment_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 添加片段按钮
        add_fragment_btn = ttk.Button(fragment_frame, text="添加片段", command=self.add_fragment)
        add_fragment_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # 片段列表
        self.fragment_listbox = tk.Listbox(fragment_frame, selectmode=tk.SINGLE, height=10)
        self.fragment_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 片段操作按钮
        fragment_btn_frame = ttk.Frame(fragment_frame)
        fragment_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        remove_fragment_btn = ttk.Button(fragment_btn_frame, text="移除片段", command=self.remove_fragment)
        remove_fragment_btn.pack(side=tk.LEFT, padx=5)
        
        move_up_btn = ttk.Button(fragment_btn_frame, text="上移", command=self.move_fragment_up)
        move_up_btn.pack(side=tk.LEFT, padx=5)
        
        move_down_btn = ttk.Button(fragment_btn_frame, text="下移", command=self.move_fragment_down)
        move_down_btn.pack(side=tk.LEFT, padx=5)
        
        # 右侧：载体部分
        vector_frame = ttk.LabelFrame(right_frame, text="载体")
        vector_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 选择载体文件
        vector_file_frame = ttk.Frame(vector_frame)
        vector_file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(vector_file_frame, text="载体文件:").pack(side=tk.LEFT)
        self.vector_file_var = tk.StringVar()
        vector_file_entry = ttk.Entry(vector_file_frame, textvariable=self.vector_file_var, width=30)
        vector_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        vector_file_btn = ttk.Button(vector_file_frame, text="浏览...", command=self.select_vector_file)
        vector_file_btn.pack(side=tk.LEFT)
        
        # 载体线性化方式
        linearization_frame = ttk.Frame(vector_frame)
        linearization_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(linearization_frame, text="线性化方式:").pack(side=tk.LEFT)
        self.linearization_var = tk.StringVar(value="restriction")
        
        restriction_radio = ttk.Radiobutton(linearization_frame, text="限制酶切", 
                                           variable=self.linearization_var, value="restriction",
                                           command=self.toggle_linearization_options)
        restriction_radio.pack(side=tk.LEFT, padx=5)
        
        pcr_radio = ttk.Radiobutton(linearization_frame, text="PCR扩增", 
                                   variable=self.linearization_var, value="pcr",
                                   command=self.toggle_linearization_options)
        pcr_radio.pack(side=tk.LEFT, padx=5)
        
        # 限制酶选项
        self.restriction_frame = ttk.Frame(vector_frame)
        self.restriction_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.restriction_frame, text="限制酶:").pack(side=tk.LEFT)
        
        # 常用限制酶列表
        enzymes = ['EcoRI', 'BamHI', 'HindIII', 'XhoI', 'NdeI', 'XbaI', 'PstI', 
                  'SalI', 'SmaI', 'KpnI', 'SacI', 'SphI', 'NotI', 'BglII', 'NcoI']
        
        self.enzyme_var = tk.StringVar()
        enzyme_combobox = ttk.Combobox(self.restriction_frame, textvariable=self.enzyme_var, 
                                      values=enzymes, width=15)
        enzyme_combobox.pack(side=tk.LEFT, padx=5)
        enzyme_combobox.current(0)
        
        # PCR引物选项
        self.pcr_frame = ttk.Frame(vector_frame)
        
        # 正向引物
        fw_primer_frame = ttk.Frame(self.pcr_frame)
        fw_primer_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(fw_primer_frame, text="正向引物:").pack(side=tk.LEFT)
        self.fw_primer_var = tk.StringVar()
        fw_primer_entry = ttk.Entry(fw_primer_frame, textvariable=self.fw_primer_var, width=40)
        fw_primer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 反向引物
        rv_primer_frame = ttk.Frame(self.pcr_frame)
        rv_primer_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(rv_primer_frame, text="反向引物:").pack(side=tk.LEFT)
        self.rv_primer_var = tk.StringVar()
        rv_primer_entry = ttk.Entry(rv_primer_frame, textvariable=self.rv_primer_var, width=40)
        rv_primer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 同源臂长度设置
        homology_frame = ttk.Frame(right_frame)
        homology_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(homology_frame, text="同源臂长度 (bp):").pack(side=tk.LEFT)
        self.homology_length_var = tk.IntVar(value=25)
        homology_spinbox = ttk.Spinbox(homology_frame, from_=15, to=40, 
                                      textvariable=self.homology_length_var, width=5)
        homology_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 设计引物按钮
        design_btn = ttk.Button(right_frame, text="设计引物", command=self.design_primers)
        design_btn.pack(fill=tk.X, padx=5, pady=10)
        
        # 默认显示限制酶选项
        self.toggle_linearization_options()
    
    def setup_result_frame(self):
        """设置结果页面的组件"""
        # 结果显示区域
        result_text_frame = ttk.Frame(self.result_frame)
        result_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_text_frame, wrap=tk.WORD, 
                                                   width=80, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 导出按钮
        export_frame = ttk.Frame(self.result_frame)
        export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        export_csv_btn = ttk.Button(export_frame, text="导出为CSV", command=lambda: self.export_results('csv'))
        export_csv_btn.pack(side=tk.LEFT, padx=5)
        
        export_txt_btn = ttk.Button(export_frame, text="导出为TXT", command=lambda: self.export_results('txt'))
        export_txt_btn.pack(side=tk.LEFT, padx=5)
    
    def add_fragment(self):
        """添加插入片段"""
        file_path = filedialog.askopenfilename(
            title="选择FASTA文件",
            filetypes=[("FASTA文件", "*.fasta;*.fa"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            records = self.dna_tools.read_fasta(file_path)
            
            if not records:
                messagebox.showerror("错误", "FASTA文件中未找到序列")
                return
            
            # 处理多个序列的情况
            if len(records) > 1:
                # 创建选择对话框
                select_window = tk.Toplevel(self.root)
                select_window.title("选择序列")
                select_window.geometry("400x300")
                select_window.resizable(True, True)
                
                # 添加说明标签
                ttk.Label(select_window, text="FASTA文件中包含多个序列，请选择要添加的序列:").pack(pady=10)
                
                # 创建列表框
                select_listbox = tk.Listbox(select_window, selectmode=tk.EXTENDED, height=10)
                select_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # 添加序列到列表框
                for record in records:
                    select_listbox.insert(tk.END, f"{record.id} ({len(record.seq)} bp)")
                
                # 添加按钮
                btn_frame = ttk.Frame(select_window)
                btn_frame.pack(fill=tk.X, padx=10, pady=10)
                
                def add_selected():
                    selected_indices = select_listbox.curselection()
                    if not selected_indices:
                        messagebox.showinfo("提示", "请至少选择一个序列")
                        return
                    
                    for idx in selected_indices:
                        record = records[idx]
                        # 使用序列ID作为片段名称
                        fragment_name = record.id
                        if not fragment_name or fragment_name.strip() == "":
                            # 如果ID为空，则使用文件名和索引
                            fragment_name = f"{os.path.basename(file_path)}_{idx+1}"
                        
                        # 添加到片段列表
                        self.fragments.append(record)
                        self.fragment_files.append(file_path)
                        self.fragment_order.append(len(self.fragments) - 1)
                        
                        # 更新列表显示
                        self.fragment_listbox.insert(tk.END, fragment_name)
                    
                    select_window.destroy()
                
                ttk.Button(btn_frame, text="添加选中序列", command=add_selected).pack(side=tk.LEFT, padx=5)
                ttk.Button(btn_frame, text="取消", command=select_window.destroy).pack(side=tk.RIGHT, padx=5)
                
                # 使对话框模态
                select_window.transient(self.root)
                select_window.grab_set()
                self.root.wait_window(select_window)
                
            else:
                # 只有一个序列的情况
                record = records[0]
                # 使用序列ID作为片段名称
                fragment_name = record.id
                if not fragment_name or fragment_name.strip() == "":
                    # 如果ID为空，则使用文件名
                    fragment_name = os.path.basename(file_path)
                
                # 添加到片段列表
                self.fragments.append(record)
                self.fragment_files.append(file_path)
                self.fragment_order.append(len(self.fragments) - 1)
                
                # 更新列表显示
                self.fragment_listbox.insert(tk.END, fragment_name)
                
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def remove_fragment(self):
        """移除选中的片段"""
        selected_idx = self.fragment_listbox.curselection()
        
        if not selected_idx:
            messagebox.showinfo("提示", "请先选择要移除的片段")
            return
        
        idx = selected_idx[0]
        
        # 从列表中移除
        self.fragment_listbox.delete(idx)
        
        # 更新片段顺序
        removed_idx = self.fragment_order[idx]
        self.fragment_order.pop(idx)
        
        # 调整顺序索引
        for i in range(len(self.fragment_order)):
            if self.fragment_order[i] > removed_idx:
                self.fragment_order[i] -= 1
    
    def move_fragment_up(self):
        """上移选中的片段"""
        selected_idx = self.fragment_listbox.curselection()
        
        if not selected_idx or selected_idx[0] == 0:
            return
        
        idx = selected_idx[0]
        
        # 交换列表项
        fragment_name = self.fragment_listbox.get(idx)
        self.fragment_listbox.delete(idx)
        self.fragment_listbox.insert(idx - 1, fragment_name)
        self.fragment_listbox.selection_set(idx - 1)
        
        # 交换顺序
        self.fragment_order[idx], self.fragment_order[idx - 1] = self.fragment_order[idx - 1], self.fragment_order[idx]
    
    def move_fragment_down(self):
        """下移选中的片段"""
        selected_idx = self.fragment_listbox.curselection()
        
        if not selected_idx or selected_idx[0] == self.fragment_listbox.size() - 1:
            return
        
        idx = selected_idx[0]
        
        # 交换列表项
        fragment_name = self.fragment_listbox.get(idx)
        self.fragment_listbox.delete(idx)
        self.fragment_listbox.insert(idx + 1, fragment_name)
        self.fragment_listbox.selection_set(idx + 1)
        
        # 交换顺序
        self.fragment_order[idx], self.fragment_order[idx + 1] = self.fragment_order[idx + 1], self.fragment_order[idx]
    
    def select_vector_file(self):
        """选择载体文件"""
        file_path = filedialog.askopenfilename(
            title="选择载体FASTA文件",
            filetypes=[("FASTA文件", "*.fasta;*.fa"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            records = self.dna_tools.read_fasta(file_path)
            
            if not records:
                messagebox.showerror("错误", "FASTA文件中未找到序列")
                return
            
            if len(records) > 1:
                messagebox.showwarning("警告", f"FASTA文件中包含多个序列，将使用第一个序列")
            
            # 设置载体信息
            self.vector = records[0]
            self.vector_file = file_path
            self.vector_file_var.set(file_path)
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def toggle_linearization_options(self):
        """根据线性化方式切换选项"""
        if self.linearization_var.get() == "restriction":
            self.pcr_frame.pack_forget()
            self.restriction_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.restriction_frame.pack_forget()
            self.pcr_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def design_primers(self):
        """设计Gibson Assembly引物"""
        # 检查输入
        if not self.fragments:
            messagebox.showerror("错误", "请添加至少一个插入片段")
            return
        
        if not self.vector:
            messagebox.showerror("错误", "请选择载体文件")
            return
        
        # 获取同源臂长度
        homology_length = self.homology_length_var.get()
        
        # 获取载体线性化信息
        linearization_method = self.linearization_var.get()
        linearization_info = {}
        
        if linearization_method == "restriction":
            linearization_info["enzyme"] = self.enzyme_var.get()
        else:
            fw_primer = self.fw_primer_var.get().strip()
            rv_primer = self.rv_primer_var.get().strip()
            
            if not fw_primer or not rv_primer:
                messagebox.showerror("错误", "请输入PCR引物序列")
                return
            
            linearization_info["fw_primer"] = fw_primer
            linearization_info["rv_primer"] = rv_primer
        
        try:
            # 按顺序获取片段
            ordered_fragments = [self.fragments[i] for i in self.fragment_order]
            
            # 设计引物
            primer_results = self.dna_tools.design_gibson_primers(
                ordered_fragments, 
                self.vector, 
                homology_length, 
                linearization_method, 
                linearization_info
            )
            
            # 显示结果
            self.display_results(primer_results)
            
            # 切换到结果页面
            self.notebook.select(1)
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def display_results(self, primer_results):
        """显示引物设计结果"""
        self.result_text.delete(1.0, tk.END)
        
        # 存储结果用于导出
        self.primer_results = primer_results
        
        # 添加标题
        self.result_text.insert(tk.END, "Gibson Assembly引物设计结果\n")
        self.result_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # 显示载体信息
        self.result_text.insert(tk.END, "载体信息:\n")
        self.result_text.insert(tk.END, f"名称: {self.vector.id}\n")
        self.result_text.insert(tk.END, f"长度: {len(self.vector.seq)} bp\n")
        self.result_text.insert(tk.END, f"文件: {self.vector_file}\n\n")
        
        # 显示片段信息
        self.result_text.insert(tk.END, "插入片段:\n")
        for i, idx in enumerate(self.fragment_order):
            fragment = self.fragments[idx]
            self.result_text.insert(tk.END, f"{i+1}. {fragment.id} ({len(fragment.seq)} bp)\n")
            self.result_text.insert(tk.END, f"   文件: {self.fragment_files[idx]}\n")
        
        self.result_text.insert(tk.END, "\n" + "=" * 80 + "\n\n")
        
        # 显示引物信息
        self.result_text.insert(tk.END, "引物设计结果:\n\n")
        
        # 载体引物
        if "vector_primers" in primer_results:
            self.result_text.insert(tk.END, "载体引物:\n")
            vector_primers = primer_results["vector_primers"]
            
            # 显示正向引物名称和序列
            fw = vector_primers['fw']
            fw_name = fw.get('name', "Vector-F")
            self.result_text.insert(tk.END, f"{fw_name}: {fw['sequence']}\n")
            self.result_text.insert(tk.END, f"Tm值: {fw['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"GC含量: {fw['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"长度: {fw['length']} bp\n\n")
            
            # 显示反向引物名称和序列
            rv = vector_primers['rv']
            rv_name = rv.get('name', "Vector-R")
            self.result_text.insert(tk.END, f"{rv_name}: {rv['sequence']}\n")
            self.result_text.insert(tk.END, f"Tm值: {rv['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"GC含量: {rv['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"长度: {rv['length']} bp\n\n")
            
            # 添加分割线
            self.result_text.insert(tk.END, "-" * 80 + "\n\n")
        
        # 片段引物
        self.result_text.insert(tk.END, "片段引物:\n")
        
        for i, primer_info in enumerate(primer_results["fragment_primers"]):
            # 使用片段名称
            fragment_name = primer_info.get("name", f"片段 {i+1}")
            self.result_text.insert(tk.END, f"{fragment_name}:\n")
            
            # 正向引物
            fw = primer_info["fw"]
            fw_name = fw.get('name', f"{fragment_name}-F")
            self.result_text.insert(tk.END, f"{fw_name}: {fw['sequence']}\n")
            self.result_text.insert(tk.END, f"Tm值: {fw['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"GC含量: {fw['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"长度: {fw['length']} bp\n")
            
            # 显示结构问题
            structure_issues = []
            if fw.get('has_poly_x', False):
                structure_issues.append("连续重复碱基")
            if fw.get('has_hairpin', False):
                structure_issues.append("可能形成发夹结构")
            if fw.get('has_dimer', False):
                structure_issues.append("可能形成自二聚体")
            
            if structure_issues:
                self.result_text.insert(tk.END, f"结构问题: {', '.join(structure_issues)}\n")
            
            self.result_text.insert(tk.END, "\n")
            
            # 反向引物
            rv = primer_info["rv"]
            rv_name = rv.get('name', f"{fragment_name}-R")
            self.result_text.insert(tk.END, f"{rv_name}: {rv['sequence']}\n")
            self.result_text.insert(tk.END, f"Tm值: {rv['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"GC含量: {rv['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"长度: {rv['length']} bp\n")
            
            # 显示结构问题
            structure_issues = []
            if rv.get('has_poly_x', False):
                structure_issues.append("连续重复碱基")
            if rv.get('has_hairpin', False):
                structure_issues.append("可能形成发夹结构")
            if rv.get('has_dimer', False):
                structure_issues.append("可能形成自二聚体")
        
        if structure_issues:
            self.result_text.insert(tk.END, f"结构问题: {', '.join(structure_issues)}\n")
        
        # 如果存在引物二聚体问题
        if primer_info.get('primer_dimer', False):
            self.result_text.insert(tk.END, "\n警告: 正向和反向引物可能形成二聚体\n")
        
        self.result_text.insert(tk.END, "\n" + "-" * 40 + "\n\n")
    
    def export_results(self, format_type):
        """导出引物设计结果"""
        if not hasattr(self, 'primer_results'):
            messagebox.showerror("错误", "没有可导出的结果")
            return
        
        # 选择保存文件
        file_types = [("CSV文件", "*.csv")] if format_type == 'csv' else [("文本文件", "*.txt")]
        file_path = filedialog.asksaveasfilename(
            title="保存结果",
            filetypes=file_types,
            defaultextension=f".{format_type}"
        )
        
        if not file_path:
            return
        
        try:
            if format_type == 'csv':
                # 导出为CSV
                self.dna_tools.export_primers_to_csv(self.primer_results, file_path)
            else:
                # 导出为TXT
                self.dna_tools.export_primers_to_txt(self.primer_results, file_path)
            
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def export_primers_to_csv(self, primers, output_file):
        """将引物导出为CSV文件"""
        with open(output_file, 'w') as f:
            f.write("Primer Name,Sequence,Tm,GC%,Length,Issues\n")
            
            # 载体引物
            if "vector_primers" in primers:
                vector_primers = primers["vector_primers"]
                
                fw = vector_primers['fw']
                fw_name = fw.get('name', "Vector-F")
                issues_fw = []
                if fw.get('has_poly_x', False):
                    issues_fw.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    issues_fw.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    issues_fw.append("可能形成自二聚体")
                
                f.write(f"{fw_name},{fw['sequence']},{fw['tm']:.2f},{fw['gc_content']:.2f},{fw['length']},{';'.join(issues_fw)}\n")
                
                rv = vector_primers['rv']
                rv_name = rv.get('name', "Vector-R")
                issues_rv = []
                if rv.get('has_poly_x', False):
                    issues_rv.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    issues_rv.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    issues_rv.append("可能形成自二聚体")
                
                f.write(f"{rv_name},{rv['sequence']},{rv['tm']:.2f},{rv['gc_content']:.2f},{rv['length']},{';'.join(issues_rv)}\n")
            
            # 片段引物
            for primer_info in primers["fragment_primers"]:
                fragment_name = primer_info.get("name", "Fragment")
                
                fw = primer_info["fw"]
                fw_name = fw.get('name', f"{fragment_name}-F")
                issues_fw = []
                if fw.get('has_poly_x', False):
                    issues_fw.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    issues_fw.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    issues_fw.append("可能形成自二聚体")
                
                f.write(f"{fw_name},{fw['sequence']},{fw['tm']:.2f},{fw['gc_content']:.2f},{fw['length']},{';'.join(issues_fw)}\n")
                
                rv = primer_info["rv"]
                rv_name = rv.get('name', f"{fragment_name}-R")
                issues_rv = []
                if rv.get('has_poly_x', False):
                    issues_rv.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    issues_rv.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    issues_rv.append("可能形成自二聚体")
                
                f.write(f"{rv_name},{rv['sequence']},{rv['tm']:.2f},{rv['gc_content']:.2f},{rv['length']},{';'.join(issues_rv)}\n")
                
                if primer_info.get('primer_dimer', False):
                    f.write(f"{fragment_name}-Warning,正向和反向引物可能形成二聚体,,,,\n")
            
            # 添加署名、仓库地址和免责声明
            f.write("\n")
            f.write("本引物由Let's Gibson生成 / These primers were generated by Let's Gibson\n")
            f.write("项目地址 / Repository: https://github.com/goodenough1/LetsGibson\n")
            f.write("\n")
            f.write("免责声明：引物设计仅供参考，实际使用前请进行验证。\n")
            f.write("Disclaimer: Primer designs are for reference only. Please validate experimentally before actual use.\n")

    def export_primers_to_txt(self, primers, output_file):
        """将引物导出为TXT文件"""
        with open(output_file, 'w') as f:
            f.write("Gibson Assembly引物设计结果\n")
            f.write("=" * 80 + "\n\n")
            
            # 载体引物
            if "vector_primers" in primers:
                f.write("载体引物:\n")
                vector_primers = primers["vector_primers"]
                
                fw = vector_primers['fw']
                fw_name = fw.get('name', "Vector-F")
                f.write(f"{fw_name}: {fw['sequence']}\n")
                f.write(f"Tm值: {fw['tm']:.2f}°C\n")
                f.write(f"GC含量: {fw['gc_content']:.2f}%\n")
                f.write(f"长度: {fw['length']} bp\n")
                
                issues_fw = []
                if fw.get('has_poly_x', False):
                    issues_fw.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    issues_fw.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    issues_fw.append("可能形成自二聚体")
                
                if issues_fw:
                    f.write(f"结构问题: {', '.join(issues_fw)}\n")
                
                f.write("\n")
                
                rv = vector_primers['rv']
                rv_name = rv.get('name', "Vector-R")
                f.write(f"{rv_name}: {rv['sequence']}\n")
                f.write(f"Tm值: {rv['tm']:.2f}°C\n")
                f.write(f"GC含量: {rv['gc_content']:.2f}%\n")
                f.write(f"长度: {rv['length']} bp\n")
                
                issues_rv = []
                if rv.get('has_poly_x', False):
                    issues_rv.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    issues_rv.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    issues_rv.append("可能形成自二聚体")
                
                if issues_rv:
                    f.write(f"结构问题: {', '.join(issues_rv)}\n")
                
                # 添加分割线
                f.write("\n" + "-" * 80 + "\n\n")
            
            # 片段引物
            f.write("片段引物:\n\n")
            
            for primer_info in primers["fragment_primers"]:
                fragment_name = primer_info.get("name", "Fragment")
                f.write(f"{fragment_name}:\n")
                
                # 正向引物
                fw = primer_info["fw"]
                fw_name = fw.get('name', f"{fragment_name}-F")
                f.write(f"{fw_name}: {fw['sequence']}\n")
                f.write(f"Tm值: {fw['tm']:.2f}°C\n")
                f.write(f"GC含量: {fw['gc_content']:.2f}%\n")
                f.write(f"长度: {fw['length']} bp\n")
                
                # 显示结构问题
                structure_issues = []
                if fw.get('has_poly_x', False):
                    structure_issues.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    structure_issues.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    structure_issues.append("可能形成自二聚体")
                
                if structure_issues:
                    f.write(f"结构问题: {', '.join(structure_issues)}\n")
                
                f.write("\n")
                
                # 反向引物
                rv = primer_info["rv"]
                rv_name = rv.get('name', f"{fragment_name}-R")
                f.write(f"{rv_name}: {rv['sequence']}\n")
                f.write(f"Tm值: {rv['tm']:.2f}°C\n")
                f.write(f"GC含量: {rv['gc_content']:.2f}%\n")
                f.write(f"长度: {rv['length']} bp\n")
                
                # 显示结构问题
                structure_issues = []
                if rv.get('has_poly_x', False):
                    structure_issues.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    structure_issues.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    structure_issues.append("可能形成自二聚体")
                
                if structure_issues:
                    f.write(f"结构问题: {', '.join(structure_issues)}\n")
                
                # 如果存在引物二聚体问题
                if primer_info.get('primer_dimer', False):
                    f.write("\n警告: 正向和反向引物可能形成二聚体\n")
                
                f.write("\n" + "-" * 40 + "\n\n")
            
            # 添加署名、仓库地址和免责声明
            f.write("=" * 80 + "\n\n")
            f.write("本引物由Let's Gibson生成 / These primers were generated by Let's Gibson\n")
            f.write("项目地址 / Repository: https://github.com/goodenough1/LetsGibson\n")
            f.write("\n")
            f.write("免责声明：引物设计仅供参考，实际使用前请进行验证。\n")
            f.write("Disclaimer: Primer designs are for reference only. Please validate experimentally before actual use.\n")

    def show_about_dialog(self):
        """显示关于对话框，包含许可证信息"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于 Let's Gibson / About Let's Gibson")
        about_window.geometry("600x600")
        about_window.resizable(True, True)
        
        try:
            icon_path = f"{root_path}/assets/LetsGibson_subsize.ico"
            if os.path.exists(icon_path):
                about_window.iconbitmap(icon_path)
        except Exception as e:
            print(f"设置图标时出错: {str(e)}")
        
        # 添加JPG图片
        img_frame = ttk.Frame(about_window)
        img_frame.pack(fill=tk.X, padx=10, pady=5)
        
        try:
            # 尝试加载JPG图片
            from PIL import Image, ImageTk
            img_path = f"{root_path}/assets/LetsGibson.jpg"
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # 调整图片大小
                img = img.resize((500, 130), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # 创建标签显示图像
                img_label = ttk.Label(img_frame, image=photo)
                img_label.image = photo  # 保持引用，防止被垃圾回收
                img_label.pack(pady=5)
        except Exception as e:
            print(f"加载图片时出错: {str(e)}")
        
        # 添加版本号
        version_frame = ttk.Frame(about_window)
        version_frame.pack(fill=tk.X, padx=10, pady=5)
        
        version_label = ttk.Label(version_frame, text="Beta 0.0.1 / 测试版 0.0.1", font=("Arial", 12, "bold"))
        version_label.pack(pady=5)
        
        # 创建一个带滚动条的文本区域
        text_frame = ttk.Frame(about_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        about_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=70, height=25)
        about_text.pack(fill=tk.BOTH, expand=True)
        
        # 设置文本内容
        license_text = """Let's Gibson - Gibson Assembly Primer Design Tool
End-User License Agreement (CC BY-NC 4.0)

版权所有 (c) [2025] [DINGYi,4D Genome Lab]
[francisding@qq.com, 4dgenome.net]

本作品包括：

Let's Gibson 源码（github仓库scripts中的文件）
Let's Gibson 可执行文件 (LetsGibson.exe)
GUI 设计
文档和图形资产（Logo等）

基于知识共享署名-非商业性使用 4.0 国际许可协议授权。
完整文本：https://creativecommons.org/licenses/by-nc/4.0/legalcode

您可以：

分享 - 复制和分发材料
改编 - 重混、转换或基于材料创建

条件：

署名 - 明显标注"Let's Gibson"及其Logo，链接到许可证，指明所做的更改

非商业性使用 - 不得用于商业目的，包括：
• 商业实体中的付费服务
• 集成到营利性软件中
• 通过订阅/广告进行变现

特别规定：

商标保护：
不得修改衍生作品中的Logo
禁止非官方界面克隆
禁止未经授权的商品销售

技术限制：
禁止对LetsGibson.exe进行逆向工程
禁止开发功能克隆

责任免除：
示例文件不保证可用
需要实验验证
不对实验成本承担责任

使用本软件的结果时，用户应注明软件来源和此仓库地址：
https://github.com/goodenough1/LetsGibson

---------------------------------------------

Let's Gibson - Gibson Assembly Primer Design Tool
End-User License Agreement (CC BY-NC 4.0)

Copyright (c) [2025] [DINGYi,4D Genome Lab]
[francisding@qq.com, 4dgenome.net]

This work includes:

Let's Gibson source（Files in scripts folder in github repositories.）
Let's Gibson executable (LetsGibson.exe)
GUI design
Documentation & graphical assets (Logo, etc.)

Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode

You may:

Share - reproduce and distribute the material
Adapt - remix, transform, or build upon the material

Under conditions:

Attribution - Visibly credit "Let's Gibson" with Logo, link to license, indicate changes

NonCommercial - No commercial use including:
• Paid services in commercial entities
• Integration into for-profit software
• Monetization via subscriptions/ads

Special Provisions:

Trademark Protection:
No modification of Logo in derivatives
Prohibit unofficial interface cloning
Unauthorized merchandising forbidden

Technical Restrictions:
Reverse engineering of LetsGibson.exe prohibited
No functional clone development

Liability Exclusion:
Example files not guaranteed usable
Experimental validation required
No liability for experimental costs

When using the results of the software, the user should indicate the source of the software and the address of this repository:
https://github.com/goodenough1/LetsGibson
"""
        
        about_text.insert(tk.END, license_text)
        about_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 添加确定按钮
        ok_btn = ttk.Button(about_window, text="确定 / OK", command=about_window.destroy)
        ok_btn.pack(pady=10)
        
        # 使对话框模态
        about_window.transient(self.root)
        about_window.grab_set()
        self.root.wait_window(about_window)


def main():
    root = tk.Tk()
    app = GibsonPrimerDesignApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()