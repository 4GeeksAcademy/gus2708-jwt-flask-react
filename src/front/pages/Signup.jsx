import {useEffect, useState} from 'react'
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { Link } from 'react-router-dom';

const Login = () => {
  
  const navigate = useNavigate();
    
  const { actions } = useGlobalReducer()
  const [ email, setEmail ] = useState("")
  const [ password, setPassword] = useState("")

  useEffect(() => {
    if(localStorage.getItem("token")){
      navigate("/")
      alert("You are already logged in.")
    }
  }, [])

  const handleSubmit =  async (e) => {
    e.preventDefault()
    const userEmail = email
    const userPassword = password
    const isregistered = await actions.register(userEmail, userPassword)
    if(isregistered){
      const islogged = await actions.login(userEmail, userPassword)
      if(islogged){
        navigate("/")
      } else {
        alert("Signup successful but login failed.")
      }
    } else {
      alert("Signup failed. Please check your credentials and try again.")
    }
  }


  return (
    <div className="modal modal-sheet position-static d-block bg-body-secondary p-4 py-md-5" tabIndex={-1} role="dialog" id="modalSignin">
      <div className="modal-dialog">
        <div className="modal-content rounded-4 shadow">
          <div className="modal-header p-5 pb-4 border-bottom-0">
            <h1 className="fw-bold mb-0 fs-2">Signup</h1>
            <Link to="/" className="btn btn-close" data-bs-dismiss="modal" aria-label="Close" />
          </div>
          <div className="modal-body p-5 pt-0">
            <form className="needs-validation" onSubmit={handleSubmit}>
              <div className="form-floating mb-3">
                <input type="email" className="form-control rounded-3" id="floatingInput" placeholder="name@example.com" value={email} onChange={(e) => setEmail(e.target.value)} />
                <label htmlFor="floatingInput">Email address</label>
              </div>
              <div className="form-floating mb-4">
                <input type="password" className="form-control rounded-3" id="floatingPassword" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                <label htmlFor="floatingPassword">Password</label>
              </div>
              <button className="w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">Signup</button>
              <p className='text-center mt-2'>or maybe you want to <Link to="/login">Login</Link></p>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login