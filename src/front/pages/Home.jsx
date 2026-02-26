import React, { useEffect } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { Link } from "react-router-dom";

export const Home = () => {

	const { store, dispatch } = useGlobalReducer()

	useEffect(() => {
	}, [])

	return (
		<div className="text-center mt-5">
			{store.jwt ? (
				<h1 className="text-4xl font-bold mb-4">Hello, <Link to="/user">{store.user.email}</Link>!</h1>
			) : (
				<>
					<h1 className="text-4xl font-bold mb-4">Please log in to continue.</h1>
					<Link to="/login" className="btn btn-primary">Login</Link>
				</>
			)}
		</div>
	);
}; 