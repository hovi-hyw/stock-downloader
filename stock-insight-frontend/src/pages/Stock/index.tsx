import React from 'react';
import { Card, Table, Space, Input } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface StockData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
}

const Stock: React.FC = () => {
  const columns: ColumnsType<StockData> = [
    {
      title: '代码',
      dataIndex: 'symbol',
      key: 'symbol',
    },
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '最新价',
      dataIndex: 'price',
      key: 'price',
    },
    {
      title: '涨跌额',
      dataIndex: 'change',
      key: 'change',
      render: (change: number) => (
        <span style={{ color: change > 0 ? '#f5222d' : change < 0 ? '#52c41a' : 'inherit' }}>
          {change > 0 ? '+' : ''}{change}
        </span>
      ),
    },
    {
      title: '涨跌幅',
      dataIndex: 'changePercent',
      key: 'changePercent',
      render: (percent: number) => (
        <span style={{ color: percent > 0 ? '#f5222d' : percent < 0 ? '#52c41a' : 'inherit' }}>
          {percent > 0 ? '+' : ''}{percent}%
        </span>
      ),
    },
  ];

  return (
    <div className="stock-page">
      <Card title="股票列表" className="mb-4">
        <Space direction="vertical" style={{ width: '100%' }}>
          <Input.Search
            placeholder="输入股票代码或名称搜索"
            style={{ maxWidth: 300 }}
          />
          <Table<StockData>
            columns={columns}
            dataSource={[]}
            rowKey="symbol"
            pagination={{
              total: 0,
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
            }}
          />
        </Space>
      </Card>
    </div>
  );
};

export default Stock;