import { Link, useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";


export const Navbar = () => {
	const navigate = useNavigate();
	const { store, actions } = useGlobalReducer()

	const handleLogout = async () => {
		await actions.logout()
		navigate("/login")
	}

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">User interface</span>
				</Link>
				<div className="ml-auto">
					{store.jwt ? (
						<div className="container d-flex align-items-between">
							<span className="navbar-text me-3">Hello, {store.user.email}!</span>
							<button className="btn btn-outline-danger" onClick={handleLogout}>Logout</button>
						</div>
					) : (
						<>	
							<Link to="/login" className="btn btn-outline-primary me-2">Login</Link>
							<Link to="/signup" className="btn btn-outline-success">Sign Up</Link>
						</>
					)}
				</div>
			</div>
		</nav>
	);
};