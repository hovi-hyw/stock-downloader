import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Layout, Menu } from 'antd';
import { Outlet, useNavigate } from 'react-router-dom';
import {
  HomeOutlined,
  StockOutlined,
  LineChartOutlined,
  ExperimentOutlined
} from '@ant-design/icons';

const { Header, Content } = Layout;

const App = () => {
  const navigate = useNavigate();

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '首页',
    },
    {
      key: '/stock',
      icon: <StockOutlined />,
      label: '股票',
    },
    {
      key: '/index',
      icon: <LineChartOutlined />,
      label: '指数',
    },
    {
      key: '/strategy',
      icon: <ExperimentOutlined />,
      label: '策略',
    },
  ];

  return (
    <Layout className="min-h-screen">
      <Header className="bg-white">
        <div className="flex items-center">
          <h1 className="text-xl font-bold mr-8">股票数据分析系统</h1>
          <Menu
            mode="horizontal"
            items={menuItems}
            onClick={({ key }) => navigate(key)}
          />
        </div>
      </Header>
      <Content className="p-6">
        <Outlet />
      </Content>
    </Layout>
  );
};

export default App;
