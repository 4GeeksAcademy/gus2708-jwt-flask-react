import React from "react";
import { Navigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

const User = () => {
    const { store } = useGlobalReducer();
    if (!store.jwt) {
        alert("You must be logged in to view this page.");
        return <Navigate to="/login" replace />;
    }
    return (
        <div className="text-center mt-5">
            <h1 className="text-4xl font-bold mb-4">This is {store.user.email} user page!</h1>
            <p>This page is only accessible to logged-in users.</p>
        </div>
    );
};

export default User;