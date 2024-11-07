import axios from "axios";
import React from "react";

function Login({ setToken }) {
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://192.168.178.127:5000/login',{username:user,password:password});
      setToken(response.data.access_token);
    } catch (error) {
      console.error(error);
      alert('Error logging in');
    }
  } 
  const [user, setUser] = React.useState('');
  const [password, setPassword] = React.useState('');
  const changeUser = (e) => {
    setUser(e.target.value);
  }
  const changePassword = (e) => {
    setPassword(e.target.value);
  }
  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>user</label>
          <input type="text" className="form-control" value={user} onChange={changeUser}/>
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" className="form-control" value={password} onChange={changePassword} />
        </div>
        <button className="btn btn-primary">Login</button>
      </form>
    </div>
  );
}

export default Login;
