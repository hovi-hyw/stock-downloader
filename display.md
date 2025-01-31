# 一、股票相关下载

## 1.1 获取股票 列表

接口: stock_zh_a_spot

目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_a

描述: 新浪财经-沪深京 A 股数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔

限量: 单次返回沪深京 A 股上市公司的实时行情数据

输入参数: 无


```python
from django.contrib.admin import display
import akshare as ak
stock_list = ak.stock_zh_a_spot()
display(stock_list)
```

                                                                             




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>代码</th>
      <th>名称</th>
      <th>最新价</th>
      <th>涨跌额</th>
      <th>涨跌幅</th>
      <th>买入</th>
      <th>卖出</th>
      <th>昨收</th>
      <th>今开</th>
      <th>最高</th>
      <th>最低</th>
      <th>成交量</th>
      <th>成交额</th>
      <th>时间戳</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>bj430017</td>
      <td>星昊医药</td>
      <td>13.87</td>
      <td>0.07</td>
      <td>0.507</td>
      <td>13.86</td>
      <td>13.87</td>
      <td>13.80</td>
      <td>13.98</td>
      <td>14.23</td>
      <td>13.87</td>
      <td>1399591.0</td>
      <td>19673771.0</td>
      <td>15:30:02</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bj430047</td>
      <td>诺思兰德</td>
      <td>11.38</td>
      <td>-0.21</td>
      <td>-1.812</td>
      <td>11.38</td>
      <td>11.47</td>
      <td>11.59</td>
      <td>11.71</td>
      <td>11.95</td>
      <td>11.38</td>
      <td>1389714.0</td>
      <td>16243846.0</td>
      <td>15:30:02</td>
    </tr>
    <tr>
      <th>2</th>
      <td>bj430090</td>
      <td>同辉信息</td>
      <td>5.81</td>
      <td>0.04</td>
      <td>0.693</td>
      <td>5.81</td>
      <td>5.82</td>
      <td>5.77</td>
      <td>5.85</td>
      <td>6.18</td>
      <td>5.80</td>
      <td>8441210.0</td>
      <td>50492606.0</td>
      <td>15:30:02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>bj430139</td>
      <td>华岭股份</td>
      <td>24.90</td>
      <td>-0.62</td>
      <td>-2.429</td>
      <td>24.89</td>
      <td>24.90</td>
      <td>25.52</td>
      <td>26.40</td>
      <td>26.88</td>
      <td>24.85</td>
      <td>10219863.0</td>
      <td>265832233.0</td>
      <td>15:30:02</td>
    </tr>
    <tr>
      <th>4</th>
      <td>bj430198</td>
      <td>微创光电</td>
      <td>11.50</td>
      <td>-0.10</td>
      <td>-0.862</td>
      <td>11.49</td>
      <td>11.50</td>
      <td>11.60</td>
      <td>11.51</td>
      <td>12.10</td>
      <td>11.23</td>
      <td>8427035.0</td>
      <td>98356689.0</td>
      <td>15:30:02</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5387</th>
      <td>sz301622</td>
      <td>英思特</td>
      <td>68.00</td>
      <td>1.24</td>
      <td>1.857</td>
      <td>68.00</td>
      <td>68.01</td>
      <td>66.76</td>
      <td>67.20</td>
      <td>69.69</td>
      <td>66.98</td>
      <td>5342000.0</td>
      <td>367542336.0</td>
      <td>15:35:00</td>
    </tr>
    <tr>
      <th>5388</th>
      <td>sz301626</td>
      <td>苏州天脉</td>
      <td>88.30</td>
      <td>-1.20</td>
      <td>-1.341</td>
      <td>88.30</td>
      <td>88.34</td>
      <td>89.50</td>
      <td>90.50</td>
      <td>90.96</td>
      <td>88.30</td>
      <td>1287009.0</td>
      <td>115471193.0</td>
      <td>15:35:15</td>
    </tr>
    <tr>
      <th>5389</th>
      <td>sz301628</td>
      <td>强达电路</td>
      <td>116.22</td>
      <td>2.17</td>
      <td>1.903</td>
      <td>116.22</td>
      <td>116.31</td>
      <td>114.05</td>
      <td>111.11</td>
      <td>118.79</td>
      <td>108.88</td>
      <td>7813173.0</td>
      <td>886539659.0</td>
      <td>15:35:30</td>
    </tr>
    <tr>
      <th>5390</th>
      <td>sz301631</td>
      <td>壹连科技</td>
      <td>121.98</td>
      <td>-0.84</td>
      <td>-0.684</td>
      <td>121.97</td>
      <td>121.98</td>
      <td>122.82</td>
      <td>124.01</td>
      <td>126.66</td>
      <td>121.97</td>
      <td>1550877.0</td>
      <td>193279116.0</td>
      <td>15:35:45</td>
    </tr>
    <tr>
      <th>5391</th>
      <td>sz301633</td>
      <td>港迪技术</td>
      <td>89.79</td>
      <td>-2.37</td>
      <td>-2.572</td>
      <td>89.70</td>
      <td>89.79</td>
      <td>92.16</td>
      <td>91.81</td>
      <td>92.44</td>
      <td>89.00</td>
      <td>1933296.0</td>
      <td>174961899.0</td>
      <td>15:35:00</td>
    </tr>
  </tbody>
</table>
<p>5392 rows × 14 columns</p>
</div>



## 1.2 获取个股 历史数据
接口: stock_zh_a_daily

目标地址: https://finance.sina.com.cn/realstock/company/sh600006/nc.shtml(示例)

描述: 新浪财经-沪深京 A 股的数据, 历史数据按日频率更新;

限量: 单次返回指定沪深京 A 股上市公司指定日期间的历史行情日频率数据, 多次获取容易封禁 IP

输入参数

| 名称         | 类型  | 描述                                                                                   |
|------------|-----|--------------------------------------------------------------------------------------|
| symbol     | str | symbol='sh600000'; 股票代码可以在 **ak.stock_zh_a_spot()** 中获取                              |
| start_date | str | start_date='20201103'; 开始查询的日期                                                       |
| end_date   | str | end_date='20201116'; 结束查询的日期                                                         |
| adjust     | str | 默认返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; hfq-factor: 返回后复权因子; qfq-factor: 返回前复权因子 |


```python
from django.contrib.admin import display
import akshare as ak

stock_data = ak.stock_zh_a_daily(symbol="sz000001", start_date="20250101", end_date="20990101")
display(stock_data)
```


    ---------------------------------------------------------------------------

    OptionError                               Traceback (most recent call last)

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\IPython\core\formatters.py:406, in BaseFormatter.__call__(self, obj)
        404     method = get_real_method(obj, self.print_method)
        405     if method is not None:
    --> 406         return method()
        407     return None
        408 else:
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\core\frame.py:1256, in DataFrame._repr_html_(self)
       1234     show_dimensions = get_option("display.show_dimensions")
       1236     formatter = fmt.DataFrameFormatter(
       1237         self,
       1238         columns=None,
       (...)
       1254         decimal=".",
       1255     )
    -> 1256     return fmt.DataFrameRenderer(formatter).to_html(notebook=True)
       1257 else:
       1258     return None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\format.py:929, in DataFrameRenderer.to_html(self, buf, encoding, classes, notebook, border, table_id, render_links)
        922 from pandas.io.formats.html import (
        923     HTMLFormatter,
        924     NotebookFormatter,
        925 )
        927 Klass = NotebookFormatter if notebook else HTMLFormatter
    --> 929 html_formatter = Klass(
        930     self.fmt,
        931     classes=classes,
        932     border=border,
        933     table_id=table_id,
        934     render_links=render_links,
        935 )
        936 string = html_formatter.to_string()
        937 return save_to_buffer(string, buf=buf, encoding=encoding)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\html.py:68, in HTMLFormatter.__init__(self, formatter, classes, border, table_id, render_links)
         66 self.show_dimensions = self.fmt.show_dimensions
         67 if border is None or border is True:
    ---> 68     border = cast(int, get_option("func.html.border"))
         69 elif not border:
         70     border = None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:274, in CallableDynamicDoc.__call__(self, *args, **kwds)
        273 def __call__(self, *args, **kwds) -> T:
    --> 274     return self.__func__(*args, **kwds)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:146, in _get_option(pat, silent)
        145 def _get_option(pat: str, silent: bool = False) -> Any:
    --> 146     key = _get_single_key(pat, silent)
        148     # walk the nested dict
        149     root, k = _get_root(key)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:132, in _get_single_key(pat, silent)
        130     if not silent:
        131         _warn_if_deprecated(pat)
    --> 132     raise OptionError(f"No such keys(s): {repr(pat)}")
        133 if len(keys) > 1:
        134     raise OptionError("Pattern matched multiple keys")
    

    OptionError: No such keys(s): 'func.html.border'





              date   open   high    low  close       volume        amount  \
    0   2025-01-02  11.73  11.77  11.39  11.43  181959699.0  2.102923e+09   
    1   2025-01-03  11.44  11.54  11.36  11.38  115468044.0  1.320521e+09   
    2   2025-01-06  11.38  11.48  11.22  11.44  108553630.0  1.234306e+09   
    3   2025-01-07  11.42  11.53  11.37  11.51   74786288.0  8.583290e+08   
    4   2025-01-08  11.50  11.63  11.40  11.50  106238601.0  1.223599e+09   
    5   2025-01-09  11.50  11.50  11.35  11.40   75148330.0  8.578361e+08   
    6   2025-01-10  11.40  11.46  11.28  11.30   79813351.0  9.050050e+08   
    7   2025-01-13  11.25  11.26  11.08  11.20   93496618.0  1.044904e+09   
    8   2025-01-14  11.20  11.40  11.19  11.38   82462895.0  9.344678e+08   
    9   2025-01-15  11.38  11.58  11.36  11.48  103163082.0  1.185404e+09   
    10  2025-01-16  11.55  11.59  11.47  11.57   87296399.0  1.007689e+09   
    11  2025-01-17  11.53  11.55  11.42  11.45   68976486.0  7.912304e+08   
    12  2025-01-20  11.50  11.52  11.40  11.42   83202913.0  9.530922e+08   
    13  2025-01-21  11.45  11.45  11.32  11.33   90206894.0  1.024879e+09   
    14  2025-01-22  11.32  11.33  11.08  11.09  134712922.0  1.504819e+09   
    15  2025-01-23  11.17  11.40  11.17  11.32  151492027.0  1.715172e+09   
    
        outstanding_share  turnover  
    0        1.940562e+10  0.009377  
    1        1.940562e+10  0.005950  
    2        1.940562e+10  0.005594  
    3        1.940562e+10  0.003854  
    4        1.940562e+10  0.005475  
    5        1.940562e+10  0.003873  
    6        1.940562e+10  0.004113  
    7        1.940562e+10  0.004818  
    8        1.940562e+10  0.004249  
    9        1.940562e+10  0.005316  
    10       1.940562e+10  0.004499  
    11       1.940562e+10  0.003554  
    12       1.940562e+10  0.004288  
    13       1.940562e+10  0.004648  
    14       1.940562e+10  0.006942  
    15       1.940562e+10  0.007807  




```python
display(stock_data.columns)
print(stock_data.dtypes)
```

    date                  object
    open                 float64
    high                 float64
    low                  float64
    close                float64
    volume               float64
    amount               float64
    outstanding_share    float64
    turnover             float64
    dtype: object
    

# 二、 指数相关下载
## 2.1 获取指数 列表

实时行情数据-新浪
接口: stock_zh_index_spot_sina

目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_s

描述: 新浪财经-中国股票指数数据

限量: 单次返回所有指数的实时行情数据


```python
import akshare as ak

stock_zh_index_spot_sina_df = ak.stock_zh_index_spot_sina()
display(stock_zh_index_spot_sina_df)
```


      0%|          | 0/8 [00:00<?, ?it/s]



    ---------------------------------------------------------------------------

    OptionError                               Traceback (most recent call last)

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\IPython\core\formatters.py:406, in BaseFormatter.__call__(self, obj)
        404     method = get_real_method(obj, self.print_method)
        405     if method is not None:
    --> 406         return method()
        407     return None
        408 else:
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\core\frame.py:1256, in DataFrame._repr_html_(self)
       1234     show_dimensions = get_option("display.show_dimensions")
       1236     formatter = fmt.DataFrameFormatter(
       1237         self,
       1238         columns=None,
       (...)
       1254         decimal=".",
       1255     )
    -> 1256     return fmt.DataFrameRenderer(formatter).to_html(notebook=True)
       1257 else:
       1258     return None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\format.py:929, in DataFrameRenderer.to_html(self, buf, encoding, classes, notebook, border, table_id, render_links)
        922 from pandas.io.formats.html import (
        923     HTMLFormatter,
        924     NotebookFormatter,
        925 )
        927 Klass = NotebookFormatter if notebook else HTMLFormatter
    --> 929 html_formatter = Klass(
        930     self.fmt,
        931     classes=classes,
        932     border=border,
        933     table_id=table_id,
        934     render_links=render_links,
        935 )
        936 string = html_formatter.to_string()
        937 return save_to_buffer(string, buf=buf, encoding=encoding)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\html.py:68, in HTMLFormatter.__init__(self, formatter, classes, border, table_id, render_links)
         66 self.show_dimensions = self.fmt.show_dimensions
         67 if border is None or border is True:
    ---> 68     border = cast(int, get_option("func.html.border"))
         69 elif not border:
         70     border = None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:274, in CallableDynamicDoc.__call__(self, *args, **kwds)
        273 def __call__(self, *args, **kwds) -> T:
    --> 274     return self.__func__(*args, **kwds)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:146, in _get_option(pat, silent)
        145 def _get_option(pat: str, silent: bool = False) -> Any:
    --> 146     key = _get_single_key(pat, silent)
        148     # walk the nested dict
        149     root, k = _get_root(key)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:132, in _get_single_key(pat, silent)
        130     if not silent:
        131         _warn_if_deprecated(pat)
    --> 132     raise OptionError(f"No such keys(s): {repr(pat)}")
        133 if len(keys) > 1:
        134     raise OptionError("Pattern matched multiple keys")
    

    OptionError: No such keys(s): 'func.html.border'



               代码      名称        最新价      涨跌额    涨跌幅         昨收         今开  \
    0    sh000001    上证指数  3252.6264   22.463  0.695  3230.1637  3222.8774   
    1    sh000002    Ａ股指数  3409.0079   23.560  0.696  3385.4477  3377.8010   
    2    sh000003    Ｂ股指数   265.4780    1.955  0.742   263.5232   263.6428   
    3    sh000004    工业指数  2810.4132   25.239  0.906  2785.1743  2779.0269   
    4    sh000005    商业指数  2543.8511   17.921  0.709  2525.9303  2520.7897   
    ..        ...     ...        ...      ...    ...        ...        ...   
    557  sz980030    消费电子  5596.1820  131.858  2.413  5464.3240  5453.1940   
    558  sz980032    新能电池  9632.0280  132.329  1.393  9499.6990  9469.8680   
    559  sz980035    化肥农药  1553.1250   14.909  0.969  1538.2160  1537.0050   
    560  sz980076    通用航空  2773.8430   27.148  0.988  2746.6950  2743.0240   
    561  sz980092  CNIFCF  4601.0500   36.980  0.810  4564.0700  4552.3690   
    
                最高         最低         成交量           成交额  
    0    3260.0112  3221.7121   398653033  480685057973  
    1    3416.7459  3376.5855   398388294  480194309360  
    2     265.4904   263.1377      188921      85108366  
    3    2816.8757  2778.3970   242468874  355638354577  
    4    2550.6138  2511.5204    33470944   30831988582  
    ..         ...        ...         ...           ...  
    557  5600.0560  5453.1940  2598714701   60508779579  
    558  9709.7360  9469.8680   607669438   21873270653  
    559  1554.3750  1534.1250  1268904977   11735310972  
    560  2784.0910  2739.6160   689491721   14148681042  
    561  4605.5800  4542.5610  3436173676   37338531291  
    
    [562 rows x 11 columns]



```python
# 东财获取指数的方法
import akshare as ak
df = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
display(df)
```


    ---------------------------------------------------------------------------

    OptionError                               Traceback (most recent call last)

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\IPython\core\formatters.py:406, in BaseFormatter.__call__(self, obj)
        404     method = get_real_method(obj, self.print_method)
        405     if method is not None:
    --> 406         return method()
        407     return None
        408 else:
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\core\frame.py:1256, in DataFrame._repr_html_(self)
       1234     show_dimensions = get_option("display.show_dimensions")
       1236     formatter = fmt.DataFrameFormatter(
       1237         self,
       1238         columns=None,
       (...)
       1254         decimal=".",
       1255     )
    -> 1256     return fmt.DataFrameRenderer(formatter).to_html(notebook=True)
       1257 else:
       1258     return None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\format.py:929, in DataFrameRenderer.to_html(self, buf, encoding, classes, notebook, border, table_id, render_links)
        922 from pandas.io.formats.html import (
        923     HTMLFormatter,
        924     NotebookFormatter,
        925 )
        927 Klass = NotebookFormatter if notebook else HTMLFormatter
    --> 929 html_formatter = Klass(
        930     self.fmt,
        931     classes=classes,
        932     border=border,
        933     table_id=table_id,
        934     render_links=render_links,
        935 )
        936 string = html_formatter.to_string()
        937 return save_to_buffer(string, buf=buf, encoding=encoding)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\html.py:68, in HTMLFormatter.__init__(self, formatter, classes, border, table_id, render_links)
         66 self.show_dimensions = self.fmt.show_dimensions
         67 if border is None or border is True:
    ---> 68     border = cast(int, get_option("func.html.border"))
         69 elif not border:
         70     border = None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:274, in CallableDynamicDoc.__call__(self, *args, **kwds)
        273 def __call__(self, *args, **kwds) -> T:
    --> 274     return self.__func__(*args, **kwds)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:146, in _get_option(pat, silent)
        145 def _get_option(pat: str, silent: bool = False) -> Any:
    --> 146     key = _get_single_key(pat, silent)
        148     # walk the nested dict
        149     root, k = _get_root(key)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:132, in _get_single_key(pat, silent)
        130     if not silent:
        131         _warn_if_deprecated(pat)
    --> 132     raise OptionError(f"No such keys(s): {repr(pat)}")
        133 if len(keys) > 1:
        134     raise OptionError("Pattern matched multiple keys")
    

    OptionError: No such keys(s): 'func.html.border'



        序号      代码       名称       最新价   涨跌幅     涨跌额        成交量           成交额  \
    0    1  000001     上证指数   3252.63  0.70   22.47  398653033  4.806851e+11   
    1    2  399001     深证成指  10292.73  1.15  116.56  589944330  7.413316e+11   
    2    3  899050     北证50   1079.22  0.60    6.44    6378294  1.186400e+10   
    3    4  399006     创业板指   2121.84  1.36   28.53  200051426  3.607832e+11   
    4    5  000680     科创综指   1124.95  1.56   17.33   26768503  9.973191e+10   
    5    6  000688     科创50    974.83  0.90    8.72   26768503  9.973191e+10   
    6    7  399750    深主板50   8203.07  0.74   60.22   30826753  5.552057e+10   
    7    8  000300    沪深300   3832.86  0.77   29.12  148971722  2.964744e+11   
    8    9  000016     上证50   2579.10  0.45   11.62   37663633  7.479326e+10   
    9   10  399850     深证50   7188.15  0.81   57.77   30849463  9.173615e+10   
    10  11  000888  上证综合全收益   3635.86  0.73   26.27  398653033  4.806851e+11   
    11  12  399005    中小100   6335.93  1.36   84.95   35423634  7.001095e+10   
    12  13  930050    中证A50   1524.15  0.84   12.66   34232282  8.876061e+10   
    13  14  000903   中证A100   3628.49  0.76   27.45   64678690  1.511020e+11   
    14  15  000510   中证A500   4504.01  0.90   40.04  226679026  3.941103e+11   
    15  16  000904    中证200   4517.12  1.03   46.19   70884469  1.456732e+11   
    16  17  000905    中证500   5649.95  1.18   65.70  139438058  1.808588e+11   
    17  18  000906    中证800   4130.42  0.87   35.65  288409780  4.773332e+11   
    18  19  000852   中证1000   5938.13  1.87  109.10  208090445  2.791480e+11   
    19  20  932000   中证2000   2362.20  1.45   33.80  310345491  3.337952e+11   
    20  21  000985     中证全指   4674.23  1.09   50.60  968113802  1.209347e+12   
    21  22  000010    上证180   8365.41  0.80   66.25   95097288  1.563868e+11   
    22  23  000009    上证380   5364.22  1.32   69.98   56618399  9.521148e+10   
    23  24  000132    上证100   5126.78  1.30   65.59    8174122  2.196617e+10   
    24  25  000133    上证150   4531.11  1.55   69.24   13546246  2.127063e+10   
    25  26  000003     Ｂ股指数    265.48  0.74    1.96     188921  8.510837e+07   
    26  27  000012     国债指数    223.42 -0.02   -0.05    4090183  4.300714e+09   
    27  28  000013     企债指数    294.63  0.01    0.04    2135660  2.010535e+09   
    28  29  000011     基金指数   6718.08  0.92   61.47  952135564  1.785312e+11   
    29  30  399002     深成指R  13573.87  1.19  159.18  389669830  3.804860e+11   
    30  31  399003     成份Ｂ指   7886.10  0.46   35.77     223073  6.237059e+07   
    31  32  399106     深证综指   1936.34  1.21   23.08  589944330  7.413316e+11   
    32  33  399004   深证100R   6399.56  1.01   63.72   47427750  1.316978e+11   
    33  34  399007    深证300   4329.95  1.06   45.34  104930353  2.252774e+11   
    34  35  399008    中小300   1276.54  1.40   17.66  102684537  1.451203e+11   
    35  36  399293     创业大盘   4041.24  1.15   45.94   14488479  6.730950e+10   
    36  37  399019    创业200   3528.93  2.79   95.69   58647637  9.302406e+10   
    37  38  399020     创业小盘   1394.98  2.18   29.70   43792298  7.708357e+10   
    38  39  399100      新指数   9118.90  1.21  109.09  575362650  7.350421e+11   
    39  40  399550     央视50   7179.45  0.75   53.76   22611716  5.191563e+10   
    
          振幅        最高        最低        今开        昨收    量比  
    0   1.19   3260.01   3221.71   3222.88   3230.16  1.00  
    1   1.71  10315.37  10141.41  10141.41  10176.17  1.00  
    2   2.38   1082.67   1057.14   1065.55   1072.78  0.91  
    3   2.27   2131.55   2084.13   2084.13   2093.31  1.10  
    4   2.02   1128.34   1106.02   1106.02   1107.62  1.04  
    5   1.48    980.43    966.09    966.09    966.11  1.04  
    6   1.35   8225.16   8115.58   8122.04   8142.85  0.95  
    7   1.42   3847.60   3793.48   3793.85   3803.74  1.03  
    8   1.37   2594.58   2559.49   2562.87   2567.48  0.96  
    9   1.65   7223.24   7105.40   7105.40   7130.38  0.89  
    10  1.19   3644.11   3601.30   3602.60   3609.59  1.00  
    11  1.73   6341.51   6233.56   6234.98   6250.98  1.13  
    12  1.66   1533.48   1508.45   1508.64   1511.49  0.98  
    13  1.46   3646.55   3594.02   3594.96   3601.04  0.97  
    14  1.51   4519.86   4452.43   4452.77   4463.97  1.05  
    15  1.41   4523.48   4460.46   4460.97   4470.93  1.02  
    16  1.61   5660.43   5570.48   5570.48   5584.25  1.04  
    17  1.45   4143.59   4084.18   4084.26   4094.77  1.04  
    18  2.19   5943.11   5815.46   5815.46   5829.03  1.04  
    19  2.08   2364.58   2316.06   2319.68   2328.40  0.97  
    20  1.49   4679.50   4610.79   4610.86   4623.63  1.00  
    21  1.38   8394.55   8280.25   8282.77   8299.16  1.08  
    22  1.62   5369.23   5283.46   5283.66   5294.24  1.02  
    23  1.84   5145.45   5052.09   5055.06   5061.19  1.01  
    24  1.95   4537.79   4451.00   4451.00   4461.87  1.03  
    25  0.89    265.49    263.14    263.64    263.52  0.86  
    26  0.05    223.49    223.38    223.49    223.47  0.50  
    27  0.01    294.64    294.62    294.62    294.59  0.36  
    28  1.22   6732.64   6651.24   6652.82   6656.61  1.04  
    29  1.71  13603.74  13374.31  13374.31  13414.69  0.96  
    30  0.69   7886.95   7832.43   7841.43   7850.33  1.19  
    31  1.62   1938.19   1907.21   1907.21   1913.26  1.00  
    32  1.71   6426.64   6318.57   6318.57   6335.84  0.96  
    33  1.69   4343.47   4271.20   4271.20   4284.61  1.03  
    34  1.79   1277.47   1254.98   1255.18   1258.88  0.98  
    35  2.16   4064.06   3977.78   3977.78   3995.30  0.99  
    36  3.26   3532.96   3420.94   3420.94   3433.24  1.22  
    37  2.54   1395.89   1361.27   1361.27   1365.28  1.05  
    38  1.62   9127.53   8981.71   8981.71   9009.81  1.00  
    39  1.48   7209.49   7104.11   7111.36   7125.69  1.00  



```python
# sina获取指数的方法
display(df.columns)
print(df.dtypes)
```


    Index(['序号', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '最高', '最低',
           '今开', '昨收', '量比'],
          dtype='object')


    序号       int64
    代码      object
    名称      object
    最新价    float64
    涨跌幅    float64
    涨跌额    float64
    成交量      int64
    成交额    float64
    振幅     float64
    最高     float64
    最低     float64
    今开     float64
    昨收     float64
    量比     float64
    dtype: object
    

## 2.2 获取指数 数据

接口: index_zh_a_hist

目标地址: http://quote.eastmoney.com/center/hszs.html

描述: 东方财富网-中国股票指数-行情数据

限量: 单次返回具体指数指定 period 从 start_date 到 end_date 的之间的近期数据

输入参数

| 名称        | 类型   | 描述                                         |
|-------------|--------|----------------------------------------------|
| symbol      | str    | symbol="399282"; 指数代码，此处不用市场标识   |
| period      | str    | period="daily"; choice of {'daily', 'weekly', 'monthly'} |
| start_date  | str    | start_date="19700101"; 开始日期               |
| end_date    | str    | end_date="22220101"; 结束时间                 |




```python
index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000001", period="daily", start_date="20241020", end_date="20900101")
display(index_zh_a_hist_df)
```


    ---------------------------------------------------------------------------

    OptionError                               Traceback (most recent call last)

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\IPython\core\formatters.py:406, in BaseFormatter.__call__(self, obj)
        404     method = get_real_method(obj, self.print_method)
        405     if method is not None:
    --> 406         return method()
        407     return None
        408 else:
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\core\frame.py:1256, in DataFrame._repr_html_(self)
       1234     show_dimensions = get_option("display.show_dimensions")
       1236     formatter = fmt.DataFrameFormatter(
       1237         self,
       1238         columns=None,
       (...)
       1254         decimal=".",
       1255     )
    -> 1256     return fmt.DataFrameRenderer(formatter).to_html(notebook=True)
       1257 else:
       1258     return None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\format.py:929, in DataFrameRenderer.to_html(self, buf, encoding, classes, notebook, border, table_id, render_links)
        922 from pandas.io.formats.html import (
        923     HTMLFormatter,
        924     NotebookFormatter,
        925 )
        927 Klass = NotebookFormatter if notebook else HTMLFormatter
    --> 929 html_formatter = Klass(
        930     self.fmt,
        931     classes=classes,
        932     border=border,
        933     table_id=table_id,
        934     render_links=render_links,
        935 )
        936 string = html_formatter.to_string()
        937 return save_to_buffer(string, buf=buf, encoding=encoding)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\io\formats\html.py:68, in HTMLFormatter.__init__(self, formatter, classes, border, table_id, render_links)
         66 self.show_dimensions = self.fmt.show_dimensions
         67 if border is None or border is True:
    ---> 68     border = cast(int, get_option("func.html.border"))
         69 elif not border:
         70     border = None
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:274, in CallableDynamicDoc.__call__(self, *args, **kwds)
        273 def __call__(self, *args, **kwds) -> T:
    --> 274     return self.__func__(*args, **kwds)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:146, in _get_option(pat, silent)
        145 def _get_option(pat: str, silent: bool = False) -> Any:
    --> 146     key = _get_single_key(pat, silent)
        148     # walk the nested dict
        149     root, k = _get_root(key)
    

    File D:\codes\Pycharm\stock-insight\.venv\Lib\site-packages\pandas\_config\config.py:132, in _get_single_key(pat, silent)
        130     if not silent:
        131         _warn_if_deprecated(pat)
    --> 132     raise OptionError(f"No such keys(s): {repr(pat)}")
        133 if len(keys) > 1:
        134     raise OptionError("Pattern matched multiple keys")
    

    OptionError: No such keys(s): 'func.html.border'



                日期       开盘       收盘       最高       最低        成交量           成交额  \
    0   2024-10-21  3276.06  3268.11  3300.66  3239.10  668150299  8.557815e+11   
    1   2024-10-22  3263.82  3285.87  3294.96  3255.14  574913781  6.988615e+11   
    2   2024-10-23  3285.25  3302.80  3331.08  3277.07  650444128  7.600664e+11   
    3   2024-10-24  3287.82  3280.26  3292.94  3266.88  519827074  5.852489e+11   
    4   2024-10-25  3280.76  3299.70  3319.36  3276.13  595651707  6.772553e+11   
    ..         ...      ...      ...      ...      ...        ...           ...   
    64  2025-01-20  3256.15  3244.38  3268.26  3238.12  403337948  4.697410e+11   
    65  2025-01-21  3256.83  3242.62  3258.61  3229.07  384583718  4.682634e+11   
    66  2025-01-22  3235.49  3213.62  3235.50  3203.38  364817518  4.523129e+11   
    67  2025-01-23  3237.60  3230.16  3273.52  3229.57  458246803  5.398006e+11   
    68  2025-01-24  3222.88  3252.63  3260.01  3221.71  398653033  4.806851e+11   
    
          振幅   涨跌幅    涨跌额   换手率  
    0   1.89  0.20   6.55  1.43  
    1   1.22  0.54  17.76  1.23  
    2   1.64  0.52  16.93  1.39  
    3   0.79 -0.68 -22.54  1.11  
    4   1.32  0.59  19.44  1.27  
    ..   ...   ...    ...   ...  
    64  0.93  0.08   2.56  0.86  
    65  0.91 -0.05  -1.76  0.82  
    66  0.99 -0.89 -29.00  0.78  
    67  1.37  0.51  16.54  0.98  
    68  1.19  0.70  22.47  0.85  
    
    [69 rows x 11 columns]



```python
print(index_zh_a_hist_df.dtypes)
```

    日期      object
    开盘     float64
    收盘     float64
    最高     float64
    最低     float64
    成交量      int64
    成交额    float64
    振幅     float64
    涨跌幅    float64
    涨跌额    float64
    换手率    float64
    dtype: object
    


```python

```
