import React from 'react';
import { Card, Form, Select, Button, Table, Space } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface StrategyResult {
  symbol: string;
  name: string;
  score: number;
  reason: string;
}

const Strategy: React.FC = () => {
  const columns: ColumnsType<StrategyResult> = [
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
      title: '评分',
      dataIndex: 'score',
      key: 'score',
      render: (score: number) => (
        <span style={{ color: score >= 80 ? '#f5222d' : score >= 60 ? '#fa8c16' : '#52c41a' }}>
          {score}
        </span>
      ),
    },
    {
      title: '选股理由',
      dataIndex: 'reason',
      key: 'reason',
    },
  ];

  return (
    <div className="strategy-page">
      <Card title="选股策略配置" className="mb-4">
        <Form layout="inline">
          <Form.Item label="策略类型" name="strategyType">
            <Select
              style={{ width: 200 }}
              placeholder="请选择策略类型"
              options={[
                { label: '价值投资', value: 'value' },
                { label: '趋势跟踪', value: 'trend' },
                { label: '技术分析', value: 'technical' },
              ]}
            />
          </Form.Item>
          <Form.Item>
            <Button type="primary">运行策略</Button>
          </Form.Item>
        </Form>
      </Card>

      <Card title="策略运行结果">
        <Table<StrategyResult>
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
      </Card>
    </div>
  );
};

export default Strategy;