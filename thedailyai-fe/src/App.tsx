import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect } from 'react';

function App() {
  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      navigate('/home', { replace: true });
    }
  }, [navigate]);

  return (
    <>
      <h2>TheDaily.AI</h2>
      <h1>Your News, Your Way</h1>
      <div style={{ display: 'flex', flexDirection: 'column'}}>
        <button className='bubble-button' onClick={() => navigate("/onboard")}>Sign Up</button>
        <button className='text-button' onClick={() => navigate("/login")}>Already have an account? Log In</button>
      </div>

    </>
  )
}

export default App
