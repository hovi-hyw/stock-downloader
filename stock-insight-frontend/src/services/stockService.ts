import api from './api';

// 定义股票数据类型
export interface StockBasic {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  industry?: string;
  pe?: number;
  pb?: number;
}

export interface StockKline {
  date: string;
  open: number;
  close: number;
  high: number;
  low: number;
  volume: number;
}

export interface StockIndicator {
  symbol: string;
  name: string;
  ma5?: number;
  ma10?: number;
  ma20?: number;
  ma60?: number;
  rsi?: number;
  kdj?: {
    k: number;
    d: number;
    j: number;
  };
  macd?: {
    dif: number;
    dea: number;
    macd: number;
  };
}

// 股票数据服务
const stockService = {
  // 获取股票列表
  getStockList: async () => {
    return api.get<StockBasic[]>('/stocks');
  },

  // 获取单只股票基本信息
  getStockInfo: async (symbol: string) => {
    return api.get<StockBasic>(`/stocks/${symbol}`);
  },

  // 获取股票K线数据
  getStockKline: async (symbol: string, period: string = 'daily', limit: number = 90) => {
    return api.get<StockKline[]>(`/stocks/${symbol}/kline`, {
      params: { period, limit }
    });
  },

  // 获取股票技术指标
  getStockIndicators: async (symbol: string) => {
    return api.get<StockIndicator>(`/stocks/${symbol}/indicators`);
  },

  // 搜索股票
  searchStocks: async (keyword: string) => {
    return api.get<StockBasic[]>('/stocks', {
      params: { keyword }
    });
  }
};

export default stockService;