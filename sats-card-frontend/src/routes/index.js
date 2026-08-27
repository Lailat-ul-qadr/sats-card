import React from 'react';
import { Navigate } from 'react-router-dom';

// Placeholder pages (to be created)
const Landing = () => <div>Landing</div>;
const Dashboard = () => <div>Dashboard</div>;
const Login = () => <div>Login</div>;
const Signup = () => <div>Signup</div>;
const Card = () => <div>Card</div>;
const Fund = () => <div>Fund</div>;
const Send = () => <div>Send</div>;
const Receive = () => <div>Receive</div>;
const Spend = () => <div>Spend</div>;
const Transactions = () => <div>Transactions</div>;
const Profile = () => <div>Profile</div>;
const Settings = () => <div>Settings</div>;
const Help = () => <div>Help</div>;

export const routes = [
  {
    path: '/',
    element: <Landing />,
    public: true,
  },
  {
    path: '/login',
    element: <Login />,
    public: true,
  },
  {
    path: '/signup',
    element: <Signup />,
    public: true,
  },
  {
    path: '/dashboard',
    element: <Dashboard />,
    public: false,
  },
  {
    path: '/card',
    element: <Card />,
    public: false,
  },
  {
    path: '/fund',
    element: <Fund />,
    public: false,
  },
  {
    path: '/send',
    element: <Send />,
    public: false,
  },
  {
    path: '/receive',
    element: <Receive />,
    public: false,
  },
  {
    path: '/spend',
    element: <Spend />,
    public: false,
  },
  {
    path: '/transactions',
    element: <Transactions />,
    public: false,
  },
  {
    path: '/profile',
    element: <Profile />,
    public: false,
  },
  {
    path: '/settings',
    element: <Settings />,
    public: false,
  },
  {
    path: '/help',
    element: <Help />,
    public: false,
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
];
