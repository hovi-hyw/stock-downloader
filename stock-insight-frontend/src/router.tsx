import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import Home from './pages/Home';
import Stock from './pages/Stock';
import Index from './pages/Index';
import Strategy from './pages/Strategy';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <Home />,
      },
      {
        path: '/stock',
        element: <Stock />,
      },
      {
        path: '/index',
        element: <Index />,
      },
      {
        path: '/strategy',
        element: <Strategy />,
      },
    ],
  },
]);

export default router;