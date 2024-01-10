import { redirect, useNavigate } from 'react-router-dom'
import './App.css'

function App() {
  const navigate = useNavigate();

  return (
    <>
      <h2>TheDaily.AI</h2>
      <h1>Your News, Your Way</h1>
      <button onClick={() => navigate("/onboard")}>Get Started</button>
    </>
  )
}

export default App
