# 基于Leave-Cluster-Out策略的交叉验证数据准备软件  
## 1. 软件简介  
此软件的功能是，将大量分子数据按照分子相似性以用户指定的簇数进行聚类，并按照给定的交叉验证折数和测试集比例自动且相对均衡地从每个簇中抽取数据，继而生成相对应的训练集与测试集以便于下一步的交叉验证。  
这样做的目的，便是模拟机器学习中交叉验证的过程并将分子结构特性纳入考虑，让参与交叉验证的每一折数据均包括各种不同结构的分子，使得模型评价更加合理、精准。  
## 2. 软件基本信息  
- 英文简称：`LCO-CVDP`  
- 面向领域：`生物医药`、`药物化学`、`药物研发`、`机器学习`  
- 编程语言：`Python`  
- 软件版本：`0.1.0`  
## 3. 使用说明  
### 3.1. 运行环境  
- 硬件环境  
  - 处理器：`1GHz` `32位`或`64位`处理器  
  - 内存空间：`32MB`及以上  
  - 硬盘空间：`1GB`及以上  
- 软件环境  
  - 操作系统：`Windows 7`及以上，或`Ubuntu 18.04`及以上  
  - 环境依赖：`Python 3.8`  
### 3.2. 软件安装  
1. 在`3.1. 运行环境`所述硬件环境的机器中及符合`3.1. 运行环境`所述软件环境中要求的操作系统下，安装`3.1. 运行环境`所述软件环境中的环境依赖。  
2. 在用户有读写权限的目录启动终端命令行，并执行：  
```sh  
git clone https://github.com/Wenying-Yu-Lab/LCO-CVDP.git
cd LCO-CVDP
pip install -r requirements.txt
```  
### 3.3. 使用方法  
1. 准备包含输入数据的表格文件，并应满足以下要求：  
   1. 输入文件是逗号分隔值文件(`*.csv`)  
   2. 表格包括标题行  
   3. 表格的某一列记录了一系列以`SMILES`格式记录的分子结构  
   4. 所在目录可读  
2. 确定启动参数，包括：
   1. 位置参数  
      1. `{data_path}`：将花括号中的字符替换为输入文件的路径。  
   2. 必选参数  
      1. `-n {N_CLUSTERS}`或`--n-clusters {N_CLUSTERS}`：将花括号中的字符替换为聚类的簇数。  
   3. 可选参数  
      1. `[-f {FOLDS}]`或`[--folds {FOLDS}]`： 将花括号中的字符替换为交叉验证的折数（默认为`10`）。  
      2. `[-c {STRUCTURE_COLUMN_HEADER}]`或`[--column-header {STRUCTURE_COLUMN_HEADER}]`：将花括号中的字符替换为表格中以`SMILES`格式记录分子结构的列标题（默认为`smiles`）。  
      3. `[--et-ratio {EXTERNAL_TEST_RATIO}]`：将花括号中的字符替换为将要分出的外部测试集所占的比例（默认为`0.2`）。  
      4. `[-o {OUTPUT_DIR}]`或`[--output-dir {OUTPUT_DIR}]`：将花括号中的字符替换为保存结果的目录路径（默认为`./model_data_out`即当前目录下的`model_data_out`目录）。目录不存在时，程序将尝试创建。  
3. 在当前目录启动终端命令行，并运行以下命令（将花括号中的字符按照上一步骤的提示进行更换，如果不改变某个可选参数的默认值，可以将方括号中的字符连同中括号本身一并省略）：  
```sh  
python -u src/main.py -n {N_CLUSTERS} [-f {FOLDS}] [-c {STRUCTURE_COLUMN_HEADER}] [--et-ratio {EXTERNAL_TEST_RATIO}] [-o {OUTPUT_DIR}] {data_path}
```  
4. 等待程序执行完毕，并可在保存结果的目录路径（应该为`./model_data_out`除非用户在启动时进行了更改）获取数据。  