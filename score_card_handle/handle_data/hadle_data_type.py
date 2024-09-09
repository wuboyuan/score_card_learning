import pandas as pd
import numpy as np


class DataPreprocessing():

    # 检查变量类型并返回对应的字符串表示
    def check_variable_type(self, var):
        # 定义常见的数据类型与对应的字符串映射
        types = {
            str: "字符串",  # 字符串类型
            list: "列表",  # 列表类型
            dict: "字典",  # 字典类型
            (int, float): "数字",  # 数字类型，包括整型和浮点型
            pd.DataFrame: "DataFrame",  # Pandas DataFrame 类型
            np.ndarray: "向量",  # NumPy 数组，代表向量
            pd.Series: "Series"  # Pandas Series 类型
        }

        # 遍历字典，检查变量是否属于某种类型
        for var_type, var_name in types.items():
            if isinstance(var, var_type):
                return var_name  # 返回匹配的类型名称
        return "未知类型"  # 如果没有匹配，返回“未知类型”

    # 数据描述：根据输入参数 typed 来描述不同类型的数据
    def data_describe(self, var, typed="all"):
        if typed == "object":
            # 如果指定类型为 "object"，返回字符串类型的描述信息
            return var[self.dataframe_col_str(var)].describe(include=['object'])
        elif typed == "number":
            # 如果指定类型为 "number"，返回数值类型的描述信息
            return var[self.dataframe_col_num(var)].describe(include=['number'])
        elif typed == "all":
            # 如果指定类型为 "all"，分别描述数值和字符串类型的数据
            return (
                var[self.dataframe_col_num(var)].describe(include=['number']),  # 数值类型描述
                var[self.dataframe_col_str(var)].describe(include=['object'])  # 字符串类型描述
            )

    # 获取字符串类型的列名
    def dataframe_col_str(self, var):
        return var.select_dtypes(include=['object']).columns  # 返回 DataFrame 中字符串类型的列名

    # 获取数值类型的列名
    def dataframe_col_num(self, var):
        return var.select_dtypes(include=['number']).columns  # 返回 DataFrame 中数值类型的列名

    # 处理数值列中的缺失值
    def data_null_hand_num(self, var, method='null', nv=-999):
        var = var[self.dataframe_col_num(var)]  # 选择 DataFrame 中数值类型的列
        # 根据不同的填充方法处理数值列中的缺失值
        if method == "mean":
            return var.fillna(var.mean(), inplace=True)  # 使用均值填充
        elif method == "median":
            return var.fillna(var.median(), inplace=True)  # 使用中位数填充
        elif method == "mode":
            return var.fillna(var.mode()[0], inplace=True)  # 使用众数填充
        elif method == "ff":
            return var.fillna(method='ffill', inplace=True)  # 前向填充
        elif method == "bf":
            return var.fillna(method='bfill', inplace=True)  # 后向填充
        elif method == "linear":
            return var.interpolate(method='linear', inplace=True)  # 使用线性插值填充
        elif method == "dro_col":
            return var.dropna(axis=0, inplace=True)  # 删除含有缺失值的行
        elif method == "dro_axi":
            return var.dropna(axis=1, inplace=True)  # 删除含有缺失值的列
        else:
            return var.fillna(nv, inplace=True)  # 使用指定的常数值 nv 填充

    # 处理字符串列中的缺失值
    def data_null_hand_str(self, var, method='null', nv='Unknown'):
        str_c = self.dataframe_col_str(var)  # 获取字符串列
        var = var[str_c]  # 选择字符串列进行处理
        # 根据不同的方法处理字符串列中的缺失值
        if method == "mode":
            for string_column in str_c:
                most_frequent = var[string_column].mode()[0]  # 获取众数
                var[string_column].fillna(most_frequent, inplace=True)  # 使用众数填充缺失值
            return var
        else:
            return var.fillna(nv, inplace=True)  # 使用指定的字符串值 nv 填充
