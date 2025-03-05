import api from './api';

// 定义指数数据类型
export interface IndexBasic {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  turnoverRate?: number;
}

export interface IndexKline {
  date: string;
  open: number;
  close: number;
  high: number;
  low: number;
  volume: number;
}

export interface IndexComponent {
  symbol: string;
  name: string;
  weight: number;
  price: number;
  change: number;
  changePercent: number;
}

// 指数数据服务
const indexService = {
  // 获取指数列表
  getIndexList: async () => {
    return api.get<IndexBasic[]>('/indices');
  },

  // 获取单个指数基本信息
  getIndexInfo: async (symbol: string) => {
    return api.get<IndexBasic>(`/indices/${symbol}`);
  },

  // 获取指数K线数据
  getIndexKline: async (symbol: string, period: string = 'daily', limit: number = 90) => {
    return api.get<IndexKline[]>(`/indices/${symbol}/kline`, {
      params: { period, limit }
    });
  },

  // 获取指数成分股
  getIndexComponents: async (symbol: string) => {
    return api.get<IndexComponent[]>(`/indices/${symbol}/components`);
  },

  // 搜索指数
  searchIndices: async (keyword: string) => {
    return api.get<IndexBasic[]>('/indices', {
      params: { keyword }
    });
  }
};

export default indexService;