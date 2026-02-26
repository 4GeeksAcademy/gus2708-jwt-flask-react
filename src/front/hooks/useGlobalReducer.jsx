import { useContext, createContext, useReducer } from "react";
import storeReducer, { initialStore } from "../store";
import Actions from "../actions";

const StoreContext = createContext();

export function StoreProvider({ children }) {
    const [store, dispatch] = useReducer(storeReducer, initialStore());
    return (
        <StoreContext.Provider value={{ store, dispatch }}>
            {children}
        </StoreContext.Provider>
    );
}

export default function useGlobalReducer() {
    const context = useContext(StoreContext);
    if (!context) throw Error("useGlobalReducer debe usarse dentro de un StoreProvider");

    const { store, dispatch } = context;
    
    const actions = new Actions(store, dispatch);

    return { store, dispatch, actions };
}