import api from './api';

// 定义策略数据类型
export interface Strategy {
  id: string;
  name: string;
  description: string;
  type: string;
  parameters?: Record<string, any>;
}

export interface StrategyParameter {
  name: string;
  label: string;
  type: string;
  default?: any;
  options?: Array<{label: string; value: any}>;
  min?: number;
  max?: number;
}

export interface StrategyResult {
  id: string;
  strategyId: string;
  createdAt: string;
  stocks: StrategyResultStock[];
}

export interface StrategyResultStock {
  symbol: string;
  name: string;
  score: number;
  reason: string;
  price?: number;
  change?: number;
  changePercent?: number;
}

// 策略服务
const strategyService = {
  // 获取可用策略列表
  getStrategies: async () => {
    return api.get<Strategy[]>('/strategies');
  },

  // 获取策略详情
  getStrategyDetail: async (id: string) => {
    return api.get<Strategy>(`/strategies/${id}`);
  },

  // 运行选股策略
  runStrategy: async (id: string, parameters?: Record<string, any>) => {
    return api.post<{resultId: string}>(`/strategies/${id}/run`, { parameters });
  },

  // 获取策略运行结果
  getStrategyResult: async (resultId: string) => {
    return api.get<StrategyResult>(`/strategies/results/${resultId}`);
  },

  // 获取历史策略结果列表
  getStrategyResultHistory: async (strategyId?: string) => {
    return api.get<StrategyResult[]>('/strategies/results', {
      params: { strategyId }
    });
  }
};

export default strategyService;