import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import Onboard from './Onboard.tsx'
import Home from './Home.tsx'

const router = createBrowserRouter([
  {
    path: '',
    element: <App />
  },
  {
    path: '/onboard',
    element: <Onboard />
  },
  {
    path: '/home',
    element: <Home />
  }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
