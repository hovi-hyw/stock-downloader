import React from 'react';
import { Card, Row, Col } from 'antd';
import { LineChart } from 'echarts/charts';
import { GridComponent } from 'echarts/components';
import * as echarts from 'echarts/core';

// 注册必需的组件
echarts.use([LineChart, GridComponent]);

const Home: React.FC = () => {
  return (
    <div className="home-page">
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card title="市场概览">
            <div>市场概览内容将在这里显示</div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="热门股票">
            <div>热门股票列表将在这里显示</div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="市场动态">
            <div>最新市场动态将在这里显示</div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Home;