import React from 'react';
import { Card, Table, Space, Input } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface IndexData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  turnoverRate: number;
}

const Index: React.FC = () => {
  const columns: ColumnsType<IndexData> = [
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
      title: '最新点位',
      dataIndex: 'price',
      key: 'price',
    },
    {
      title: '涨跌点',
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
    {
      title: '换手率',
      dataIndex: 'turnoverRate',
      key: 'turnoverRate',
      render: (rate: number) => `${rate}%`,
    },
  ];

  return (
    <div className="index-page">
      <Card title="指数列表" className="mb-4">
        <Space direction="vertical" style={{ width: '100%' }}>
          <Input.Search
            placeholder="输入指数代码或名称搜索"
            style={{ maxWidth: 300 }}
          />
          <Table<IndexData>
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

export default Index;